from pydantic import BaseModel, Field, model_validator
from typing import List

# Define allowed values for the 'include' field
ALLOWED_INCLUDE = ['ids', 'embeddings', 'documents', 'metadatas', 'distances']

class QueryItem(BaseModel):
    query: str
    n_results: int = Field(1, ge=0, description="Value must be greater than or equal to 0")
    include: List[str] = Field(default_factory=lambda: ['documents', 'metadatas'])  # Default to ['documents', 'metadatas']

    @model_validator(mode='before')
    def check_fields(cls, values):
        # Ensure at least query is provided
        if not values.get('query'):
            raise ValueError("Query cannot be empty")
        
        # Ensure 'include' only contains valid options
        include_list = values.get('include', [])
        invalid_items = [item for item in include_list if item not in ALLOWED_INCLUDE]
        if invalid_items:
            raise ValueError(f"Invalid items in 'include': {', '.join(invalid_items)}")
        
        return values

class DocumentItem(BaseModel):
    document: str
    metadata: dict = Field(default_factory=dict)  # Default to an empty dictionary
    id: str

    @model_validator(mode='before')
    def check_fields(cls, values):
        # Ensure at least 'document' is provided
        if not values.get('document'):
            raise ValueError("Document cannot be empty")
        
        # Ensure 'id' is provided
        if not values.get('id'):
            raise ValueError("Id cannot be empty")
        
        return values
    
class DocumentItems(BaseModel):
    documents: List[str]
    metadatas: List[dict]
    ids: List[str]

    @model_validator(mode='before')
    def check_document_items(cls, values):
        documents = values.get('documents', [])
        metadatas = values.get('metadatas', [])
        ids = values.get('ids', [])
        
        # Ensure none of the lists are empty
        if not documents or not metadatas or not ids:
            raise ValueError("None of the lists (documents, metadatas, ids) can be empty.")
        
        # Ensure all lists have the same length
        if not (len(documents) == len(metadatas) == len(ids)):
            raise ValueError("The lists 'documents', 'metadatas', and 'ids' must have the same length.")

        # Validate each element of the lists (each element in documents, ids, and metadatas)
        for doc, metadata, doc_id in zip(documents, metadatas, ids):
            # Here you can add specific validation for document, metadata, and id
            if not doc or not doc_id:
                raise ValueError("Each document and id must be non-empty.")
            if not isinstance(metadata, dict):
                raise ValueError("Each metadata must be a dictionary.")

        return values
    

class IdItems(BaseModel):
    ids: List[str]

    @model_validator(mode='before')
    def check_document_items(cls, values):
        ids = values.get('ids')
        
        # Ensure the 'ids' field exists and is not empty
        if not ids or not isinstance(ids, list) or len(ids) == 0:
            raise ValueError("The 'ids' field must be a non-empty list of strings.")
        
        # Validate each element in the 'ids' list
        for id in ids:
            if not isinstance(id, str) or not id.strip():
                raise ValueError("Each 'id' must be a non-empty string.")
        
        return values
        