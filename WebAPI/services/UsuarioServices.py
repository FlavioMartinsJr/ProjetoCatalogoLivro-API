from typing import List
from sqlalchemy import insert, select,update,delete
from sqlalchemy.exc import IntegrityError
from fastapi import status, HTTPException
from Logger import logger
import logging
import re
from models.Login import LoginModel
from models.Role import RoleModel
from datetime import datetime
from helpers.__Permission__ import permission


Role = RoleModel
log_Level = logging

class UsuarioServices:

    def SelectUsuario(self, db):
        with db as session:
            try:
                query = select(LoginModel).where(LoginModel.ativo==True)
                result = session.execute(query)
                usuario: List[LoginModel] = result.scalars().all()
                session.commit()
                if(usuario.__len__() == 0):
                    logger.GravarLog("SelectUsuario","Retorno Vazio","",log_Level.WARNING)
                else:
                    logger.GravarLog("SelectUsuario","Consulta realizada com Sucesso","",log_Level.INFO)
                return usuario
            
            except IntegrityError:
                logger.GravarLog("SelectUsuario","Falha na Consulta","",log_Level.ERROR)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Falha na Consulta");log_Level.ERROR
    
    def SelectUsuarioById(Self,id,db):
        with db as session:
            try:
                query = select(LoginModel).filter(LoginModel.id == id,LoginModel.ativo == True)
                result = session.execute(query)
                usuario: List[LoginModel] = result.scalars().all()
                session.commit()
                if(usuario.__len__() == 0):
                    logger.GravarLog("SelectUsuariobyId","Retorno Vazio","",log_Level.WARNING)
                else:
                    logger.GravarLog("SelectUsuariobyId","Inclusão realizada com Sucesso","",log_Level.INFO)
                return usuario
                
            except IntegrityError:
                logger.GravarLog("SelectUsuariobyId","Falha na Consulta","",log_Level.ERROR)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi Possivel Consultar")
    
    def InsertLogin(self, login, db):
        with db as session:
            try:
                email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not (re.match(email, login.email)):
                    logger.GravarLog("InsertLogin","Falha na Inclusão","",log_Level.WARNING)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Email Não é Valido", headers="X-Insert-Error")
                
                if(len(login.senha) < 8):
                    logger.GravarLog("InsertLogin","Falha na Inclusão","",log_Level.WARNING)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Senha Muito Curto Minino 8 Caracteres", headers="X-Insert-Error")
                
                dataAtual = datetime.now()
                usuario_existe = select(LoginModel).where(LoginModel.email == login.email)
                result = session.execute(usuario_existe)
                usuario_existe: List[LoginModel] = result.scalars().all()
                if usuario_existe.__len__() == 0:
                    query = insert(LoginModel).values(email=login.email,senha=login.senha,dataCriacao=dataAtual,dataAlteracao=dataAtual,role=Role.USUARIO,ativo=True)
                    session.execute(query)
                    session.commit()
                    logger.GravarLog("InsertLogin","Inclusão realizada com Sucesso","",log_Level.INFO)
                    return HTTPException(status_code=status.HTTP_200_OK, detail="Adicionado com Sucesso",headers="X-Insert-Success")
                else:
                    logger.GravarLog("InsertLogin","Falha na Inclusão","",log_Level.WARNING)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Email de Usuario ja Existe", headers="X-Insert-Error")
                
            except IntegrityError:
                logger.GravarLog("InsertLogin","Falha na Inclusão","",log_Level.ERROR)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi Possivel Adicionar")
    
    def UpdateSenhaLoginByEmail(self, login, db):
        with db as session:
            try:
                dataAtual = datetime.now()
                query = update(LoginModel).where(LoginModel.id == id).values(dataAlteracao=dataAtual,senha=login.senha)
                result = session.execute(query)
                if result.rowcount > 0:
                    session.commit()
                    logger.GravarLog("UpdateSenhaLoginByEmail","Atualização realizada com Sucesso",acesso.email,log_Level.INFO)
                    logger.InsertLogger("UpdateSenhaLoginByEmail","Atualização realizada com Sucesso",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_200_OK, detail="Atualizado com Sucesso", headers={"dados_atualizados":{"data_alteracao":dataAtual,"role":usuario.role,}})
                else:
                    logger.GravarLog("UpdateUsuarioById","Retorno Vazio nenhum usuario encontrado",acesso.email,log_Level.WARNING)
                    logger.InsertLogger("UpdateUsuarioById","Retorno Vazio nenhum usuario encontrado",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Nenhum Usuario foi Encontrado", headers={"dados_atualizados":"Nenhum"})
                
            except IntegrityError:
                logger.GravarLog("UpdateUsuarioById","Falha na Atualização",acesso.email,log_Level.ERROR)
                logger.InsertLogger("UpdateUsuarioById","Falha na Atualização",acesso.id,log_Level.INFO,session)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Não foi Possivel Atualizar")

    def InsertUsuario(self, usuario, acesso, db):
        with db as session:
            try:
                if not(usuario.role == Role.ADMINISTRADOR or usuario.role == Role.USUARIO):
                    logger.GravarLog("InsertUsuario","Falha na Inclusão",acesso.email,log_Level.WARNING)
                    logger.InsertLogger("InsertUsuario","Falha na Inclusão",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Tipo de Permissão Inválida, Consulte o Admin",headers="X-Insert-Error")
   
                email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not (re.match(email, usuario.email)):
                    logger.GravarLog("InsertUsuario","Falha na Inclusão",acesso.email,log_Level.WARNING)
                    logger.InsertLogger("InsertUsuario","Falha na Inclusão",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Email Não é Valido", headers="X-Insert-Error")
                
                if(len(usuario.senha) < 8):
                    logger.GravarLog("InsertUsuario","Falha na Inclusão",acesso.email,log_Level.WARNING)
                    logger.InsertLogger("InsertUsuario","Falha na Inclusão",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Senha Muito Curto Minino 8 Caracteres", headers="X-Insert-Error")
                
                if(permission.Verify_Role_Permission_Admin("InsertUsuario",acesso,session) != True):
                    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sem Permissão Necessaria", headers={"Resultado":"Nenhum"})
                
                dataAtual = datetime.now()
                usuario_existe = select(LoginModel).where(LoginModel.email == usuario.email)
                result = session.execute(usuario_existe)
                usuario_existe: List[LoginModel] = result.scalars().all()
                if usuario_existe.__len__() == 0:
                    query = insert(LoginModel).values(email=usuario.email,senha=usuario.senha,dataCriacao=dataAtual,dataAlteracao=dataAtual,role=usuario.role,ativo=True)
                    session.execute(query)
                    session.commit()
                    logger.GravarLog("InsertUsuario","Inclusão realizada com Sucesso",acesso.email,log_Level.INFO)
                    logger.InsertLogger("InsertUsuario","Inclusão realizada com Sucesso",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_200_OK, detail="Adicionado com Sucesso",headers="X-Insert-Success")
                else:
                    logger.GravarLog("InsertUsuario","Falha na Inclusão",acesso.email,log_Level.WARNING)
                    logger.InsertLogger("InsertUsuario","Falha na Inclusão",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Email de Usuario ja Existe", headers="X-Insert-Error")
                
            except IntegrityError:
                logger.GravarLog("InsertUsuario","Falha na Inclusão",acesso.email,log_Level.ERROR)
                logger.InsertLogger("InsertUsuario","Falha na Inclusão",acesso.id,log_Level.ERROR,session)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi Possivel Adicionar")
    
    def UpdateUsuarioById(self, id, usuario, acesso, db):
        with db as session:
            try:
                if not(usuario.role == Role.ADMINISTRADOR or usuario.role == Role.USUARIO):
                    logger.GravarLog("UpdateUsuarioById","Retorno Vazio nenhuma alteração foi feita",acesso.email,log_Level.WARNING)
                    logger.InsertLogger("UpdateUsuarioById","Retorno Vazio nenhuma alteração foi feita",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Tipo de Permissão Inválida, Consulte o Admin", headers={"dados_atualizados":"Nenhum"})

                if(permission.Verify_Role_Permission_Admin("UpdateUsuarioById",acesso,session) != True):
                    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sem Permissão Necessaria", headers={"Resultado":"Nenhum"})

                dataAtual = datetime.now()
                query = update(LoginModel).where(LoginModel.id == id).values(dataAlteracao=dataAtual,role=usuario.role)
                result = session.execute(query)
                if result.rowcount > 0:
                    session.commit()
                    logger.GravarLog("UpdateUsuarioById","Atualização realizada com Sucesso",acesso.email,log_Level.INFO)
                    logger.InsertLogger("UpdateUsuarioById","Atualização realizada com Sucesso",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_200_OK, detail="Atualizado com Sucesso", headers={"dados_atualizados":{"data_alteracao":dataAtual,"role":usuario.role,}})
                else:
                    logger.GravarLog("UpdateUsuarioById","Retorno Vazio nenhum usuario encontrado",acesso.email,log_Level.WARNING)
                    logger.InsertLogger("UpdateUsuarioById","Retorno Vazio nenhum usuario encontrado",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Nenhum Usuario foi Encontrado", headers={"dados_atualizados":"Nenhum"})
                
            except IntegrityError:
                logger.GravarLog("UpdateUsuarioById","Falha na Atualização",acesso.email,log_Level.ERROR)
                logger.InsertLogger("UpdateUsuarioById","Falha na Atualização",acesso.id,log_Level.INFO,session)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Não foi Possivel Atualizar")

    def DeleteUsuarioById(self, id, acesso, db):
        with db as session:
            try:
                if(permission.Verify_Role_Permission(id,"DeleteUsuarioById",acesso,session) != True):
                    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sem Permissão Necessaria", headers={"Resultado":"Nenhum"})

                query = update(LoginModel).where(LoginModel.id == id).values(ativo=False)
                result = session.execute(query)
                if result.rowcount > 0:
                    session.commit()
                    logger.GravarLog("DeleteUsuarioById","Exclusão realizada com Sucesso",acesso.email,log_Level.INFO)
                    logger.InsertLogger("DeleteUsuarioById","Exclusão realizada com Sucesso",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_200_OK, detail="Exclusão com Sucesso", headers={"Usuario foi Desabilitado"})
                else:
                    logger.GravarLog("DeleteUsuarioById","Retorno Vazio nenhum usuario encontrado",acesso.email,log_Level.WARNING)
                    logger.InsertLogger("DeleteUsuarioById","Retorno Vazio nenhum usuario encontrado",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Nenhum Usuario foi Encontrado")
                
            except IntegrityError:
                logger.GravarLog("DeleteUsuarioById","Falha na Exclusão",acesso.email,log_Level.ERROR)
                logger.InsertLogger("DeleteUsuarioById","Falha na Exclusão",acesso.id,log_Level.INFO,session)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Não foi Possivel Excluir")        

_usuarioServices = UsuarioServices()