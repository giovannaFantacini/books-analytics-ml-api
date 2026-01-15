from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    preco: float = Field(..., ge=0, description="Preço do livro")
    disponibilidade: int = Field(..., ge=0, le=1, description="Disponibilidade (0 ou 1)")
    categoria: str = Field(..., description="Categoria do livro")
