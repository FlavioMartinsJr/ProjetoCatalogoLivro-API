import logging
from sqlalchemy.exc import IntegrityError
from Logger import logger
from models.Login import LoginModel
from models.Role import RoleModel

Role = RoleModel
log_Level = logging

class Permission:

    def Verify_Role_Permission_Owner(self,idLogin : int | None,funcao : str | None ,acesso : LoginModel,db):
        with db as session:
            try:
                if(acesso.id == idLogin):
                    return True
                
                else:
                    logger.GravarLog(funcao,"Permissão de usuario negada",acesso.email,log_Level.INFO)
                    logger.InsertLogger(funcao,"Permissão de usuario negada",acesso.id,log_Level.INFO,session)
                    return False
                
            except IntegrityError:
               raise

    def Verify_Role_Permission_Admin(self,funcao : str | None ,acesso : LoginModel,db):
        with db as session:
            try:
                if(acesso.role == Role.ADMINISTRADOR):
                    return True
                else:
                    logger.GravarLog(funcao,"Permissão de usuario negada",acesso.email,log_Level.INFO)
                    logger.InsertLogger(funcao,"Permissão de usuario negada",acesso.id,log_Level.INFO,session)
                    return False
                
            except IntegrityError:
               raise

permission: Permission = Permission()

