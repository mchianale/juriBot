from pydantic import BaseModel, Field, model_validator
from typing import List

    
class DocumentItems(BaseModel):
    documents: List[str]

    @model_validator(mode='before')
    def check_document_items(cls, values):
        documents = values.get('documents', [])

        # Ensure none of the lists are empty
        if not documents:
            raise ValueError("Documents can be empty.")
        

        # Validate each element of the lists (each element in documents, ids, and metadatas)
        for doc in documents:
            # Here you can add specific validation for document, metadata, and id
            if not doc:
                raise ValueError("Each document must be non-empty.")
          
        return values
    
 