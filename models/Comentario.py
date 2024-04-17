from sqlalchemy import Column, Integer,ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from .Login import Base

class ComentarioModel(Base):
    __tablename__ = 'Tbl_ComentarioLivro'

    id = Column(Integer, primary_key=True, index=True)
    idLivro = Column(String(255))
    tituloLivro = Column(String(255))
    descricao = Column(String(255))
    dataCriacao = Column(DateTime)
    dataAlteracao = Column(DateTime)
    idLogin = Column(Integer, ForeignKey('Tbl_Login.id'))
    FK_comentario = relationship("LoginModel", back_populates="FK_comentario")
    
   