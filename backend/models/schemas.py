from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class Product(BaseModel):
    """Product model for the shopping assistant"""
    id: str
    name: str
    description: str
    category: str
    price: float
    tags: List[str] = []
    image_url: Optional[str] = None
    rating: Optional[float] = 4.0
    in_stock: bool = True
    brand: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "prod_001",
                "name": "Waterproof Rain Jacket",
                "description": "Lightweight waterproof jacket perfect for rainy weather",
                "category": "Outerwear",
                "price": 79.99,
                "tags": ["rainwear", "waterproof", "outdoor", "jacket"],
                "rating": 4.5,
                "in_stock": True,
                "brand": "WeatherPro"
            }
        }


class Document(BaseModel):
    """Document model for RAG knowledge base"""
    id: str
    title: str
    content: str
    doc_type: str  # FAQ, guide, spec, tutorial
    category: Optional[str] = None
    tags: List[str] = []
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "doc_001",
                "title": "How to choose rain gear",
                "content": "When selecting rain gear, consider waterproof rating, breathability, and fit...",
                "doc_type": "guide",
                "category": "Outerwear",
                "tags": ["rainwear", "guide", "buying-tips"]
            }
        }


class SearchRequest(BaseModel):
    """Search request model"""
    query: str
    limit: int = Field(default=10, ge=1, le=50)
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None


class SearchResponse(BaseModel):
    """Search response model"""
    query: str
    results: List[Product]
    total: int
    semantic_matches: bool = True


class ChatRequest(BaseModel):
    """Chat/RAG request model"""
    question: str
    context_limit: int = Field(default=3, ge=1, le=10)
    include_products: bool = True


class ChatResponse(BaseModel):
    """Chat/RAG response model"""
    question: str
    answer: str
    sources: List[Dict[str, Any]] = []
    related_products: List[Product] = []


class RecommendationRequest(BaseModel):
    """Recommendation request model"""
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    query: Optional[str] = None
    limit: int = Field(default=5, ge=1, le=20)


class RecommendationResponse(BaseModel):
    """Recommendation response model"""
    based_on: str
    recommendations: List[Product]
    similarity_scores: Optional[List[float]] = None
