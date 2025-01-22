from pydantic import BaseModel, Field, model_validator
from typing import List

# Define allowed values for the 'include' field
ALLOWED_INCLUDE = ['ids', 'embeddings', 'documents', 'metadatas', 'distances']

class ChatItem(BaseModel):
    user_query: str
    history_messages: List[dict] = Field(default_factory=lambda: [])  

    @model_validator(mode='before')
    def check_fields(cls, values):
        # Ensure at least query is provided
        if not values.get('user_query'):
            raise ValueError("Query cannot be empty")
        
        return values
 