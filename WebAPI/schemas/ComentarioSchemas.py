from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ComentarioUpdateSchemas(BaseModel):
    id: Optional[int] = None
    idLivro: Optional[str] = None
    tituloLivro: Optional[str] = None
    descricao: Optional[str] = None

    class Config:
        orm_mode = True

class ComentarioInsertSchemas(ComentarioUpdateSchemas):
    id: Optional[int] = None
    idLivro: Optional[str] = None
    tituloLivro: Optional[str] = None
    descricao: Optional[str] = None
    idLogin: Optional[int] = None

class ComentarioSchemas(BaseModel):
    id: Optional[int] = None
    idLivro: Optional[str] = None
    tituloLivro: Optional[str] = None
    descricao: Optional[str] = None
    dataCriacao: Optional[datetime] = None
    dataAlteracao: Optional[datetime] = None
    idLogin: Optional[int] = None

    class Config:
        orm_mode = True

class ComentarioSelectSchemas(ComentarioSchemas):
    id: Optional[int] = None
    idLivro: Optional[str] = None
    tituloLivro: Optional[str] = None
    descricao: Optional[str] = None
    dataCriacao: Optional[datetime] = None
    dataAlteracao: Optional[datetime] = None
    idLogin: Optional[int] = None
    email: Optional[str] = None


