from typing import List
import logging
from sqlalchemy import insert, select,update,delete
from sqlalchemy.exc import IntegrityError
from fastapi import status, HTTPException
from Logger import logger
from models.Login import LoginModel
from models.Comentario import ComentarioModel
from models.Role import RoleModel
from datetime import datetime
from services.UsuarioServices import _usuarioServices
from helpers.__Permission__ import permission

Role = RoleModel
log_Level = logging


class ComentarioServices:

    def SelectComentario(self, db):
        with db as session:
            try:
                query = select(ComentarioModel.id,ComentarioModel.idLivro,ComentarioModel.tituloLivro,ComentarioModel.descricao, ComentarioModel.dataCriacao, ComentarioModel.dataAlteracao,ComentarioModel.idLogin,LoginModel.email).select_from(ComentarioModel).join(LoginModel,ComentarioModel.idLogin == LoginModel.id)
                result = session.execute(query)
                comentario: List[ComentarioModel] = result.all()
                session.commit()
                if(comentario.__len__() == 0):
                    logger.GravarLog("SelectComentario","Retorno Vazio","",log_Level.WARNING)
                else:
                    logger.GravarLog("SelectComentario","Consulta realizada com Sucesso","",log_Level.INFO)
                return comentario
            
            except IntegrityError:
                logger.GravarLog("SelectComentario","Falha na Consulta","",log_Level.ERROR)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Falha na Consulta");log_Level.ERROR
    
    def SelectComentarioById(Self,id,db):
        with db as session:
            try:
                query = select(ComentarioModel.id,ComentarioModel.idLivro,ComentarioModel.tituloLivro,ComentarioModel.descricao, ComentarioModel.dataCriacao, ComentarioModel.dataAlteracao,ComentarioModel.idLogin,LoginModel.email).select_from(ComentarioModel).join(LoginModel,ComentarioModel.idLogin == LoginModel.id).where(ComentarioModel.id == id)
                result = session.execute(query)
                comentario: List[ComentarioModel] = result.all()
                session.commit()
                if(comentario.__len__() == 0):
                    logger.GravarLog("SelectComentarioById","Retorno Vazio","",log_Level.WARNING)
                else:
                    logger.GravarLog("SelectComentarioById","Consulta realizada com Sucesso","",log_Level.INFO)
                return comentario
            
            except IntegrityError:
                logger.GravarLog("SelectComentarioById","Falha na Consulta","",log_Level.ERROR)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Falha na Consulta");log_Level.ERROR
    
    def InsertComentario(self, comentario, acesso, db):
        with db as session:
            try:
                if(permission.Verify_Role_Permission_Admin("InsertComentario",acesso,session) != True):
                    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sem Permissão Necessaria", headers={"Resultado":"Nenhum"})
                
                dataAtual = datetime.now()
                result = _usuarioServices.SelectUsuarioById(comentario.idLogin,session)
                if result.__len__() != 0:
                    query = insert(ComentarioModel).values(idLivro=comentario.idLivro,tituloLivro=comentario.tituloLivro,descricao=comentario.descricao,dataCriacao=dataAtual,dataAlteracao=dataAtual,idLogin=comentario.idLogin)
                    session.execute(query)
                    session.commit()
                    logger.GravarLog("InsertComentario","Inclusão realizada com Sucesso",acesso.email,log_Level.INFO)
                    logger.InsertLogger("InsertComentario","Inclusão realizada com Sucesso",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_200_OK, detail="Adicionado com Sucesso",headers="X-Insert-Success")
                else:
                    logger.GravarLog("InsertComentario","Falha na Inclusão",acesso.email,log_Level.WARNING)
                    logger.InsertLogger("InsertComentario","Falha na Inclusão",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Usuario Não Existe ou Está Desabilitado", headers="X-Insert-Error")
                
            except IntegrityError:
                logger.GravarLog("InsertComentario","Falha na Inclusão",acesso.email,log_Level.ERROR)
                logger.InsertLogger("InsertComentario","Falha na Inclusão",acesso.id,log_Level.ERROR,session)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi Possivel Adicionar")
    
    def UpdateComentarioById(self, id, comentario, acesso, db):
        with db as session:
            try:
                if(permission.Verify_Role_Permission_Admin("UpdateComentarioById",acesso,session) != True):
                    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sem Permissão Necessaria", headers={"Resultado":"Nenhum"})

                dataAtual = datetime.now()
                query = update(ComentarioModel).where(ComentarioModel.id == id).values(idLivro=comentario.idLivro,tituloLivro=comentario.tituloLivro,descricao=comentario.descricao,dataAlteracao=dataAtual)
                result = session.execute(query)
                if result.rowcount > 0:
                    session.commit()
                    logger.GravarLog("UpdateComentarioById","Atualização realizada com Sucesso",acesso.email,log_Level.INFO)
                    logger.InsertLogger("UpdateComentarioById","Atualização realizada com Sucesso",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_200_OK, detail="Atualizado com Sucesso", headers={"dados_atualizados":{"idLivro":comentario.idLivro,"tituloLivro":comentario.tituloLivro,"descricao":comentario.descricao,"data_alteracao":dataAtual}})
                else:
                    logger.GravarLog("UpdateComentarioById","Retorno Vazio nenhum usuario encontrado",acesso.email,log_Level.WARNING)
                    logger.InsertLogger("UpdateComentarioById","Retorno Vazio nenhum usuario encontrado",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Nenhum Comentario foi Encontrada", headers={"dados_atualizados":"Nenhum"})
                
            except IntegrityError:
                logger.GravarLog("UpdateAvaliacaoById","Falha na Atualização",acesso.email,log_Level.ERROR)
                logger.InsertLogger("UpdateAvaliacaoById","Falha na Atualização",acesso.id,log_Level.INFO,session)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Não foi Possivel Atualizar")
    
    def UpdateComentarioOwnerById(self, id, comentario, acesso, db):
        with db as session:
            try:
                comentario_buscado = session.query(ComentarioModel).filter(ComentarioModel.id==id,ComentarioModel.idLivro==acesso.id).first()
                if(comentario_buscado is None):
                    logger.GravarLog("UpdateComentarioById","Retorno Vazio nenhum usuario encontrado",acesso.email,log_Level.WARNING)
                    logger.InsertLogger("UpdateComentarioById","Retorno Vazio nenhum usuario encontrado",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Nenhum Comentario foi Encontrada", headers={"dados_atualizados":"Nenhum"})
                
                if(permission.Verify_Role_Permission_Owner(comentario_buscado.idLogin,"UpdateComentarioById",acesso,session) != True):
                    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sem Permissão Necessaria", headers={"Resultado":"Nenhum"})

                dataAtual = datetime.now()
                query = update(ComentarioModel).where(ComentarioModel.id == id).values(idLivro=comentario.idLivro,tituloLivro=comentario.tituloLivro,descricao=comentario.descricao,dataAlteracao=dataAtual)
                result = session.execute(query)
                if result.rowcount > 0:
                    session.commit()
                    logger.GravarLog("UpdateComentarioById","Atualização realizada com Sucesso",acesso.email,log_Level.INFO)
                    logger.InsertLogger("UpdateComentarioById","Atualização realizada com Sucesso",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_200_OK, detail="Atualizado com Sucesso", headers={"dados_atualizados":{"idLivro":comentario.idLivro,"tituloLivro":comentario.tituloLivro,"descricao":comentario.descricao,"data_alteracao":dataAtual}})
                    
            except IntegrityError:
                logger.GravarLog("UpdateAvaliacaoById","Falha na Atualização",acesso.email,log_Level.ERROR)
                logger.InsertLogger("UpdateAvaliacaoById","Falha na Atualização",acesso.id,log_Level.INFO,session)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Não foi Possivel Atualizar")

    def DeleteComentarioById(self, id, acesso, db):
        with db as session:
            try:
                if(permission.Verify_Role_Permission_Admin("DeleteComentarioById",acesso,session) != True):
                    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sem Permissão Necessaria", headers={"Resultado":"Nenhum"})

                query = delete(ComentarioModel).where(ComentarioModel.id == id)
                result = session.execute(query)
                if result.rowcount > 0:
                    session.commit()
                    logger.GravarLog("DeleteComentarioById","Exclusão realizada com Sucesso",acesso.email,log_Level.INFO)
                    logger.InsertLogger("DeleteComentarioById","Exclusão realizada com Sucesso",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_200_OK, detail="Exclusão com Sucesso", headers={"Comentario Foi Excluido"})
                else:
                    logger.GravarLog("DeleteComentarioById","Retorno Vazio nenhum usuario encontrado",acesso.email,log_Level.WARNING)
                    logger.InsertLogger("DeleteComentarioById","Retorno Vazio nenhum usuario encontrado",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Nenhum Comentario foi Encontrado")
                
            except IntegrityError:
                logger.GravarLog("DeleteComentarioById","Falha na Exclusão",acesso.email,log_Level.ERROR)
                logger.InsertLogger("DeleteComentarioById","Falha na Exclusão",acesso.id,log_Level.INFO,session)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Não foi Possivel Excluir")        

    def DeleteComentarioOwnerById(self, id, acesso, db):
        with db as session:
            try:
                comentario_buscado = session.query(ComentarioModel).filter(ComentarioModel.id==id,ComentarioModel.idLivro==acesso.id).first()
                if(comentario_buscado is None):
                    logger.GravarLog("DeleteComentarioById","Retorno Vazio nenhum usuario encontrado",acesso.email,log_Level.WARNING)
                    logger.InsertLogger("DeleteComentarioById","Retorno Vazio nenhum usuario encontrado",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Nenhum Comentario foi Encontrado")
                
                if(permission.Verify_Role_Permission_Owner(comentario_buscado.idLogin,"DeleteComentarioById",acesso,session) != True):
                    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sem Permissão Necessaria", headers={"Resultado":"Nenhum"})

                query = delete(ComentarioModel).where(ComentarioModel.id == id)
                result = session.execute(query)
                if result.rowcount > 0:
                    session.commit()
                    logger.GravarLog("DeleteComentarioById","Exclusão realizada com Sucesso",acesso.email,log_Level.INFO)
                    logger.InsertLogger("DeleteComentarioById","Exclusão realizada com Sucesso",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_200_OK, detail="Exclusão com Sucesso", headers={"Comentario Foi Excluido"})
                     
            except IntegrityError:
                logger.GravarLog("DeleteComentarioById","Falha na Exclusão",acesso.email,log_Level.ERROR)
                logger.InsertLogger("DeleteComentarioById","Falha na Exclusão",acesso.id,log_Level.INFO,session)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Não foi Possivel Excluir")        

_comentarioServices = ComentarioServices()