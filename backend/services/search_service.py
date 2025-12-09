"""Search service for semantic product search using Pinecone"""

from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Any, Optional
from models.schemas import Product, SearchRequest
from services.embedding_service import EmbeddingService
import json
import os


class SearchService:
    """Service for semantic product search using vector embeddings"""
    
    def __init__(self, embedding_service: EmbeddingService, index_name: str = "products"):
        """
        Initialize search service with Pinecone
        
        Args:
            embedding_service: Instance of EmbeddingService for generating embeddings
            index_name: Name of the Pinecone index
        """
        self.embedding_service = embedding_service
        self.index_name = index_name
        
        # Initialize Pinecone client
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY environment variable is required")
        
        self.pc = Pinecone(api_key=api_key)
        
        # Get embedding dimension
        embedding_dim = self.embedding_service.get_model_info()["embedding_dimension"]
        
        # Create index if it doesn't exist
        if index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=index_name,
                dimension=embedding_dim,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
        
        # Connect to index
        self.index = self.pc.Index(index_name)
        
        # Wait for index to be ready
        import time
        time.sleep(1)
        
        stats = self.index.describe_index_stats()
        print(f"✓ Search service initialized with {stats['total_vector_count']} products")
    
    def index_products(self, products: List[Dict[str, Any]]) -> int:
        """
        Index products in Pinecone with embeddings
        
        Args:
            products: List of product dictionaries to index
            
        Returns:
            Number of products indexed
        """
        if not products:
            return 0
        
        # Check if products already exist
        stats = self.index.describe_index_stats()
        existing_count = stats['total_vector_count']
        if existing_count >= len(products):
            print(f"Products already indexed ({existing_count} products)")
            return existing_count
        
        print(f"Indexing {len(products)} products...")
        
        # Prepare vectors for upsert
        vectors = []
        
        for product in products:
            # Create searchable text from product data
            searchable_text = f"{product['name']} {product['description']} {product['category']} {' '.join(product.get('tags', []))}"
            
            # Generate embedding
            embedding = self.embedding_service.generate_embedding(searchable_text)
            
            # Prepare metadata (Pinecone supports flat metadata)
            metadata = {
                "name": product['name'],
                "category": product['category'],
                "price": float(product['price']),
                "rating": float(product.get('rating', 0)),
                "description": product['description'][:500],  # Limit description length
                "image": product.get('image', ''),
                "tags": ','.join(product.get('tags', []))
            }
            
            vectors.append({
                "id": product['id'],
                "values": embedding,
                "metadata": metadata
            })
        
        # Upsert vectors in batches
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            self.index.upsert(vectors=batch)
        
        print(f"✓ Indexed {len(products)} products successfully")
        return len(products)
    
    def search(
        self,
        query: str,
        limit: int = 10,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[Product]:
        """
        Perform semantic search for products
        
        Args:
            query: Search query text
            limit: Maximum number of results to return
            category: Optional category filter
            min_price: Optional minimum price filter
            max_price: Optional maximum price filter
            
        Returns:
            List of matching Product objects
        """
        # Generate query embedding
        query_embedding = self.embedding_service.generate_embedding(query)
        
        # Build filter conditions
        filter_dict = {}
        if category:
            filter_dict["category"] = {"$eq": category}
        if min_price is not None:
            filter_dict["price"] = filter_dict.get("price", {})
            filter_dict["price"]["$gte"] = min_price
        if max_price is not None:
            filter_dict["price"] = filter_dict.get("price", {})
            filter_dict["price"]["$lte"] = max_price
        
        # Perform search
        results = self.index.query(
            vector=query_embedding,
            top_k=limit,
            include_metadata=True,
            filter=filter_dict if filter_dict else None
        )
        
        # Parse results
        products = []
        for match in results['matches']:
            metadata = match['metadata']
            product_data = {
                "id": match['id'],
                "name": metadata['name'],
                "description": metadata['description'],
                "category": metadata['category'],
                "price": metadata['price'],
                "rating": metadata.get('rating', 0),
                "image": metadata.get('image', ''),
                "tags": metadata.get('tags', '').split(',') if metadata.get('tags') else []
            }
            products.append(Product(**product_data))
        
        return products
    
    def get_all_products(self) -> List[Product]:
        """
        Get all indexed products
        
        Returns:
            List of all Product objects
        """
        # Pinecone doesn't support fetching all vectors easily
        # We'll use a dummy query to get products
        stats = self.index.describe_index_stats()
        total = stats['total_vector_count']
        
        if total == 0:
            return []
        
        # Query with a zero vector to get random samples (or all if small dataset)
        embedding_dim = self.embedding_service.get_model_info()["embedding_dimension"]
        dummy_vector = [0.0] * embedding_dim
        
        results = self.index.query(
            vector=dummy_vector,
            top_k=min(total, 10000),  # Limit to reasonable number
            include_metadata=True
        )
        
        products = []
        for match in results['matches']:
            metadata = match['metadata']
            product_data = {
                "id": match['id'],
                "name": metadata['name'],
                "description": metadata['description'],
                "category": metadata['category'],
                "price": metadata['price'],
                "rating": metadata.get('rating', 0),
                "image": metadata.get('image', ''),
                "tags": metadata.get('tags', '').split(',') if metadata.get('tags') else []
            }
            products.append(Product(**product_data))
        
        return products
    
    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """
        Get a specific product by ID
        
        Args:
            product_id: Product ID to retrieve
            
        Returns:
            Product object or None if not found
        """
        try:
            results = self.index.fetch(ids=[product_id])
            if product_id in results['vectors']:
                metadata = results['vectors'][product_id]['metadata']
                product_data = {
                    "id": product_id,
                    "name": metadata['name'],
                    "description": metadata['description'],
                    "category": metadata['category'],
                    "price": metadata['price'],
                    "rating": metadata.get('rating', 0),
                    "image": metadata.get('image', ''),
                    "tags": metadata.get('tags', '').split(',') if metadata.get('tags') else []
                }
                return Product(**product_data)
        except Exception as e:
            print(f"Error retrieving product {product_id}: {e}")
        
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get search service statistics
        
        Returns:
            Dictionary with statistics
        """
        stats = self.index.describe_index_stats()
        return {
            "total_products": stats['total_vector_count'],
            "index_name": self.index_name,
            "embedding_model": self.embedding_service.model_name
        }
