"""RAG (Retrieval-Augmented Generation) service for answering questions"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import chromadb
from services.embedding_service import EmbeddingService
from services.search_service import SearchService
import json
import os


class RAGService:
    """Service for RAG-based question answering using document knowledge base"""
    
    def __init__(
        self,
        embedding_service: EmbeddingService,
        search_service: SearchService,
        collection_name: str = "documents"
    ):
        """
        Initialize RAG service
        
        Args:
            embedding_service: Instance of EmbeddingService
            search_service: Instance of SearchService for product context
            collection_name: Name of the ChromaDB collection for documents
        """
        self.embedding_service = embedding_service
        self.search_service = search_service
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

        print(f"✓ RAG service initialized with {self.collection.count()} documents")
    
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

        print(f"Indexing {len(documents)} documents...")

        ids = []
        embeddings = []
        metadatas = []
        documents_payload = []

        for doc in documents:
            # Create searchable text from document
            searchable_text = f"{doc['title']} {doc['content']}"
            ids.append(doc['id'])
            embeddings.append(self.embedding_service.generate_embedding(searchable_text))
            metadatas.append({
                "title": doc['title'],
                "doc_type": doc['doc_type'],
                "category": doc.get('category', ''),
                "content": doc['content'][:1000]  # Limit content length in metadata
            })
            documents_payload.append(searchable_text)
        
        # Upsert vectors in batches
        batch_size = 100
        for i in range(0, len(ids), batch_size):
            self.collection.upsert(
                ids=ids[i:i + batch_size],
                embeddings=embeddings[i:i + batch_size],
                metadatas=metadatas[i:i + batch_size],
                documents=documents_payload[i:i + batch_size]
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
        question_embedding = self.embedding_service.generate_embedding(question)

        results = self.collection.query(
            query_embeddings=[question_embedding],
            n_results=limit,
            include=["metadatas", "distances"]
        )

        contexts = []
        ids = results.get("ids", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for doc_id, metadata, distance in zip(ids, metadatas, distances):
            doc_data = {
                "id": doc_id,
                "title": metadata['title'],
                "content": metadata['content'],
                "doc_type": metadata['doc_type'],
                "category": metadata.get('category', ''),
                "relevance_score": 1 - float(distance) if distance is not None else 0.0
            }
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
            "total_documents": self.collection.count(),
            "collection_name": self.collection_name,
            "vector_store": "chroma",
            "persist_directory": self.persist_directory,
            "embedding_model": self.embedding_service.model_name
        }
