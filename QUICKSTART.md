# 🚀 Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn

## Setup Instructions

### Option 1: Automated Setup (Windows)

#### Backend
```bash
cd backend
setup.bat
run.bat
```

#### Frontend (in a new terminal)
```bash
cd frontend
setup.bat
run.bat
```

### Option 2: Manual Setup

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

The backend will start on **http://localhost:8000**

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will start on **http://localhost:3000**

## 🎯 Using the Application

### 1. Semantic Search
- Navigate to the **Search** tab
- Enter natural language queries like:
  - "clothes for rainy weather"
  - "black shirt"
  - "running shoes"
  - "fitness gear"
- View results ranked by semantic similarity

### 2. Chat with AI Assistant
- Navigate to the **Chat** tab
- Ask questions about products:
  - "How do I choose rain gear?"
  - "What makes a good capsule wardrobe?"
  - "Best fitness gear for beginners?"
- Get answers from the knowledge base with sources

### 3. Get Recommendations
- Click on any product from search results
- Automatically switch to **Recommendations** tab
- See similar products based on AI embeddings

## 🏗️ Architecture

### Backend (FastAPI)
- **Port**: 8000
- **Embedding Model**: all-MiniLM-L6-v2 (Sentence Transformers)
- **Vector DB**: ChromaDB
- **Features**:
  - Semantic search with filters
  - RAG-based Q&A
  - Similarity-based recommendations

### Frontend (Next.js)
- **Port**: 3000
- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS + Custom Animations
- **Features**:
  - Beautiful dark theme with glassmorphism
  - Smooth animations with Framer Motion
  - Responsive design
  - Real-time search and chat

## 📡 API Endpoints

### Search Products
```
POST http://localhost:8000/api/search
{
  "query": "rain jacket",
  "limit": 10
}
```

### Chat
```
POST http://localhost:8000/api/chat
{
  "question": "How to choose rain gear?",
  "context_limit": 3,
  "include_products": true
}
```

### Recommendations
```
POST http://localhost:8000/api/recommend
{
  "product_id": "prod_005",
  "limit": 5
}
```

### Get All Products
```
GET http://localhost:8000/api/products
```

### Health Check
```
GET http://localhost:8000/api/health
```

## 🔧 Troubleshooting

### Backend Issues
- **Port already in use**: Change port in `backend/app.py`
- **Module not found**: Ensure virtual environment is activated and dependencies are installed
- **ChromaDB errors**: Delete `chroma_db` folder and restart

### Frontend Issues
- **API connection errors**: Ensure backend is running on port 8000
- **Dependencies errors**: Delete `node_modules` and run `npm install` again
- **Port 3000 in use**: Kill the process or change port in `package.json`

## 📊 Sample Data

The application includes:
- **15 products** across categories (Outerwear, Footwear, Apparel, Electronics, etc.)
- **6 knowledge base documents** (guides, FAQs, tutorials)

You can add more products and documents by editing:
- `backend/data/sample_data.py`

## 🎨 Customization

### Add More Products
Edit `backend/data/sample_data.py` and add to `PRODUCTS` list

### Add More Documents
Edit `backend/data/sample_data.py` and add to `DOCUMENTS` list

### Change Embedding Model
Edit `backend/app.py` and change model name in initialization:
```python
embedding_service = EmbeddingService(model_name='all-mpnet-base-v2')
```

### Modify UI Theme
Edit `frontend/tailwind.config.ts` and `frontend/app/globals.css`

## 🚀 Production Deployment

### Backend
```bash
cd backend
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend
```bash
cd frontend
npm run build
npm start
```

---

**Enjoy your AI Shopping Assistant! 🛍️✨**
