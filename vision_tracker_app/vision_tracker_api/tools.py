# vision_tracker_app/vision_tracker_api/tools.py

import logging
from .services.chroma_service import chroma_service

# Configure a logger for the tools module
logger = logging.getLogger(__name__)

def recall_memories(query: str, n_results: int = 5) -> str:
    """
    Searches archival memory (ChromaDB) for past conversations, facts, or visions
    related to the user's query.

    Args:
        query: The string to search for in the memory database. The LLM should
               generate a query that it thinks will find the most relevant memories.
        n_results: The maximum number of memories to retrieve.

    Returns:
        A formatted string containing the retrieved memories and their relevance scores,
        or a message indicating that no relevant memories were found. This string is
        intended to be read by the LLM.
    """
    logger.info(f"Executing recall_memories with query: '{query}' and requested n_results: {n_results}")
    if not query:
        logger.warning("recall_memories called with no query provided.")
        return "No query was provided. Cannot search for memories."

    try:
        # Fix 1: Ensure n_results is an integer, as ChromaDB (or your service) expects it.
        # The Generative AI model might provide it as a float (e.g., 5.0).
        n_results_int = int(n_results)
        
        # Fix 2: Assume chroma_service.query_memories returns a list of dictionaries,
        # e.g., [{'document': '...', 'distance': ...}, {'document': '...', 'distance': ...}]
        # This addresses the 'list' object has no attribute 'get' error.
        relevant_memories_list = chroma_service.query_memories(query, n_results_int)
        logger.debug(f"Raw relevant_memories from ChromaDB service: {relevant_memories_list}")

        if not relevant_memories_list:
            logger.info(f"No relevant memories found in ChromaDB for query: '{query}'.")
            return "No relevant memories were found for that query."

        # Format the results into a string that is easy for the LLM to understand.
        context_str = "Observation: The following relevant memories were found:\n"
        
        # Iterate directly over the list of memory dictionaries
        for i, mem_dict in enumerate(relevant_memories_list):
            # Access 'document' and 'distance' keys from each dictionary
            doc_content = mem_dict.get('document', 'N/A (missing document content)')
            dist_score = mem_dict.get('distance', 999.99) # Use a high score for missing distances
            context_str += f"- Memory {i+1} (Score: {dist_score:.2f}): {doc_content}\n"
        
        logger.info(f"Found and formatted {len(relevant_memories_list)} memories for query: '{query}'.")
        return context_str

    except Exception as e:
        logger.error(f"An error occurred in recall_memories while querying ChromaDB: {e}", exc_info=True)
        return f"An error occurred while trying to search for memories: {e}"