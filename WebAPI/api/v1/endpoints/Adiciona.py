from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from helpers.__Session__ import get_session, Acesso
from services.UsuarioServices import _usuarioServices
from schemas.LoginSchemas import UsuarioInsertSchemas
from services.AvaliacaoServices import _avaliacaoServices
from schemas.AvaliacaoSchemas import AvaliacaoInsertSchemas
from services.ComentarioServices import _comentarioServices
from schemas.ComentarioSchemas import ComentarioInsertSchemas

router = APIRouter()

@router.post('/AdicionaUsuario', status_code=status.HTTP_201_CREATED, response_model=None)
async def Adiciona_Usuario(usuario: UsuarioInsertSchemas, db: AsyncSession = Depends(get_session)):
    result = _usuarioServices.InsertUsuario(usuario,Acesso.USER_ACESSO,db)
    return result

@router.post('/AdicionaAvaliacao', status_code=status.HTTP_201_CREATED, response_model=None)
async def Adiciona_Avaliacao(avaliacao: AvaliacaoInsertSchemas, db: AsyncSession = Depends(get_session)):
    result = _avaliacaoServices.InsertAvaliacao(avaliacao,Acesso.USER_ACESSO,db)
    return result

@router.post('/AdicionaComentario', status_code=status.HTTP_201_CREATED, response_model=None)
async def Adiciona_Comentario(cometario: ComentarioInsertSchemas, db: AsyncSession = Depends(get_session)):
    result = _comentarioServices.InsertComentario(cometario,Acesso.USER_ACESSO,db)
    return result


    
        