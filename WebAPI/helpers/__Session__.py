from typing import Generator
from Configs import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from helpers.__db__ import Session
from helpers.__Auth__ import AuthLogin
from Logger import logger
import logging

log_Level = logging

class Acesso:
    USER_ACESSO = None

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=settings.API_V1+"/Auth/RealizaLogin"
)

def get_session() -> Generator:
    session = Session()
    try:
        yield session
    
    except Exception as ex:
        logger.GravarLog(metodo=ex.detail,mensagem=ex.detail,usuario="",log_Level=log_Level.ERROR)
    
    finally:
        session.close()

def Token_Verifier_Login(db_session: Session = Depends(get_session), token = Depends(oauth2_schema)):
    uc = AuthLogin(db_session=db_session)
    data = uc.Verify_Token_Login(access_token=token)
    Acesso.USER_ACESSO = data
