from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models import Base

class Parte(Base):
    __tablename__ = "partes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, unique=True, nullable=False)
    
    processos = relationship(
        "Processo", 
        back_populates="parte", 
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<Parte(id={self.id}, nome='{self.nome}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "total_processos": len(self.processos) if self.processos else 0
        }
