"""RAG (Retrieval-Augmented Generation) service for answering questions"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from services.embedding_service import EmbeddingService
from services.search_service import SearchService
import json


class RAGService:
    """Service for RAG-based question answering using document knowledge base"""
    
    def __init__(
        self,
        embedding_service: EmbeddingService,
        search_service: SearchService,
        persist_directory: str = "./chroma_db"
    ):
        """
        Initialize RAG service
        
        Args:
            embedding_service: Instance of EmbeddingService
            search_service: Instance of SearchService for product context
            persist_directory: Directory to persist ChromaDB data
        """
        self.embedding_service = embedding_service
        self.search_service = search_service
        
        # Initialize ChromaDB client (reuse if exists)
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Get or create collection for documents
        self.documents_collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"description": "Knowledge base documents"}
        )
        
        print(f"✓ RAG service initialized with {self.documents_collection.count()} documents")
    
    def index_documents(self, documents: List[Dict[str, Any]]) -> int:
        """
        Index documents in ChromaDB with embeddings
        
        Args:
            documents: List of document dictionaries to index
            
        Returns:
            Number of documents indexed
        """
        if not documents:
            return 0
        
        # Check if documents already exist
        existing_count = self.documents_collection.count()
        if existing_count >= len(documents):
            print(f"Documents already indexed ({existing_count} documents)")
            return existing_count
        
        print(f"Indexing {len(documents)} documents...")
        
        ids = []
        embeddings = []
        metadatas = []
        doc_texts = []
        
        for doc in documents:
            # Create searchable text from document
            searchable_text = f"{doc['title']} {doc['content']}"
            
            # Generate embedding
            embedding = self.embedding_service.generate_embedding(searchable_text)
            
            ids.append(doc['id'])
            embeddings.append(embedding)
            doc_texts.append(doc['content'])
            metadatas.append({
                "title": doc['title'],
                "doc_type": doc['doc_type'],
                "category": doc.get('category', ''),
                "document_json": json.dumps(doc)
            })
        
        # Add to collection
        self.documents_collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=doc_texts
        )
        
        print(f"✓ Indexed {len(documents)} documents successfully")
        return len(documents)
    
    def retrieve_context(self, question: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a question
        
        Args:
            question: User's question
            limit: Number of documents to retrieve
            
        Returns:
            List of relevant document dictionaries with metadata
        """
        # Generate question embedding
        question_embedding = self.embedding_service.generate_embedding(question)
        
        # Search for relevant documents
        results = self.documents_collection.query(
            query_embeddings=[question_embedding],
            n_results=limit
        )
        
        contexts = []
        if results['ids'] and results['ids'][0]:
            for i, metadata in enumerate(results['metadatas'][0]):
                doc_data = json.loads(metadata['document_json'])
                doc_data['relevance_score'] = 1 - results['distances'][0][i]
                contexts.append(doc_data)
        
        return contexts
    
    def generate_answer(
        self,
        question: str,
        context_limit: int = 3,
        include_products: bool = True
    ) -> Dict[str, Any]:
        """
        Generate answer to a question using RAG
        
        Args:
            question: User's question
            context_limit: Number of documents to use as context
            include_products: Whether to include related products
            
        Returns:
            Dictionary with answer, sources, and optional products
        """
        # Retrieve relevant documents
        contexts = self.retrieve_context(question, limit=context_limit)
        
        # Build answer from contexts
        if not contexts:
            answer = "I don't have specific information about that in my knowledge base. Could you rephrase your question or ask about products, rain gear, fashion, fitness, or tech accessories?"
            sources = []
        else:
            # Create answer by combining relevant context
            answer_parts = []
            sources = []
            
            for ctx in contexts:
                answer_parts.append(ctx['content'])
                sources.append({
                    "title": ctx['title'],
                    "type": ctx['doc_type'],
                    "category": ctx.get('category', ''),
                    "relevance": ctx.get('relevance_score', 0)
                })
            
            # Synthesize answer (in a real system, this would use an LLM)
            # For now, we'll provide the most relevant context
            answer = f"Based on our knowledge base:\n\n{contexts[0]['content']}"
            
            if len(contexts) > 1:
                answer += f"\n\nAdditional information: {contexts[1]['title']}"
        
        result = {
            "question": question,
            "answer": answer,
            "sources": sources,
            "related_products": []
        }
        
        # Optionally include related products
        if include_products:
            products = self.search_service.search(query=question, limit=3)
            result["related_products"] = [p.dict() for p in products]
        
        return result
    
    def ask(
        self,
        question: str,
        context_limit: int = 3,
        include_products: bool = True
    ) -> tuple[str, List[Dict], List[Any]]:
        """
        Simplified question answering method
        
        Args:
            question: User's question
            context_limit: Number of context documents to use
            include_products: Whether to include related products
            
        Returns:
            Tuple of (answer, sources, related_products)
        """
        result = self.generate_answer(question, context_limit, include_products)
        return result["answer"], result["sources"], result["related_products"]
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get RAG service statistics
        
        Returns:
            Dictionary with statistics
        """
        return {
            "total_documents": self.documents_collection.count(),
            "collection_name": self.documents_collection.name,
            "embedding_model": self.embedding_service.model_name
        }
