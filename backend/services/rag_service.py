"""RAG (Retrieval-Augmented Generation) service for answering questions"""

from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Any, Optional
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
        index_name: str = "documents"
    ):
        """
        Initialize RAG service
        
        Args:
            embedding_service: Instance of EmbeddingService
            search_service: Instance of SearchService for product context
            index_name: Name of the Pinecone index for documents
        """
        self.embedding_service = embedding_service
        self.search_service = search_service
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
        print(f"✓ RAG service initialized with {stats['total_vector_count']} documents")
    
    def index_documents(self, documents: List[Dict[str, Any]]) -> int:
        """
        Index documents in Pinecone with embeddings
        
        Args:
            documents: List of document dictionaries to index
            
        Returns:
            Number of documents indexed
        """
        if not documents:
            return 0
        
        # Check if documents already exist
        stats = self.index.describe_index_stats()
        existing_count = stats['total_vector_count']
        if existing_count >= len(documents):
            print(f"Documents already indexed ({existing_count} documents)")
            return existing_count
        
        print(f"Indexing {len(documents)} documents...")
        
        vectors = []
        
        for doc in documents:
            # Create searchable text from document
            searchable_text = f"{doc['title']} {doc['content']}"
            
            # Generate embedding
            embedding = self.embedding_service.generate_embedding(searchable_text)
            
            # Prepare metadata
            metadata = {
                "title": doc['title'],
                "doc_type": doc['doc_type'],
                "category": doc.get('category', ''),
                "content": doc['content'][:1000]  # Limit content length in metadata
            }
            
            vectors.append({
                "id": doc['id'],
                "values": embedding,
                "metadata": metadata
            })
        
        # Upsert vectors in batches
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            self.index.upsert(vectors=batch)
        
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
        results = self.index.query(
            vector=question_embedding,
            top_k=limit,
            include_metadata=True
        )
        
        contexts = []
        for match in results['matches']:
            metadata = match['metadata']
            doc_data = {
                "id": match['id'],
                "title": metadata['title'],
                "content": metadata['content'],
                "doc_type": metadata['doc_type'],
                "category": metadata.get('category', ''),
                "relevance_score": match['score']
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
        stats = self.index.describe_index_stats()
        return {
            "total_documents": stats['total_vector_count'],
            "index_name": self.index_name,
            "embedding_model": self.embedding_service.model_name
        }
