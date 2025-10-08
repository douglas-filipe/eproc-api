import pytest
from models.parte import Parte
from models.processo import Processo

class TestRelacionamentosModels:
    def test_parte_com_multiplos_processos(self, session, parte_factory, processo_factory):
        parte = parte_factory(nome="MARIA OLIVEIRA")
        
        processo_factory(parte_id=parte.id, numero="1111111-11.2024.8.13.0000")
        processo_factory(parte_id=parte.id, numero="2222222-22.2024.8.13.0000")
        processo_factory(parte_id=parte.id, numero="3333333-33.2024.8.13.0000")
        session.refresh(parte)
        
        assert len(parte.processos) == 3
        assert parte.to_dict()["total_processos"] == 3
    
    def test_processo_acessa_parte(self, session, parte_factory, processo_factory):
        parte = parte_factory(nome="CARLOS SANTOS")
        processo = processo_factory(parte_id=parte.id)
        
        session.refresh(processo)
        
        assert processo.parte is not None
        assert processo.parte.nome == "CARLOS SANTOS"
        assert processo.parte.id == parte.id
    
    def test_deletar_parte_deleta_processos_cascade(self, session, parte_factory, processo_factory):
        parte = parte_factory()
        processo_factory(parte_id=parte.id, numero="1111111-11.2024.8.13.0000")
        processo_factory(parte_id=parte.id, numero="2222222-22.2024.8.13.0000")
        parte_id = parte.id
        
        session.delete(parte)
        session.commit()
        
        processos_orfaos = session.query(Processo).filter(
            Processo.parte_id == parte_id
        ).all()
        assert len(processos_orfaos) == 0  # Foram deletados
    
    def test_multiple_partes_com_processos(self, session, parte_factory, processo_factory):
        parte1 = parte_factory(nome="PARTE 1")
        parte2 = parte_factory(nome="PARTE 2")
        
        processo_factory(parte_id=parte1.id, numero="1111111-11.2024.8.13.0000")
        processo_factory(parte_id=parte1.id, numero="2222222-22.2024.8.13.0000")
        processo_factory(parte_id=parte2.id, numero="3333333-33.2024.8.13.0000")
        
        session.refresh(parte1)
        session.refresh(parte2)
        
        assert len(parte1.processos) == 2
        assert len(parte2.processos) == 1
        assert parte1.processos[0].parte.nome == "PARTE 1"
        assert parte2.processos[0].parte.nome == "PARTE 2"
    
    def test_lazy_loading_processos(self, session, parte_factory, processo_factory):
        parte = parte_factory()
        processo_factory(parte_id=parte.id, numero="1111111-11.2024.8.13.0000")
        processo_factory(parte_id=parte.id, numero="2222222-22.2024.8.13.0000")
        
        session.commit()
        parte_id = parte.id
        session.close()
        
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=session.bind)
        nova_sessao = Session()
        
        parte_recarregada = nova_sessao.query(Parte).filter(
            Parte.id == parte_id
        ).first()
        
        assert len(parte_recarregada.processos) == 2
        nova_sessao.close()
