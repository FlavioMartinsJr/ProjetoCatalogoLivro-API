from sqlalchemy import Column, Integer,ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from .Login import Base

class AvaliacaoModel(Base):
    __tablename__ = 'Tbl_AvaliacaoLivro'

    id = Column(Integer, primary_key=True, index=True)
    idLivro = Column(String(255))
    tituloLivro = Column(String(255))
    avaliacao = Column(Integer)
    dataCriacao = Column(DateTime)
    dataAlteracao = Column(DateTime)
    idLogin = Column(Integer, ForeignKey('Tbl_Login.id'))
    FK_avaliacao = relationship("LoginModel", back_populates="FK_avaliacao")
    
   