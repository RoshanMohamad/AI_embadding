"""Search service for semantic product search using ChromaDB"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import chromadb
from models.schemas import Product
from services.embedding_service import EmbeddingService
import json
import os


class SearchService:
    """Service for semantic product search using vector embeddings"""
    
    def __init__(self, embedding_service: EmbeddingService, collection_name: str = "products"):
        """
        Initialize search service with ChromaDB
        
        Args:
            embedding_service: Instance of EmbeddingService for generating embeddings
            collection_name: Name of the ChromaDB collection
        """
        self.embedding_service = embedding_service
        self.collection_name = collection_name

        persist_directory = os.getenv(
            "CHROMA_DB_PATH",
            str(Path(__file__).resolve().parents[1] / "chroma_db")
        )
        self.persist_directory = persist_directory
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        print(f"✓ Search service initialized with {self.collection.count()} products")

    def _build_metadata(self, product: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "name": product["name"],
            "category": product["category"],
            "price": float(product["price"]),
            "rating": float(product.get("rating", 0)),
            "description": product["description"][:500],
            "image_url": product.get("image_url", ""),
            "tags": json.dumps(product.get("tags", [])),
            "brand": product.get("brand", ""),
            "in_stock": bool(product.get("in_stock", True))
        }

    def _parse_tags(self, value: Any) -> List[str]:
        if not value:
            return []

        if isinstance(value, list):
            return [str(tag) for tag in value]

        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return [str(tag) for tag in parsed]
            except json.JSONDecodeError:
                return [tag for tag in value.split(',') if tag]

        return []

    def _product_from_metadata(self, product_id: str, metadata: Dict[str, Any]) -> Product:
        product_data = {
            "id": product_id,
            "name": metadata.get("name", ""),
            "description": metadata.get("description", ""),
            "category": metadata.get("category", ""),
            "price": float(metadata.get("price", 0)),
            "rating": float(metadata.get("rating", 0)) if metadata.get("rating") is not None else None,
            "tags": self._parse_tags(metadata.get("tags")),
            "image_url": metadata.get("image_url") or None,
            "in_stock": bool(metadata.get("in_stock", True)),
            "brand": metadata.get("brand") or None,
        }
        return Product(**product_data)

    def _query_collection(
        self,
        query_embedding: List[float],
        limit: int,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        where: Dict[str, Any] = {}
        if category:
            where["category"] = category
        if min_price is not None:
            where["price"] = where.get("price", {})
            where["price"]["$gte"] = min_price
        if max_price is not None:
            where["price"] = where.get("price", {})
            where["price"]["$lte"] = max_price

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            where=where or None,
            include=["metadatas", "distances"]
        )

        matches: List[Dict[str, Any]] = []
        ids = results.get("ids", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for product_id, metadata, distance in zip(ids, metadatas, distances):
            matches.append({
                "id": product_id,
                "metadata": metadata or {},
                "score": 1 - float(distance) if distance is not None else 0.0,
            })

        return matches

    def query_products(
        self,
        query_embedding: List[float],
        limit: int = 10,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        return self._query_collection(
            query_embedding=query_embedding,
            limit=limit,
            category=category,
            min_price=min_price,
            max_price=max_price
        )
    
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

        print(f"Indexing {len(products)} products...")

        ids = []
        embeddings = []
        metadatas = []
        documents = []

        for product in products:
            # Create searchable text from product data
            searchable_text = f"{product['name']} {product['description']} {product['category']} {' '.join(product.get('tags', []))}"

            ids.append(product['id'])
            embeddings.append(self.embedding_service.generate_embedding(searchable_text))
            metadatas.append(self._build_metadata(product))
            documents.append(searchable_text)
        
        # Upsert vectors in batches
        batch_size = 100
        for i in range(0, len(ids), batch_size):
            self.collection.upsert(
                ids=ids[i:i + batch_size],
                embeddings=embeddings[i:i + batch_size],
                metadatas=metadatas[i:i + batch_size],
                documents=documents[i:i + batch_size]
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
        query_embedding = self.embedding_service.generate_embedding(query)

        matches = self.query_products(
            query_embedding=query_embedding,
            limit=limit,
            category=category,
            min_price=min_price,
            max_price=max_price
        )

        products = []
        for match in matches:
            products.append(self._product_from_metadata(match['id'], match['metadata']))
        
        return products
    
    def get_all_products(self) -> List[Product]:
        """
        Get all indexed products
        
        Returns:
            List of all Product objects
        """
        results = self.collection.get(include=["metadatas"])
        ids = results.get("ids", [])

        if not ids:
            return []

        products = []
        metadatas = results.get("metadatas", [])

        for product_id, metadata in zip(ids, metadatas):
            products.append(self._product_from_metadata(product_id, metadata or {}))
        
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
            results = self.collection.get(ids=[product_id], include=["metadatas"])
            ids = results.get("ids", [])
            metadatas = results.get("metadatas", [])
            if ids:
                return self._product_from_metadata(ids[0], metadatas[0] or {})
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
            "total_products": self.collection.count(),
            "collection_name": self.collection_name,
            "vector_store": "chroma",
            "persist_directory": self.persist_directory,
            "embedding_model": self.embedding_service.model_name
        }
