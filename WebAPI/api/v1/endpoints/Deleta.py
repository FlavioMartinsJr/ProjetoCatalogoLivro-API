from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from helpers.__Session__ import get_session, Acesso
from services.UsuarioServices import _usuarioServices
from services.AvaliacaoServices import _avaliacaoServices
from services.ComentarioServices import _comentarioServices

router = APIRouter()

@router.delete('/DeletaUsuarioById/{id}',response_model=None, status_code=status.HTTP_200_OK)
async def Deleta_Usuario_Id(id: int, db: AsyncSession = Depends(get_session)):
    result = _usuarioServices.DeleteUsuarioById(id,Acesso.USER_ACESSO,db)
    return result

@router.delete('/DeletaAvaliacaoById/{id}',response_model=None, status_code=status.HTTP_200_OK)
async def Deleta_Avaliacao_Id(id: int, db: AsyncSession = Depends(get_session)):
    result = _avaliacaoServices.DeleteAvaliacaoById(id,Acesso.USER_ACESSO,db)
    return result

@router.delete('/DeletaComentarioById/{id}',response_model=None, status_code=status.HTTP_200_OK)
async def Deleta_Comentario_Id(id: int, db: AsyncSession = Depends(get_session)):
    result = _comentarioServices.DeleteComentarioById(id,Acesso.USER_ACESSO,db)
    return result

@router.delete('/DeletaAvaliacaoProprietarioById/{id}',response_model=None, status_code=status.HTTP_200_OK)
async def Deleta_Avaliacao_Proprietario_Id(id: int, db: AsyncSession = Depends(get_session)):
    result = _avaliacaoServices.DeleteAvaliacaoOwnerById(id,Acesso.USER_ACESSO,db)
    return result

@router.delete('/DeletaComentarioProprietarioById/{id}',response_model=None, status_code=status.HTTP_200_OK)
async def Deleta_Comentario_Proprietario_Id(id: int, db: AsyncSession = Depends(get_session)):
    result = _comentarioServices.DeleteComentarioOwnerById(id,Acesso.USER_ACESSO,db)
    return result