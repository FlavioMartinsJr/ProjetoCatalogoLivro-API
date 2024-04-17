from pydantic.v1 import BaseSettings
from urllib.parse import quote_plus
from sqlalchemy.ext.declarative import declarative_base

class Configs(BaseSettings):

    PARAMS = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-MRL05JF\SQLEXPRESS;"
        "PORT=1433;"
        "DATABASE=ProjetoLivro;"
        "Trusted_Connection=yes"
    )
    CONN_STR = quote_plus(PARAMS)
    
    DB_URL: str = "mssql+pyodbc:///?odbc_connect=%s" % CONN_STR
    DBBaseModel = declarative_base()
    API_V1: str = '/ProjetoLivro/Api/V1'
    JWT_SECRET: str = 'qS96E1oCfq5gEZH-ngD91NC2qkcl0cffhNTIDGpF4pw'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    EMAIL: str = "projetolivros59@gmail.com"
    PWD: str = "gpod fwdt caio exqz"
    

    class Config:
        case_sensitive = True

settings: Configs = Configs()