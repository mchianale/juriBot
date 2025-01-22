# for embedding
from sentence_transformers import SentenceTransformer
import torch

# other
from fastapi import HTTPException
import logging

logging.basicConfig(level=logging.INFO)

class EncoderClient:
    def __init__(self, model_config : dict):
        # setup model
        model_name =  model_config['model_name']
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self._model = SentenceTransformer(model_name)
        self._model.to(self.device)
        logging.info(f"EncoderClient --load embedding model {model_name}, running on {self.device}")

    def encode(self, documents : list):
        try:
            embeddings = self._model.encode(documents).tolist()
            return embeddings
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


