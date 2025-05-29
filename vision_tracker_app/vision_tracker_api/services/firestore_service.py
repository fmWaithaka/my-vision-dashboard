import firebase_admin
from firebase_admin import credentials, firestore
from django.conf import settings
import logging
from google.protobuf.json_format import MessageToDict, ParseDict
import google.generativeai as genai 
from asgiref.sync import sync_to_async
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class FirestoreService:
    _instance = None
    _db = None

    def __new__(cls, *args, **kwargs):
        """
        Ensures a single instance of FirestoreService (Singleton pattern).
        Initializes the Firebase Admin SDK and Firestore client.
        """
        if cls._instance is None:
            cls._instance = super(FirestoreService, cls).__new__(cls, *args, **kwargs)
            try:
                # Check if the app is already initialized to prevent re-initialization errors
                if not firebase_admin._apps:
                    cred_path = getattr(settings, 'FIREBASE_ADMIN_SDK_PATH', None)
                    if not cred_path:
                        logger.error("FIREBASE_ADMIN_SDK_PATH not configured in Django settings.")
                        raise ValueError("Firebase Admin SDK path not configured. Please set FIREBASE_ADMIN_SDK_PATH in your Django settings.")
                    
                    cred = credentials.Certificate(cred_path)
                    firebase_admin.initialize_app(cred)
                    logger.info("Firebase Admin SDK initialized successfully.")
                else:
                    logger.info("Firebase Admin SDK already initialized.")
                
                cls._db = firestore.client()
                logger.info("Firestore client obtained successfully.")

            except ValueError as ve:
                logger.error(f"Configuration error for Firebase Admin SDK: {ve}")
                cls._db = None 
            except Exception as e:
                logger.exception("Failed to initialize Firebase Admin SDK or get Firestore client.")
                cls._db = None
        return cls._instance

    def get_db(self):
        """
        Returns the Firestore client instance.
        """
        if not self._db:
            logger.warning("Attempted to get Firestore client, but it's not initialized.")
        return self._db
        
    async def add_document(self, collection_name: str, doc_id: str, data: Dict[str, Any]) -> bool:
        """
        Adds a document to a specified Firestore collection.

        Args:
            collection_name (str): The name of the collection.
            doc_id (str): The ID of the document to add.
            data (Dict[str, Any]): The data to set for the document.

        Returns:
            bool: True if the document was added successfully, False otherwise.
        """
        if not self._db:
            logger.error("Firestore not initialized, cannot add document.")
            raise ConnectionError("Firestore service not available.")
        try:
            doc_ref = self._db.collection(collection_name).document(doc_id)
            await sync_to_async(doc_ref.set)(data)
            logger.debug(f"Document '{doc_id}' added to collection '{collection_name}'.")
            return True
        except Exception as e:
            logger.exception(f"Error adding document '{doc_id}' to '{collection_name}'.")
            return False

    async def get_document(self, collection_name: str, doc_id: str):
        """
        Retrieves a document from a specified Firestore collection.

        Args:
            collection_name (str): The name of the collection.
            doc_id (str): The ID of the document to retrieve.

        Returns:
            firebase_admin.firestore.DocumentSnapshot: The document snapshot if found, None otherwise.
        """
        if not self._db:
            logger.error("Firestore not initialized, cannot get document.")
            raise ConnectionError("Firestore service not available.")
        try:
            doc_ref = self._db.collection(collection_name).document(doc_id)
            doc_snapshot = await sync_to_async(doc_ref.get)()
            logger.debug(f"Document '{doc_id}' retrieved from collection '{collection_name}'. Exists: {doc_snapshot.exists}")
            return doc_snapshot
        except Exception as e:
            logger.exception(f"Error getting document '{doc_id}' from '{collection_name}'.")
            return None
        
    ## Conversation History Management

    async def get_conversation_history(self, conversation_id: str) -> List[genai.protos.Content]:
        """
        Retrieves and deserializes the message history for a given conversation_id from Firestore.
        This method converts stored dictionary representations back into genai.protos.Content objects.

        Args:
            conversation_id (str): The ID of the conversation to retrieve history for.

        Returns:
            List[genai.protos.Content]: A list of Content objects representing the conversation history.
                                        Returns an empty list if no history is found or on error.
        """
        if not self._db:
            logger.error("Firestore not initialized, cannot get conversation history.")
            raise ConnectionError("Firestore service not available.")
        
        try:
            doc_ref = self._db.collection('conversations').document(conversation_id)
            doc_snapshot = await sync_to_async(doc_ref.get)()

            if doc_snapshot.exists:
                raw_history_data = doc_snapshot.to_dict()
                message_dicts = raw_history_data.get('messages', [])
                
                deserialized_history = []
                for msg_dict in message_dicts:
                    content_message = genai.protos.Content()
                    try:
                        # ParseDict populates the message object from a dictionary
                        ParseDict(js_dict=msg_dict, message=content_message)
                        deserialized_history.append(content_message)
                    except Exception as e:
                        logger.error(f"Failed to deserialize message: {msg_dict} for conversation '{conversation_id}'. Error: {e}")
                        # Decide how to handle corrupted messages: skip or raise?
                        # For robustness, we'll skip the corrupted message here.
                        continue
                        
                logger.debug(f"Retrieved and deserialized {len(deserialized_history)} messages for conversation '{conversation_id}'.")
                return deserialized_history
            else:
                logger.debug(f"No history found for conversation '{conversation_id}'. Returning empty list.")
                return []
        except ConnectionError:
            # Re-raise ConnectionError as it indicates a service availability issue
            raise
        except Exception as e:
            logger.exception(f"Error retrieving or deserializing history for conversation '{conversation_id}'.")
            return []

    async def save_conversation_history(self, conversation_id: str, history: List[genai.protos.Content]) -> bool:
        """
        Serializes and saves the complete message history for a conversation to Firestore.
        This method converts genai.protos.Content objects into a serializable dictionary format for storage.

        Args:
            conversation_id (str): The ID of the conversation.
            history (List[genai.protos.Content]): The list of Content objects representing the conversation.

        Returns:
            bool: True if the history was saved successfully, False otherwise.
        """
        if not self._db:
            logger.error("Firestore not initialized, cannot save conversation history.")
            raise ConnectionError("Firestore service not available.")

        try:
            serializable_history = []
            for content_message in history:
                if not isinstance(content_message, genai.protos.Content):
                    logger.warning(f"Skipping non-Content object in history for conversation '{conversation_id}': {type(content_message)}")
                    continue
                try:
                    # MessageToDict converts the protobuf message to a dictionary
                    # preserving_proto_field_name=True ensures field names match the proto definition
                    msg_dict = MessageToDict(message=content_message, preserving_proto_field_name=True)
                    serializable_history.append(msg_dict)
                except Exception as e:
                    logger.error(f"Failed to serialize message: {content_message} for conversation '{conversation_id}'. Error: {e}")
                    # Decide: skip this message or fail the entire save operation?
                    # Skipping offers more robustness against individual message corruption.
                    continue

            doc_ref = self._db.collection('conversations').document(conversation_id)
            # Using set with merge=True is robust as it creates the document if it doesn't exist
            # or updates the 'messages' field without affecting other potential fields.
            await sync_to_async(doc_ref.set)({'messages': serializable_history}, merge=True)
            logger.debug(f"Serialized and saved {len(serializable_history)} messages for conversation '{conversation_id}'.")
            return True
        except ConnectionError:
            # Re-raise ConnectionError for consistent service availability handling
            raise
        except Exception as e:
            logger.exception(f"Error serializing or saving history for conversation '{conversation_id}'.")
            return False

# Initialize the singleton instance when the module is imported
firestore_service = FirestoreService()