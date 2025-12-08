"""Search service for semantic product search using ChromaDB"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from models.schemas import Product, SearchRequest
from services.embedding_service import EmbeddingService
import json


class SearchService:
    """Service for semantic product search using vector embeddings"""
    
    def __init__(self, embedding_service: EmbeddingService, persist_directory: str = "./chroma_db"):
        """
        Initialize search service with ChromaDB
        
        Args:
            embedding_service: Instance of EmbeddingService for generating embeddings
            persist_directory: Directory to persist ChromaDB data
        """
        self.embedding_service = embedding_service
        
        # Initialize ChromaDB client
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Get or create collection for products
        self.products_collection = self.client.get_or_create_collection(
            name="products",
            metadata={"description": "Product catalog with embeddings"}
        )
        
        print(f"✓ Search service initialized with {self.products_collection.count()} products")
    
    def index_products(self, products: List[Dict[str, Any]]) -> int:
        """
        Index products in ChromaDB with embeddings
        
        Args:
            products: List of product dictionaries to index
            
        Returns:
            Number of products indexed
        """
        if not products:
            return 0
        
        # Check if products already exist
        existing_count = self.products_collection.count()
        if existing_count >= len(products):
            print(f"Products already indexed ({existing_count} products)")
            return existing_count
        
        print(f"Indexing {len(products)} products...")
        
        # Prepare data for indexing
        ids = []
        embeddings = []
        metadatas = []
        documents = []
        
        for product in products:
            # Create searchable text from product data
            searchable_text = f"{product['name']} {product['description']} {product['category']} {' '.join(product.get('tags', []))}"
            
            # Generate embedding
            embedding = self.embedding_service.generate_embedding(searchable_text)
            
            ids.append(product['id'])
            embeddings.append(embedding)
            documents.append(searchable_text)
            metadatas.append({
                "name": product['name'],
                "category": product['category'],
                "price": product['price'],
                "product_json": json.dumps(product)  # Store full product as JSON
            })
        
        # Add to collection
        self.products_collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )
        
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
        where_conditions = {}
        if category:
            where_conditions["category"] = category
        
        # Perform search
        results = self.products_collection.query(
            query_embeddings=[query_embedding],
            n_results=min(limit * 2, 50),  # Get more results for filtering
            where=where_conditions if where_conditions else None
        )
        
        # Parse results and apply additional filters
        products = []
        if results['ids'] and results['ids'][0]:
            for i, metadata in enumerate(results['metadatas'][0]):
                product_data = json.loads(metadata['product_json'])
                
                # Apply price filters
                if min_price is not None and product_data['price'] < min_price:
                    continue
                if max_price is not None and product_data['price'] > max_price:
                    continue
                
                products.append(Product(**product_data))
                
                if len(products) >= limit:
                    break
        
        return products
    
    def get_all_products(self) -> List[Product]:
        """
        Get all indexed products
        
        Returns:
            List of all Product objects
        """
        results = self.products_collection.get()
        
        products = []
        if results['metadatas']:
            for metadata in results['metadatas']:
                product_data = json.loads(metadata['product_json'])
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
            results = self.products_collection.get(ids=[product_id])
            if results['metadatas']:
                product_data = json.loads(results['metadatas'][0]['product_json'])
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
        return {
            "total_products": self.products_collection.count(),
            "collection_name": self.products_collection.name,
            "embedding_model": self.embedding_service.model_name
        }
