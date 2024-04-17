from fastapi import status
from fastapi.exceptions import HTTPException
from datetime import datetime, timedelta
from sqlalchemy import update
from helpers.__Session__ import Session
from jose import jwt, JWTError,ExpiredSignatureError
from models.Login import LoginModel
from schemas.LoginSchemas import ValidaLoginSchemas
from Configs import settings
from Logger import logger
import logging

log_Level = logging

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.ALGORITHM
EXPIRES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

class AuthLogin:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def Login(self, user: ValidaLoginSchemas, expires_in: int = EXPIRES):
        user_on_db = self.db_session.query(LoginModel).filter(LoginModel.email==user.email,LoginModel.senha==user.senha).first()
        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Email ou Senha invalida'
            )
        if user_on_db.ativo is False:
          raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Usuario Está Desativado'
            )
        exp = datetime.utcnow() + timedelta(minutes=expires_in)
        payload = {
            'sub': str(user_on_db.id),
            'exp': exp
        }
        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return {
            'access_token': access_token,
            'exp': exp.isoformat(),
            'id': user_on_db.id,
            'email': user_on_db.email,
            'role': user_on_db.role,
            'ativo':user_on_db.ativo
        }

    def tokenizar_senha(self, senha: str,user: ValidaLoginSchemas, expires_in: int = EXPIRES):
        user_on_db = self.db_session.query(LoginModel).filter(LoginModel.email==user.email).first()
        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Email não é valido'
            )
        exp = datetime.utcnow() + timedelta(minutes=expires_in)
        payload = {
            'sub': senha,
            'id':user_on_db.id,
            'exp': exp
        }
        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return access_token
    
    def Verify_Token_Login(self,access_token):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            user_on_db = self.db_session.query(LoginModel).filter(LoginModel.id == data['sub'],LoginModel.ativo==True).first()
            if user_on_db is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Usuario não é mais valido'
                )
            return user_on_db
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token Expirado"
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token inválido"
            )
        
    def Verify_Senha_Token_Login(self, access_token):
        try:
            dataAtual = datetime.now()
            data = jwt.decode(access_token, SECRET_KEY,algorithms=[ALGORITHM])
            query = update(LoginModel).where(LoginModel.id == data['id'], LoginModel.ativo == True).values(senha=data['sub'],dataAlteracao=dataAtual)
            result = self.db_session.execute(query)
            if result.rowcount == 0:
                logger.GravarLog("UpdateSenhaLoginByEmail","Retorno Vazio nenhum usuario encontrado",'',log_Level.INFO)
                logger.InsertLogger("UpdateSenhaLoginByEmail","Retorno Vazio nenhum usuario encontrado",data['id'],log_Level.INFO,self.db_session)
                return HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Usuario não é mais valido',
                    headers={"dados_atualizados":"Nenhum"}
                )
            else:
                self.db_session.commit()
                logger.GravarLog("UpdateSenhaLoginByEmail","Atualização realizada com Sucesso",'',log_Level.INFO)
                logger.InsertLogger("UpdateSenhaLoginByEmail","Atualização realizada com Sucesso",data['id'],log_Level.INFO,self.db_session)
                return HTTPException(
                    status_code=status.HTTP_200_OK,
                    detail='Senha alterada',
                    headers={"dados_atualizados":{"data_alteracao":dataAtual,"senha_nova":data['sub']}}
                )
        except ExpiredSignatureError:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token Expirado"
            )    
        except JWTError:
            return HTTPException(
                status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, 
                detail="Token inválido"
            )

