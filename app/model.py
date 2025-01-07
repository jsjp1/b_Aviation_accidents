from pydantic import BaseModel

class DescriptionUpdate(BaseModel):
  doc_id: str
  description: str