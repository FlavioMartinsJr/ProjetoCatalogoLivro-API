from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class AvaliacaoUpdateSchemas(BaseModel):
    id: Optional[int] = None
    idLivro: Optional[str] = None
    tituloLivro: Optional[str] = None
    avaliacao: Optional[int] = None

    class Config:
        orm_mode = True

class AvaliacaoInsertSchemas(AvaliacaoUpdateSchemas):
    id: Optional[int] = None
    idLivro: Optional[str] = None
    tituloLivro: Optional[str] = None
    avaliacao: Optional[int] = None
    idLogin: Optional[int] = None

class AvaliacaoSchemas(BaseModel):
    id: Optional[int] = None
    idLivro: Optional[str] = None
    tituloLivro: Optional[str] = None
    avaliacao: Optional[int] = None
    dataCriacao: Optional[datetime] = None
    dataAlteracao: Optional[datetime] = None
    idLogin: Optional[int] = None

    class Config:
        orm_mode = True

class AvaliacaoSelectSchemas(AvaliacaoSchemas):
    id: Optional[int] = None
    idLivro: Optional[str] = None
    tituloLivro: Optional[str] = None
    avaliacao: Optional[int] = None
    dataCriacao: Optional[datetime] = None
    dataAlteracao: Optional[datetime] = None
    idLogin: Optional[int] = None
    email: Optional[str] = None


  
   