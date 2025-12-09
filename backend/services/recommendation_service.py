"""Recommendation service for product recommendations based on similarity"""

from typing import List, Optional, Dict, Any
from models.schemas import Product
from services.embedding_service import EmbeddingService
from services.search_service import SearchService
import json


class RecommendationService:
    """Service for generating product recommendations based on embeddings"""
    
    def __init__(self, search_service: SearchService, embedding_service: EmbeddingService):
        """
        Initialize recommendation service
        
        Args:
            search_service: Instance of SearchService
            embedding_service: Instance of EmbeddingService
        """
        self.search_service = search_service
        self.embedding_service = embedding_service
        print("✓ Recommendation service initialized")
    
    def recommend_by_product_id(self, product_id: str, limit: int = 5) -> tuple[List[Product], List[float]]:
        """
        Get product recommendations based on a product ID
        
        Args:
            product_id: ID of the product to base recommendations on
            limit: Number of recommendations to return
            
        Returns:
            Tuple of (list of recommended products, list of similarity scores)
        """
        # Get the source product embedding
        try:
            results = self.search_service.index.fetch(ids=[product_id])
            
            if product_id not in results['vectors']:
                return [], []
            
            source_embedding = results['vectors'][product_id]['values']
            
            # Find similar products
            similar_results = self.search_service.index.query(
                vector=source_embedding,
                top_k=limit + 1,  # +1 to account for the source product itself
                include_metadata=True
            )
            
            recommendations = []
            scores = []
            
            for match in similar_results['matches']:
                # Skip the source product itself
                if match['id'] == product_id:
                    continue
                
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
                recommendations.append(Product(**product_data))
                scores.append(match['score'])
                
                if len(recommendations) >= limit:
                    break
            
            return recommendations, scores
            
        except Exception as e:
            print(f"Error getting recommendations for product {product_id}: {e}")
            return [], []
    
    def recommend_by_product_name(self, product_name: str, limit: int = 5) -> tuple[List[Product], List[float]]:
        """
        Get product recommendations based on a product name
        
        Args:
            product_name: Name of the product to base recommendations on
            limit: Number of recommendations to return
            
        Returns:
            Tuple of (list of recommended products, list of similarity scores)
        """
        # Search for the product by name
        products = self.search_service.search(query=product_name, limit=1)
        
        if not products:
            return [], []
        
        # Get recommendations based on the found product
        return self.recommend_by_product_id(products[0].id, limit)
    
    def recommend_by_query(self, query: str, limit: int = 5) -> tuple[List[Product], List[float]]:
        """
        Get product recommendations based on a free-text query
        
        Args:
            query: Text query describing desired products
            limit: Number of recommendations to return
            
        Returns:
            Tuple of (list of recommended products, list of similarity scores)
        """
        # Generate embedding for the query
        query_embedding = self.embedding_service.generate_embedding(query)
        
        # Find similar products
        results = self.search_service.index.query(
            vector=query_embedding,
            top_k=limit,
            include_metadata=True
        )
        
        recommendations = []
        scores = []
        
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
            recommendations.append(Product(**product_data))
            scores.append(match['score'])
        
        return recommendations, scores
    
    def recommend_similar_items(
        self,
        product_id: Optional[str] = None,
        product_name: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 5
    ) -> tuple[List[Product], List[float], str]:
        """
        Unified recommendation method that handles different input types
        
        Args:
            product_id: Optional product ID
            product_name: Optional product name
            query: Optional text query
            limit: Number of recommendations to return
            
        Returns:
            Tuple of (recommendations, scores, basis for recommendations)
        """
        if product_id:
            recommendations, scores = self.recommend_by_product_id(product_id, limit)
            basis = f"Similar to product {product_id}"
        elif product_name:
            recommendations, scores = self.recommend_by_product_name(product_name, limit)
            basis = f"Similar to '{product_name}'"
        elif query:
            recommendations, scores = self.recommend_by_query(query, limit)
            basis = f"Based on your interest in '{query}'"
        else:
            return [], [], "No basis provided"
        
        return recommendations, scores, basis
    
    def get_category_recommendations(self, category: str, limit: int = 5) -> List[Product]:
        """
        Get top-rated products from a specific category
        
        Args:
            category: Product category
            limit: Number of recommendations to return
            
        Returns:
            List of recommended products
        """
        products = self.search_service.search(query=category, limit=limit * 2, category=category)
        
        # Sort by rating and return top N
        sorted_products = sorted(products, key=lambda p: p.rating or 0, reverse=True)
        return sorted_products[:limit]
