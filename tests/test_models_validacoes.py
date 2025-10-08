import pytest
from models.parte import Parte
from models.processo import Processo

class TestValidacoesModels:
    def test_parte_nome_vazio(self, session):
        parte = Parte(nome="")
        session.add(parte)
        session.commit()
        
        assert parte.nome == ""
    
    def test_processo_campos_longos(self, session, parte_factory):
        parte = parte_factory()
        texto_longo = "A" * 10000
        
        processo = Processo(
            parte_id=parte.id,
            numero_processo="1234567-89.2024.8.13.0000",
            assunto=texto_longo,
            ultimo_evento=texto_longo
        )
        session.add(processo)
        session.commit()
        session.refresh(processo)
        
        assert len(processo.assunto) == 10000
        assert len(processo.ultimo_evento) == 10000
    
    def test_processo_campos_nulos_opcionais(self, session, parte_factory):
        parte = parte_factory()
        
        processo = Processo(
            parte_id=parte.id,
            numero_processo="1234567-89.2024.8.13.0000",
            autor=None,
            reu=None,
            assunto=None,
            ultimo_evento=None,
            link_processo=None
        )
        session.add(processo)
        session.commit()
        session.refresh(processo)
        
        assert processo.autor is None
        assert processo.reu is None
        assert processo.assunto is None