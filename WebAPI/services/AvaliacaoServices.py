from typing import List
import logging
from sqlalchemy import insert, select,update,delete
from sqlalchemy.exc import IntegrityError
from fastapi import status, HTTPException
from Logger import logger
from models.Login import LoginModel
from models.Avaliacao import AvaliacaoModel
from models.Role import RoleModel
from datetime import datetime
from services.UsuarioServices import _usuarioServices
from helpers.__Permission__ import permission

Role = RoleModel
log_Level = logging


class AvaliacaoServices:

    def SelectAvaliacao(self, db):
        with db as session:
            try:
                query = select(AvaliacaoModel.id,AvaliacaoModel.idLivro,AvaliacaoModel.tituloLivro,AvaliacaoModel.avaliacao, AvaliacaoModel.dataCriacao, AvaliacaoModel.dataAlteracao,AvaliacaoModel.idLogin,LoginModel.email).select_from(AvaliacaoModel).join(LoginModel,AvaliacaoModel.idLogin == LoginModel.id)
                result = session.execute(query)
                avaliacao: List[AvaliacaoModel] = result.all()
                session.commit()
                if(avaliacao.__len__() == 0):
                    logger.GravarLog("SelectAvaliacao","Retorno Vazio","",log_Level.WARNING)
                else:
                    logger.GravarLog("SelectAvaliacao","Consulta realizada com Sucesso","",log_Level.INFO)
                return avaliacao
            
            except IntegrityError:
                logger.GravarLog("SelectAvaliacao","Falha na Consulta","",log_Level.ERROR)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Falha na Consulta");log_Level.ERROR
    
    def SelectAvaliacaoById(Self,id,db):
        with db as session:
            try:
                query = select(AvaliacaoModel.id,AvaliacaoModel.idLivro,AvaliacaoModel.tituloLivro, AvaliacaoModel.avaliacao, AvaliacaoModel.dataCriacao, AvaliacaoModel.dataAlteracao,AvaliacaoModel.idLogin,LoginModel.email).select_from(AvaliacaoModel).join(LoginModel,AvaliacaoModel.idLogin == LoginModel.id).where(AvaliacaoModel.id == id)
                result = session.execute(query)
                avaliacao: List[AvaliacaoModel] = result.all()
                session.commit()
                if(avaliacao.__len__() == 0):
                    logger.GravarLog("SelectAvaliacaoById","Retorno Vazio","",log_Level.WARNING)
                else:
                    logger.GravarLog("SelectAvaliacaoById","Consulta realizada com Sucesso","",log_Level.INFO)
                return avaliacao
            
            except IntegrityError:
                logger.GravarLog("SelectAvaliacaoById","Falha na Consulta","",log_Level.ERROR)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Falha na Consulta");log_Level.ERROR
    
    def InsertAvaliacao(self, avaliacao, acesso, db):
        with db as session:
            try:
                if(permission.Verify_Role_Permission_Admin("InsertAvaliacao",acesso,session) != True):
                    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sem Permissão Necessaria", headers={"Resultado":"Nenhum"})
                
                dataAtual = datetime.now()
                result = _usuarioServices.SelectUsuarioById(avaliacao.idLogin,session)
                if result.__len__() != 0:
                    query = insert(AvaliacaoModel).values(idLivro=avaliacao.idLivro,tituloLivro=avaliacao.tituloLivro,avaliacao=avaliacao.avaliacao,dataCriacao=dataAtual,dataAlteracao=dataAtual,idLogin=avaliacao.idLogin)
                    session.execute(query)
                    session.commit()
                    logger.GravarLog("InsertAvaliacao","Inclusão realizada com Sucesso",acesso.email,log_Level.INFO)
                    logger.InsertLogger("InsertAvaliacao","Inclusão realizada com Sucesso",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_200_OK, detail="Adicionado com Sucesso",headers="X-Insert-Success")
                else:
                    logger.GravarLog("InsertAvaliacao","Falha na Inclusão",acesso.email,log_Level.WARNING)
                    logger.InsertLogger("InsertAvaliacao","Falha na Inclusão",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Usuario Não Existe ou Está Desabilitado", headers="X-Insert-Error")
                
            except IntegrityError:
                logger.GravarLog("InsertAvaliacao","Falha na Inclusão",acesso.email,log_Level.ERROR)
                logger.InsertLogger("InsertAvaliacao","Falha na Inclusão",acesso.id,log_Level.ERROR,session)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi Possivel Adicionar")
    
    def UpdateAvaliacaoById(self, id, avaliacao, acesso, db):
        with db as session:
            try:
                if(permission.Verify_Role_Permission_Admin("UpdateAvaliacaoById",acesso,session) != True):
                    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sem Permissão Necessaria", headers={"Resultado":"Nenhum"})

                dataAtual = datetime.now()
                query = update(AvaliacaoModel).where(AvaliacaoModel.id == id).values(avaliacao=avaliacao.avaliacao,dataAlteracao=dataAtual)
                result = session.execute(query)
                if result.rowcount > 0:
                    session.commit()
                    logger.GravarLog("UpdateAvaliacaoById","Atualização realizada com Sucesso",acesso.email,log_Level.INFO)
                    logger.InsertLogger("UpdateAvaliacaoById","Atualização realizada com Sucesso",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_200_OK, detail="Atualizado com Sucesso", headers={"dados_atualizados":{"avaliacao":avaliacao.avaliacao,"data_alteracao":dataAtual}})
                else:
                    logger.GravarLog("UpdateAvaliacaoById","Retorno Vazio nenhum usuario encontrado",acesso.email,log_Level.WARNING)
                    logger.InsertLogger("UpdateAvaliacaoById","Retorno Vazio nenhum usuario encontrado",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Nenhuma Avaliação foi Encontrada", headers={"dados_atualizados":"Nenhum"})
                
            except IntegrityError:
                logger.GravarLog("UpdateAvaliacaoById","Falha na Atualização",acesso.email,log_Level.ERROR)
                logger.InsertLogger("UpdateAvaliacaoById","Falha na Atualização",acesso.id,log_Level.INFO,session)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Não foi Possivel Atualizar")

    def UpdateAvaliacaoOwnerById(self, id, avaliacao, acesso, db):
        with db as session:
            try:
                avaliacao_buscada = session.query(AvaliacaoModel).filter(AvaliacaoModel.id==id,AvaliacaoModel.idLivro==acesso.id).first()
                if(avaliacao_buscada is None):
                    logger.GravarLog("UpdateAvaliacaoById","Retorno Vazio nenhum usuario encontrado",acesso.email,log_Level.WARNING)
                    logger.InsertLogger("UpdateAvaliacaoById","Retorno Vazio nenhum usuario encontrado",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Nenhuma Avaliação foi Encontrada", headers={"dados_atualizados":"Nenhum"})
                
                if(permission.Verify_Role_Permission_Owner(avaliacao_buscada.idLogin,"UpdateAvaliacaoById",acesso,session) != True):
                    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sem Permissão Necessaria", headers={"Resultado":"Nenhum"})

                dataAtual = datetime.now()
                query = update(AvaliacaoModel).where(AvaliacaoModel.id == id).values(avaliacao=avaliacao.avaliacao,dataAlteracao=dataAtual)
                result = session.execute(query)
                if result.rowcount > 0:
                    session.commit()
                    logger.GravarLog("UpdateAvaliacaoById","Atualização realizada com Sucesso",acesso.email,log_Level.INFO)
                    logger.InsertLogger("UpdateAvaliacaoById","Atualização realizada com Sucesso",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_200_OK, detail="Atualizado com Sucesso", headers={"dados_atualizados":{"avaliacao":avaliacao.avaliacao,"data_alteracao":dataAtual}})
                    
            except IntegrityError:
                logger.GravarLog("UpdateAvaliacaoById","Falha na Atualização",acesso.email,log_Level.ERROR)
                logger.InsertLogger("UpdateAvaliacaoById","Falha na Atualização",acesso.id,log_Level.INFO,session)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Não foi Possivel Atualizar")

    def DeleteAvaliacaoById(self, id, acesso, db):
        with db as session:
            try:
                if(permission.Verify_Role_Permission_Admin("DeleteAvaliacaoById",acesso,session) != True):
                    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sem Permissão Necessaria", headers={"Resultado":"Nenhum"})

                query = delete(AvaliacaoModel).where(AvaliacaoModel.id == id)
                result = session.execute(query)
                if result.rowcount > 0:
                    session.commit()
                    logger.GravarLog("DeleteAvaliacaoById","Exclusão realizada com Sucesso",acesso.email,log_Level.INFO)
                    logger.InsertLogger("DeleteAvaliacaoById","Exclusão realizada com Sucesso",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_200_OK, detail="Exclusão com Sucesso", headers={"Avaliação Foi Excluida"})
                else:
                    logger.GravarLog("DeleteAvaliacaoById","Retorno Vazio nenhum usuario encontrado",acesso.email,log_Level.WARNING)
                    logger.InsertLogger("DeleteAvaliacaoById","Retorno Vazio nenhum usuario encontrado",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Nenhuma Avaliação foi Encontrado")
                
            except IntegrityError:
                logger.GravarLog("DeleteAvaliacaoById","Falha na Exclusão",acesso.email,log_Level.ERROR)
                logger.InsertLogger("DeleteAvaliacaoById","Falha na Exclusão",acesso.id,log_Level.INFO,session)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Não foi Possivel Excluir")        

    def DeleteAvaliacaoOwnerById(self, id, acesso, db):
        with db as session:
            try:
                avaliacao_buscada = session.query(AvaliacaoModel).filter(AvaliacaoModel.id==id,AvaliacaoModel.idLivro==acesso.id).first()
                if(avaliacao_buscada is None):
                    logger.GravarLog("DeleteAvaliacaoById","Retorno Vazio nenhum usuario encontrado",acesso.email,log_Level.WARNING)
                    logger.InsertLogger("DeleteAvaliacaoById","Retorno Vazio nenhum usuario encontrado",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Nenhuma Avaliação foi Encontrado")
                
                if(permission.Verify_Role_Permission_Owner(avaliacao_buscada.idLogin,"DeleteAvaliacaoById",acesso,session) != True):
                    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sem Permissão Necessaria", headers={"Resultado":"Nenhum"})

                query = delete(AvaliacaoModel).where(AvaliacaoModel.id == id)
                result = session.execute(query)
                if result.rowcount > 0:
                    session.commit()
                    logger.GravarLog("DeleteAvaliacaoById","Exclusão realizada com Sucesso",acesso.email,log_Level.INFO)
                    logger.InsertLogger("DeleteAvaliacaoById","Exclusão realizada com Sucesso",acesso.id,log_Level.INFO,session)
                    return HTTPException(status_code=status.HTTP_200_OK, detail="Exclusão com Sucesso", headers={"Avaliação Foi Excluida"})
                    
            except IntegrityError:
                logger.GravarLog("DeleteAvaliacaoById","Falha na Exclusão",acesso.email,log_Level.ERROR)
                logger.InsertLogger("DeleteAvaliacaoById","Falha na Exclusão",acesso.id,log_Level.INFO,session)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Não foi Possivel Excluir")        

_avaliacaoServices = AvaliacaoServices()