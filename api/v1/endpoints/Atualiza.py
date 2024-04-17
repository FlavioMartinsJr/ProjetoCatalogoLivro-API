from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from helpers.__Session__ import get_session, Acesso
from services.UsuarioServices import _usuarioServices
from schemas.LoginSchemas import UsuarioUpdateSchemas
from services.AvaliacaoServices import _avaliacaoServices
from schemas.AvaliacaoSchemas import AvaliacaoUpdateSchemas
from services.ComentarioServices import _comentarioServices
from schemas.ComentarioSchemas import ComentarioUpdateSchemas

router = APIRouter()

@router.put('/AtualizaUsuarioById/{id}',response_model=None, status_code=status.HTTP_200_OK)
async def Atualiza_Usuario_Id(id: int,usuario: UsuarioUpdateSchemas, db: AsyncSession = Depends(get_session)):
    result = _usuarioServices.UpdateUsuarioById(id,usuario,Acesso.USER_ACESSO,db)
    return result

@router.put('/AtualizaAvaliacaoById/{id}',response_model=None, status_code=status.HTTP_200_OK)
async def Atualiza_Avaliacao_Id(id: int,avaliacao: AvaliacaoUpdateSchemas, db: AsyncSession = Depends(get_session)):
    result = _avaliacaoServices.UpdateAvaliacaoById(id,avaliacao,Acesso.USER_ACESSO,db)
    return result

@router.put('/AtualizaComentarioById/{id}',response_model=None, status_code=status.HTTP_200_OK)
async def Atualiza_Comentario_Id(id: int,comentario: ComentarioUpdateSchemas, db: AsyncSession = Depends(get_session)):
    result = _comentarioServices.UpdateComentarioById(id,comentario,Acesso.USER_ACESSO,db)
    return result

@router.put('/AtualizaAvaliacaoProprietarioById/{id}',response_model=None, status_code=status.HTTP_200_OK)
async def Atualiza_Avaliacao_Proprietario_Id(id: int,avaliacao: AvaliacaoUpdateSchemas, db: AsyncSession = Depends(get_session)):
    result = _avaliacaoServices.DeleteAvaliacaoOwnerById(id,avaliacao,Acesso.USER_ACESSO,db)
    return result

@router.put('/AtualizaComentarioProprietarioById/{id}',response_model=None, status_code=status.HTTP_200_OK)
async def Atualiza_Comentario_Proprietario_Id(id: int,comentario: ComentarioUpdateSchemas, db: AsyncSession = Depends(get_session)):
    result = _comentarioServices.UpdateComentarioOwnerById(id,comentario,Acesso.USER_ACESSO,db)
    return result
