# for chroma
import chromadb
from chromadb.config import Settings

# other
import requests
from fastapi import HTTPException
import logging

logging.basicConfig(level=logging.INFO)

class ChromaClient:
    def __init__(self):
        """
            Init a chroma client, the vector collection and embedding model
        """
        # static parameters 
        self.collection_name = "droit"
        db_path = 'vectorSimilarityAPI/data'
        self.encoder_url = 'http://encoder-api:8000/encode'
        logging.info(f"ChromaClient --encoder api url : {self.encoder_url}")

        # setup chroma client
        self._chroma_client = chromadb.PersistentClient(
            path=db_path, settings=Settings(allow_reset=True, anonymized_telemetry=False)
        )
        logging.info("ChromaClient --load chroma_client")

        # setup collection 
        self._collection = self._chroma_client.get_or_create_collection(name=self.collection_name)
        logging.info(f"ChromaClient --load chroma collection {self.collection_name}")

       

    def _encode(self, documents : list):
        encode_data = {
            "documents" : documents
        }
        response = requests.get(self.encoder_url, json=encode_data)
        if response.status_code == 200:
            return response.json()['embeddings']
        else:
            raise HTTPException(status_code=500, detail=response.json()['detail'])
    
    # Manage one document
    def addOneDocument(self, document : str, metadata : dict, id : str):
        try:
            embedding = self._encode(documents=[document])[0]
            self._collection.add(embeddings=embedding, documents=document, metadatas=metadata, ids=id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    def updateOneDocument(self, document : str, metadata : dict, id : str):
        try:
            embedding = self._encode(documents=[document])[0]
            self._collection.update(embeddings=embedding, documents=document, metadatas=metadata, ids=id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    def deleteOneDocument(self, id : str):
        try:
            self._collection.delete(ids=id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    # manage several documents
    def addDocuments(self, documents : list, metadatas : list, ids : list):
        try:
            embeddings = self._encode(documents=documents)
            self._collection.add(embeddings=embeddings, documents=documents, metadatas=metadatas, ids=ids)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    def updateDocuments(self, documents : list, metadatas : list, ids : list):
        try:
            embeddings = self._encode(documents=documents)
            self._collection.update(embeddings=embeddings, documents=documents, metadatas=metadatas, ids=ids)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    def deleteDocuments(self, ids : list):
        try:
            self._collection.delete(ids=ids)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    # Query
    def query(self, query : str, n_results : int, include : list):
        try:
            query_embedding = self._encode(documents=[query])[0]
            return self._collection.query(
                query_embeddings=query_embedding,
                n_results=n_results,
                include=include #['embeddings', 'documents', 'metadatas', 'distances']
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    # Other
    def getNumberOfDocuments(self):
        try:
            return self._collection.count()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    def reset(self):
        try:
            self._chroma_client.reset()
            self._collection = self._chroma_client.get_or_create_collection(name=self.collection_name)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
        