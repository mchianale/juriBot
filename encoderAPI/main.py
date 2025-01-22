from fastapi import FastAPI 
from encoderAPI.core import EncoderClient
from encoderAPI.models import DocumentItems
import json
# load model config
model_config = json.load(open('encoderAPI/model_config.json', encoding='utf-8'))
# Initialize FastAPI app 
app = FastAPI(
    title="Encoder API",
    description="API pour générer des embeddings à partir de documents. Fournit des endpoints pour vérifier la santé du service et encoder des documents.",
    version="1.0.0"
)
encoderClient = EncoderClient(model_config=model_config)

@app.get("/health_check", summary="Vérification de santé", tags=["Monitoring"])
async def health_check():
    """
    Vérifie si l'application est en cours d'exécution et fonctionnelle.
    """
    return {
        "status": "success",
        "message": "Health check successful."
    }

# Query
@app.get(
    "/encode",
    summary="Créer des embeddings",
    tags=["Encodage"]
)
async def encode(documentItems: DocumentItems):
    """
    Génère des embeddings à partir d'une liste de documents textuels.

    - **documents**: Une liste de chaînes de caractères contenant les textes à encoder.
    """
    results = encoderClient.encode(
        documents=documentItems.documents
    )
    return {
        "status": "success",
        "embeddings": results
    }