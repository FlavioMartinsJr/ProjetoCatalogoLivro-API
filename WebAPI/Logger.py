import logging
from sqlalchemy.exc import IntegrityError
from models.Log import LogModel
from os import path
from datetime import datetime

class Logger:

    def GravarLog(self,metodo : str | None,  mensagem : str | None, usuario : str | None , log_Level : logging):
        
        log_file = path.join(path.dirname(path.realpath(__file__)),"Logs\\Log.txt")
        logging.basicConfig(
            filename= log_file, 
            level=logging.INFO,
            encoding='utf-8', 
            format='%(asctime)s - %(levelname)s - %(funcName)s => %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'
        )
        MensagemLog = "[ metodo : "+ metodo +" ] [ " + mensagem +" ] [ usuario : " + usuario +" ]"

        if(log_Level == logging.ERROR):            
            logging.error(MensagemLog)

        elif(log_Level == logging.WARNING):
            logging.warning(MensagemLog)

        else:
            logging.info(MensagemLog)

    def InsertLogger(self,funcao : str | None ,situacao : str | None ,acesso : int | None, level : logging ,db):
        with db as session:
            try:
                if(level == logging.ERROR):            
                    level_log = "ERROR"

                elif(level == logging.WARNING):
                    level_log = "WARNING"

                else:
                    level_log = "INFO"

                model_log = LogModel(funcao=funcao,level=level_log,situacao=situacao,data=datetime.now(),idLogin=acesso)
                session.add(model_log)
                session.commit()
            
            except IntegrityError:
               raise

logger: Logger = Logger()