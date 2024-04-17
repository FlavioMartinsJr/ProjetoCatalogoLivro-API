from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ValidaLoginSchemas(BaseModel):
    email: Optional[str] = None
    senha: Optional[str] = None

    class Config:
        orm_mode = True

class LoginSchemas(ValidaLoginSchemas):
    id: Optional[int] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    dataCriacao: Optional[datetime] = None
    dataAlteracao: Optional[datetime] = None
    role: Optional[str] = None
    ativo: Optional[bool] = None

class UsuarioUpdateSchemas(BaseModel):
    id: Optional[int] = None
    role: Optional[str] = None

    class Config:
        orm_mode = True

class UsuarioInsertSchemas(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    role: Optional[str] = None

    class Config:
        orm_mode = True

class UsuarioSelectSchemas(UsuarioUpdateSchemas):
    id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None
    dataCriacao: Optional[datetime] = None
    dataAlteracao: Optional[datetime] = None