"""
AI Personal Shopping & Knowledge Assistant - FastAPI Backend

This backend provides:
- Semantic search for products
- RAG-based question answering
- Product recommendations based on embeddings
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Dict, Any

from models.schemas import (
    Product, SearchRequest, SearchResponse,
    ChatRequest, ChatResponse,
    RecommendationRequest, RecommendationResponse
)
from services.embedding_service import EmbeddingService
from services.search_service import SearchService
from services.rag_service import RAGService
from services.recommendation_service import RecommendationService
from data.sample_data import PRODUCTS, DOCUMENTS


# Global service instances
embedding_service: EmbeddingService = None
search_service: SearchService = None
rag_service: RAGService = None
recommendation_service: RecommendationService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup"""
    global embedding_service, search_service, rag_service, recommendation_service
    
    print("\n" + "="*60)
    print("🚀 Initializing AI Shopping Assistant Backend")
    print("="*60)
    
    # Initialize embedding service
    print("\n1️⃣ Loading embedding model...")
    embedding_service = EmbeddingService(model_name='all-MiniLM-L6-v2')
    
    # Initialize search service
    print("\n2️⃣ Initializing search service...")
    search_service = SearchService(embedding_service)
    
    # Index products
    print("\n3️⃣ Indexing products...")
    search_service.index_products(PRODUCTS)
    
    # Initialize RAG service
    print("\n4️⃣ Initializing RAG service...")
    rag_service = RAGService(embedding_service, search_service)
    
    # Index documents
    print("\n5️⃣ Indexing knowledge base...")
    rag_service.index_documents(DOCUMENTS)
    
    # Initialize recommendation service
    print("\n6️⃣ Initializing recommendation service...")
    recommendation_service = RecommendationService(search_service, embedding_service)
    
    print("\n" + "="*60)
    print("✅ All services initialized successfully!")
    print("="*60)
    print(f"📊 Stats:")
    print(f"   - Products indexed: {search_service.get_stats()['total_products']}")
    print(f"   - Documents indexed: {rag_service.get_stats()['total_documents']}")
    print(f"   - Embedding model: {embedding_service.model_name}")
    print("="*60 + "\n")
    
    yield
    
    print("\n🛑 Shutting down services...")


# Create FastAPI app
app = FastAPI(
    title="AI Shopping Assistant API",
    description="Semantic search, RAG, and recommendations for e-commerce",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🛍️ AI Personal Shopping & Knowledge Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "search": "/api/search",
            "chat": "/api/chat",
            "recommend": "/api/recommend",
            "products": "/api/products",
            "health": "/api/health"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "embedding": embedding_service is not None,
            "search": search_service is not None,
            "rag": rag_service is not None,
            "recommendation": recommendation_service is not None
        },
        "stats": {
            "products": search_service.get_stats() if search_service else {},
            "documents": rag_service.get_stats() if rag_service else {}
        }
    }


@app.post("/api/search", response_model=SearchResponse)
async def search_products(request: SearchRequest):
    """
    Semantic search for products
    
    Example:
        POST /api/search
        {
            "query": "clothes for rainy weather",
            "limit": 5
        }
    """
    try:
        products = search_service.search(
            query=request.query,
            limit=request.limit,
            category=request.category,
            min_price=request.min_price,
            max_price=request.max_price
        )
        
        return SearchResponse(
            query=request.query,
            results=products,
            total=len(products),
            semantic_matches=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    RAG-based question answering
    
    Example:
        POST /api/chat
        {
            "question": "How do I choose rain gear?",
            "context_limit": 3,
            "include_products": true
        }
    """
    try:
        answer, sources, related_products = rag_service.ask(
            question=request.question,
            context_limit=request.context_limit,
            include_products=request.include_products
        )
        
        return ChatResponse(
            question=request.question,
            answer=answer,
            sources=sources,
            related_products=[Product(**p) for p in related_products] if related_products else []
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@app.post("/api/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Get product recommendations based on similarity
    
    Examples:
        1. By product ID:
           POST /api/recommend
           {"product_id": "prod_005", "limit": 5}
        
        2. By product name:
           POST /api/recommend
           {"product_name": "black shirt", "limit": 5}
        
        3. By query:
           POST /api/recommend
           {"query": "casual comfortable clothing", "limit": 5}
    """
    try:
        recommendations, scores, basis = recommendation_service.recommend_similar_items(
            product_id=request.product_id,
            product_name=request.product_name,
            query=request.query,
            limit=request.limit
        )
        
        return RecommendationResponse(
            based_on=basis,
            recommendations=recommendations,
            similarity_scores=scores if scores else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation error: {str(e)}")


@app.get("/api/products", response_model=list[Product])
async def get_all_products():
    """Get all products in the catalog"""
    try:
        products = search_service.get_all_products()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")


@app.get("/api/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Get a specific product by ID"""
    try:
        product = search_service.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")


@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    return {
        "embedding_model": embedding_service.get_model_info(),
        "search": search_service.get_stats(),
        "rag": rag_service.get_stats(),
        "total_products": len(PRODUCTS),
        "total_documents": len(DOCUMENTS)
    }


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n🚀 Starting AI Shopping Assistant Backend Server\n")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
