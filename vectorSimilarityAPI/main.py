from fastapi import FastAPI 
from vectorSimilarityAPI.core import ChromaClient
from vectorSimilarityAPI.models import QueryItem, DocumentItem, DocumentItems, IdItems

# Initialize FastAPI app 
app = FastAPI(
    title="ChromaDb API",
    description="API pour requêter la BD chroma par similarité",
    version="1.0.0"
)
chroma_client = ChromaClient()

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
@app.get("/query", summary="Retrouve les documents par similarité", tags=["Querying"])
async def query(queryItem: QueryItem):
    """
    Retourne les n_results documents les plus pertinents

    - **query**: Requête textuelle 
    - **n_results**: Nombre maximal de documents à retourner
    - **include**: Informations souhaitées incluses dans ['ids', 'embeddings', 'documents', 'metadatas', 'distances']
    """
    results = chroma_client.query(
        query=queryItem.query,
        n_results=queryItem.n_results,
        include=queryItem.include
    )
    return {
        "status": "success",
        "results": results
    }

# Work with one document
@app.post("/add_one_document", summary="Ajoute un document à la collection", tags=["Manage one document"])
async def add_one_document(documentItem: DocumentItem):
    """
    Ajoute un document à la collection

    - **document**: le document (texte)
    - **metadata**: autres attributs (peut être vide)
    - **id**: identifiant unique du document
    """
    chroma_client.addOneDocument(
        document=documentItem.document,
        metadata=documentItem.metadata,
        id=documentItem.id
    )
    return {
        "status": "success",
        "message": f"Successfully added the document with ID: {documentItem.id}"
    }

@app.put("/update_one_document", summary="Modifie un document de la collection par son id", tags=["Manage one document"])
async def update_one_document(documentItem: DocumentItem):
    """
    Modifie un document de la collection par son id

    - **document**: nouveau document (texte)
    - **metadata**: nouveaux attributs (peut être vide)
    - **id**: identifiant unique du document
    """
    chroma_client.updateOneDocument(
        document=documentItem.document,
        metadata=documentItem.metadata,
        id=documentItem.id
    )
    return {
        "status": "success",
        "message": f"Successfully updated the document with ID: {documentItem.id}"
    }

@app.put("/delete_one_document", summary="Supprime un document de la collection par son id", tags=["Manage one document"])
async def delete_one_document(id: str):
    """
    Supprime un document de la collection par son id

     - **id**: identifiant unique du document
    """
    chroma_client.deleteOneDocument(id=id)
    return {
        "status": "success",
        "message": f"Successfully deleted the document with ID: {id}"
    }


# Work with documents
@app.post("/add_documents", summary="Ajoute des documents à la collection", tags=["Manage documents"])
async def add_documents(documentItems: DocumentItems):
    """
    Ajoute des documents à la collection
    """
    chroma_client.addDocuments(
        documents=documentItems.documents,
        metadatas=documentItems.metadatas,
        ids=documentItems.ids
    )
    return {
        "status": "success",
        "message": f"Successfully added {len(documentItems.documents)} documents"
    }

@app.put("/update_documents", summary="Modifie des documents de la collection", tags=["Manage documents"])
async def update_documents(documentItems: DocumentItems):
    """
    Modifie des documents de la collection
    """
    chroma_client.updateDocuments(
        documents=documentItems.documents,
        metadatas=documentItems.metadatas,
        ids=documentItems.ids
    )
    return {
        "status": "success",
        "message": f"Successfully updated {len(documentItems.documents)} documents"
    }

@app.put("/delete_documents", summary="Supprime des documents de la collection", tags=["Manage documents"])
async def delete_documents(ids: IdItems):
    """
    Supprime des documents de la collection
    """
    chroma_client.deleteDocuments(ids=ids.ids)
    return {
        "status": "success",
        "message": f"Successfully deleted {len(ids.ids)} documents"
    }


# others
@app.get("/count_documents", summary="Retourne le nombre de documents présents", tags=["Others"])
async def count_documents():
    """
    Retourne le nombre de documents présents
    """
    count = chroma_client.getNumberOfDocuments()
    return {
        "status": "success",
        "message": f"total numbers of documents : {count}"
    }

@app.post("/reset", summary="Supprime la collection", tags=["Others"])
async def reset():
    """
    Supprime la collection
    """
    chroma_client.reset()
    return {
        "status": "success",
        "message": "Reset chroma-db"
    }


