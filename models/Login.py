from sqlalchemy import Column, Integer,func, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from Configs import settings

Base = settings.DBBaseModel

class LoginModel(Base):
    __tablename__ = 'Tbl_Login'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255))
    senha = Column(String(255))
    dataCriacao = Column(DateTime)
    dataAlteracao = Column(DateTime)
    role = Column(String(255))
    ativo = Column(Boolean)
    FK_log = relationship("LogModel", back_populates="FK_log")
    FK_avaliacao = relationship("AvaliacaoModel", back_populates="FK_avaliacao")
    FK_comentario = relationship("ComentarioModel", back_populates="FK_comentario")
   
