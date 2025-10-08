from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base


class Processo(Base):
    __tablename__ = "processos"

    id = Column(Integer, primary_key=True, index=True)
    numero_processo = Column(String, index=True, nullable=False)
    autor = Column(String)
    reu = Column(String)
    assunto = Column(Text)
    ultimo_evento = Column(Text)
    link_processo = Column(Text)
    
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    parte_id = Column(Integer, ForeignKey("partes.id", ondelete="CASCADE"), nullable=False)
    parte = relationship("Parte", back_populates="processos")

    def __repr__(self):
        return f"<Processo(id={self.id}, numero='{self.numero_processo}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "numero_processo": self.numero_processo,
            "autor": self.autor,
            "reu": self.reu,
            "assunto": self.assunto,
            "ultimo_evento": self.ultimo_evento,
            "link_processo": self.link_processo,
            "parte_id": self.parte_id,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
            "atualizado_em": self.atualizado_em.isoformat() if self.atualizado_em else None
        }
