# 🏗️ System Architecture

## Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                         (Next.js App)                           │
│  ┌──────────┐    ┌──────────┐    ┌─────────────────────┐      │
│  │  Search  │    │   Chat   │    │  Recommendations    │      │
│  │   Tab    │    │   Tab    │    │       Tab           │      │
│  └──────────┘    └──────────┘    └─────────────────────┘      │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST API
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API Endpoints                                            │  │
│  │  • POST /api/search      - Semantic search               │  │
│  │  • POST /api/chat        - RAG Q&A                       │  │
│  │  • POST /api/recommend   - Similar products              │  │
│  │  • GET  /api/products    - All products                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐    │
│  │  Search     │  │  RAG         │  │  Recommendation    │    │
│  │  Service    │  │  Service     │  │  Service           │    │
│  └─────────────┘  └──────────────┘  └────────────────────┘    │
│         │                │                     │                │
│         └────────────────┴─────────────────────┘                │
│                          │                                       │
│                ┌─────────▼─────────┐                            │
│                │ Embedding Service  │                            │
│                │ (Sentence Trans.)  │                            │
│                └─────────┬─────────┘                            │
│                          │                                       │
└──────────────────────────┼───────────────────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────┐
        │         ChromaDB Vector Store         │
        │  ┌──────────────┐  ┌──────────────┐ │
        │  │  Products    │  │  Documents   │ │
        │  │  Collection  │  │  Collection  │ │
        │  │              │  │              │ │
        │  │  • IDs       │  │  • IDs       │ │
        │  │  • Vectors   │  │  • Vectors   │ │
        │  │  • Metadata  │  │  • Metadata  │ │
        │  └──────────────┘  └──────────────┘ │
        └──────────────────────────────────────┘
```

## Component Details

### 1. Frontend (Next.js)
**File**: `frontend/app/page.tsx`
- **Search Interface**: Natural language product search
- **Chat Interface**: RAG-based Q&A with knowledge base
- **Recommendations**: Similar product suggestions
- **Features**:
  - Framer Motion animations
  - Glassmorphism design
  - Real-time updates
  - Responsive layout

### 2. Backend Services

#### Embedding Service
**File**: `backend/services/embedding_service.py`
- Model: `all-MiniLM-L6-v2` (384-dimensional vectors)
- Converts text → vector embeddings
- Computes cosine similarity
- Batch processing support

#### Search Service
**File**: `backend/services/search_service.py`
- Indexes products with embeddings
- Semantic search using vector similarity
- Supports filters (category, price range)
- ChromaDB integration

#### RAG Service
**File**: `backend/services/rag_service.py`
- Indexes knowledge base documents
- Retrieves relevant context for questions
- Generates answers using context
- Returns sources and related products

#### Recommendation Service
**File**: `backend/services/recommendation_service.py`
- Finds similar products by ID
- Finds similar products by name
- Finds products by query
- Returns similarity scores

### 3. Vector Database (ChromaDB)
- **Collections**:
  - `products`: 15 products with embeddings
  - `documents`: 6 knowledge base docs with embeddings
- **Storage**: Persistent on disk (`chroma_db/`)
- **Features**:
  - Fast similarity search
  - Metadata filtering
  - Automatic indexing

## Data Flow

### Semantic Search Flow
```
User Query
    ↓
Generate Embedding (384-dim vector)
    ↓
Search Products Collection (ChromaDB)
    ↓
Rank by Cosine Similarity
    ↓
Apply Filters (category, price)
    ↓
Return Top N Products
```

### RAG Flow
```
User Question
    ↓
Generate Question Embedding
    ↓
Search Documents Collection
    ↓
Retrieve Top K Relevant Documents
    ↓
Combine Context
    ↓
Generate Answer
    ↓
Include Related Products (optional)
    ↓
Return Answer + Sources + Products
```

### Recommendation Flow
```
Product ID/Name/Query
    ↓
Get Product Embedding
    ↓
Find Similar Embeddings (ChromaDB)
    ↓
Compute Similarity Scores
    ↓
Rank by Similarity
    ↓
Return Top N Similar Products
```

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Sentence Transformers**: Embedding generation
- **ChromaDB**: Vector database
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type safety
- **Tailwind CSS**: Utility-first styling
- **Framer Motion**: Animation library
- **Axios**: HTTP client

### AI/ML
- **Model**: all-MiniLM-L6-v2
  - Size: ~80MB
  - Speed: ~3000 sentences/second
  - Dimension: 384
- **Similarity**: Cosine similarity
- **Search**: Approximate Nearest Neighbor (ANN)

## Performance Characteristics

### Embedding Generation
- **Speed**: ~3000 sentences/second on CPU
- **Latency**: ~5-10ms per query
- **Memory**: ~200MB model in RAM

### Vector Search
- **Speed**: <10ms for 1000 products
- **Scalability**: Logarithmic with collection size
- **Accuracy**: High precision with 384-dim vectors

### API Response Times
- **Search**: 50-100ms
- **Chat**: 100-200ms
- **Recommendations**: 30-50ms

## Scalability Considerations

### Current Setup (Demo)
- 15 products
- 6 documents
- In-memory ChromaDB
- Single instance

### Production Ready
- 1000s of products
- 100s of documents
- Persistent ChromaDB
- Load balanced backend

### Future Enhancements
- Add caching layer (Redis)
- Use GPU for embeddings
- Implement LLM for better answers
- Add user personalization
- A/B testing framework
