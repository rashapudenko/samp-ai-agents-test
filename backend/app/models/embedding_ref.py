from pydantic import BaseModel, Field
import uuid

class EmbeddingRef(BaseModel):
    """Reference between a vulnerability and its vector embedding."""
    vulnerability_id: str
    vector_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create an embedding reference from a dictionary."""
        return cls(**data)
