from sqlalchemy import Column, Integer,ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from .Login import Base

class LogModel(Base):
    __tablename__ = 'Tbl_Log'

    id = Column(Integer, primary_key=True, index=True)
    funcao = Column(String(255))
    level = Column(String(255))
    situacao = Column(String(255))
    data = Column(DateTime)
    idLogin = Column(Integer, ForeignKey('Tbl_Login.id'))
    FK_log = relationship("LoginModel", back_populates="FK_log")
    

   