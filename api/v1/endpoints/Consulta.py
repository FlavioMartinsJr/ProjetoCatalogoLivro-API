from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from helpers.__Session__ import get_session
from services.UsuarioServices import _usuarioServices
from services.AvaliacaoServices import _avaliacaoServices
from services.ComentarioServices import _comentarioServices
from schemas.LoginSchemas import UsuarioSelectSchemas
from schemas.AvaliacaoSchemas import AvaliacaoSelectSchemas
from schemas.ComentarioSchemas import ComentarioSelectSchemas

router = APIRouter()

@router.get('/ListaUsuario', response_model=list[UsuarioSelectSchemas], status_code=status.HTTP_200_OK)
async def Lista_Usuario(db: AsyncSession = Depends(get_session)):
    result = _usuarioServices.SelectUsuario(db)
    return result

@router.get('/ListaUsuarioById/{id}', response_model=list[UsuarioSelectSchemas],status_code=status.HTTP_200_OK)
async def Lista_Usuario_Id(id: int,db: AsyncSession = Depends(get_session)):
    result = _usuarioServices.SelectUsuarioById(id,db)
    return result

@router.get('/ListaAvaliacao', response_model=list[AvaliacaoSelectSchemas], status_code=status.HTTP_200_OK)
async def Lista_Avaliacao(db: AsyncSession = Depends(get_session)):
    result = _avaliacaoServices.SelectAvaliacao(db)
    return result

@router.get('/ListaAvaliacaoById/{id}', response_model=list[AvaliacaoSelectSchemas],status_code=status.HTTP_200_OK)
async def Lista_Avaliacao_Id(id: int,db: AsyncSession = Depends(get_session)):
    result = _avaliacaoServices.SelectAvaliacaoById(id,db)
    return result

@router.get('/ListaComentario', response_model=list[ComentarioSelectSchemas], status_code=status.HTTP_200_OK)
async def Lista_Comentario(db: AsyncSession = Depends(get_session)):
    result = _comentarioServices.SelectComentario(db)
    return result

@router.get('/ListaComentarioById/{id}', response_model=list[ComentarioSelectSchemas],status_code=status.HTTP_200_OK)
async def Lista_Comentario_Id(id: int,db: AsyncSession = Depends(get_session)):
    result = _comentarioServices.SelectComentarioById(id,db)
    return result


