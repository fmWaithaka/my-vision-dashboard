# vision_tracker_app/vision_tracker_api/services/chroma_service.py

import chromadb
import os
from .gemini_service import generate_embedding # Import our embedding function

# Define a consistent path for ChromaDB storage
# BASE_DIR should be imported carefully, or passed in
# For now, let's assume a 'chroma_db' directory in the project root
# We can refine this path later if needed.
CHROMADB_PERSIST_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'chroma_db')

class ChromaService:
    _instance = None
    _collection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChromaService, cls).__new__(cls)
            cls._instance._initialize_client()
        return cls._instance

    def _initialize_client(self):
        """Initializes the ChromaDB client and gets/creates the collection."""
        print(f"DEBUG: Initializing ChromaDB client at: {CHROMADB_PERSIST_PATH}")
        # Ensure the directory exists
        os.makedirs(CHROMADB_PERSIST_PATH, exist_ok=True)
        self.client = chromadb.PersistentClient(path=CHROMADB_PERSIST_PATH)
        # Define your collection name - can be dynamic later if needed per user
        self.collection_name = "vision_tracker_memories"
        self._collection = self.client.get_or_create_collection(name=self.collection_name)
        print(f"DEBUG: ChromaDB collection '{self.collection_name}' ready.")

    def add_memory(self, doc_id: str, document_text: str, metadata: dict = None):
        """
        Adds a single document to the ChromaDB collection.
        Generates embedding using Gemini.
        """
        if not document_text.strip():
            print("Warning: Attempted to add empty document to ChromaDB.")
            return

        try:
            embedding = generate_embedding(document_text)
            if not embedding:
                print(f"Error: Could not generate embedding for document ID {doc_id}.")
                return

            self._collection.add(
                documents=[document_text],
                metadatas=[metadata if metadata is not None else {}],
                embeddings=[embedding],
                ids=[doc_id]
            )
            print(f"DEBUG: Document ID '{doc_id}' added to ChromaDB.")
        except Exception as e:
            print(f"ERROR: Failed to add document ID '{doc_id}' to ChromaDB: {e}")

    def query_memories(self, query_text: str, n_results: int = 5) -> list:
        """
        Queries the ChromaDB collection for similar documents.
        Generates embedding for the query using Gemini.
        Returns a list of dictionaries with 'id', 'document', 'metadata', 'distance'.
        """
        if not query_text.strip():
            print("Warning: Attempted to query ChromaDB with empty text.")
            return []

        try:
            query_embedding = generate_embedding(query_text)
            if not query_embedding:
                print(f"Error: Could not generate embedding for query '{query_text}'.")
                return []

            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )

            # Format results for easier use
            formatted_results = []
            if results and results['ids']:
                for i in range(len(results['ids'][0])):
                    formatted_results.append({
                        'id': results['ids'][0][i],
                        'document': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i] if results['metadatas'][0] else {},
                        'distance': results['distances'][0][i] if results['distances'][0] else None
                    })
            print(f"DEBUG: Queried ChromaDB for '{query_text}', found {len(formatted_results)} results.")
            return formatted_results
        except Exception as e:
            print(f"ERROR: Failed to query ChromaDB: {e}")
            return []

# Make it a singleton to ensure only one client instance
chroma_service = ChromaService()