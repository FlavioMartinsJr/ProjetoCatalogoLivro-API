from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from services.UsuarioServices import _usuarioServices
from helpers.__Auth__ import AuthLogin
from helpers.__Menssage__ import Menssage
from schemas.LoginSchemas import ValidaLoginSchemas,LoginSchemas
from helpers.__Session__ import get_session

router = APIRouter()

@router.post('/AdicionaLogin', status_code=status.HTTP_201_CREATED, response_model=None)
async def Adiciona_Login(login: ValidaLoginSchemas, db: AsyncSession = Depends(get_session)):
    result = _usuarioServices.InsertLogin(login,db)
    return result

@router.get('/SolicitaEsqueceuSenhaLogin/{email}', status_code=status.HTTP_200_OK, response_model=None)
async def Solicita_Esqueceu_Senha_Login(email: str, db: AsyncSession = Depends(get_session)):
    uc = AuthLogin(db_session=db)
    nova_senha = Menssage.gerar_nova_senha()
    user_buscar = ValidaLoginSchemas(
        email=email
    )

    token_senha = uc.tokenizar_senha(senha=nova_senha,user=user_buscar)
    Menssage.send_email(email,token_senha)
    return JSONResponse(
        content="Email Enviado, Verifique sua caixa de Entrada",
        status_code=status.HTTP_200_OK
    )

@router.get('/AlteraSenhaLoginByToken/{token}', status_code=status.HTTP_200_OK)
async def Altera_Senha_Login_Token(token: str, db: AsyncSession = Depends(get_session)):
    uc = AuthLogin(db_session=db)
    result = uc.Verify_Senha_Token_Login(access_token=token)
    return result

@router.post('/RealizaLogin', status_code=status.HTTP_200_OK)
async def Realiza_Login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    uc = AuthLogin(db_session=db)
    user = ValidaLoginSchemas(
        email=form_data.username,
        senha=form_data.password
    )
    result = uc.Login(user=user)
    return JSONResponse(
        content=result,
        status_code=status.HTTP_200_OK
    )

@router.get('/AutenticaLoginByToken/{token}',response_model=LoginSchemas, status_code=status.HTTP_200_OK)
async def Autentica_Login_Token(token: str, db: AsyncSession = Depends(get_session)):
    uc = AuthLogin(db_session=db)
    result = uc.Verify_Token_Login(access_token=token)
    return result
      

        