from juriBot.core import JuriBot
from juriBot.models import ChatItem
from fastapi import FastAPI 
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import os 

# Initialize FastAPI app 
app = FastAPI(
    title="JuriBot API",
    description="API pour requêter l'agent mistral",
    version="1.0.0"
)

# init agent
load_dotenv()
n_results = 5
MISTRAL_API_KEY= os.environ['MISTRAL_API_KEY']
juriBot = JuriBot(mistral_model="open-mistral-nemo", api_key=MISTRAL_API_KEY, n_results=n_results)

@app.get("/health_check", summary="Vérification de santé", tags=["Monitoring"])
async def health_check():
    """
    Vérifie si l'application est en cours d'exécution et fonctionnelle.
    """
    return {
        "status": "success",
        "message": "Health check successful."
    }

# chat 
@app.get("/chat", summary="Appel de l'Agent", tags=["RAG"])
async def query(chatItem: ChatItem):
    """
    Appel de l'agent :
    1. Appelle une première fois le LLM pour effectuer un choix (appel d'outils ou réponse directe).
    2. En cas d'appel d'outils : ajoute au contexte les documents les plus pertinents.
    3. En conséquence de ce contexte, le LLM fournit une réponse finale.
    4. L'agent retourne l'ensemble des messages depuis la nouvelle requête utilisateur (y compris ceux générés par les outils).

    - **user_query** : Requête de l'utilisateur.
    - **history_messages** : Liste des messages précédents (incluant ceux de l'assistant et des outils). Cette liste peut être vide (cas one-shot).
    """
    return juriBot.chat(
        user_query=chatItem.user_query,
        history_messages=chatItem.history_messages
    )

# stream
"""
@app.get("/stream")
async def stream(chatItem: ChatItem):
    # Call the stream method from your class
    return StreamingResponse(juriBot.stream(
        user_query=chatItem.user_query,
        history_messages=chatItem.history_messages
    ))
"""