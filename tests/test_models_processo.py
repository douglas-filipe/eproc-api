import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from models.processo import Processo

class TestProcessoModel:
    def test_criar_processo_sucesso(self, session, parte_factory):
        parte = parte_factory()
        
        processo = Processo(
            parte_id=parte.id,
            numero_processo="1234567-89.2024.8.13.0000",
            autor="JOÃO DA SILVA",
            reu="EMPRESA XYZ LTDA",
            assunto="Cobrança",
            ultimo_evento="Audiência marcada",
            link_processo="https://eproc.tjmg.jus.br/teste"
        )
        session.add(processo)
        session.commit()
        session.refresh(processo)
        
        assert processo.id is not None
        assert processo.numero_processo == "1234567-89.2024.8.13.0000"
        assert processo.autor == "JOÃO DA SILVA"
        assert processo.reu == "EMPRESA XYZ LTDA"
        assert processo.parte_id == parte.id
    
    def test_processo_campos_obrigatorios(self, session, parte_factory):
        parte = parte_factory()

        processo = Processo(
            parte_id=parte.id,
            numero_processo=None
        )
        session.add(processo)

        with pytest.raises(IntegrityError):
            session.commit()
    
    def test_processo_sem_parte_id(self, session):
        processo = Processo(
            numero_processo="1234567-89.2024.8.13.0000",
            parte_id=None
        )
        session.add(processo)
        
        with pytest.raises(IntegrityError):
            session.commit()
    
    def test_processo_timestamps_automaticos(self, session, parte_factory):
        parte = parte_factory()
        
        processo = Processo(
            parte_id=parte.id,
            numero_processo="1234567-89.2024.8.13.0000",
            autor="AUTOR TESTE"
        )
        session.add(processo)
        session.commit()
        session.refresh(processo)
        
        assert processo.criado_em is not None
        assert processo.atualizado_em is not None
        assert isinstance(processo.criado_em, datetime)
        assert isinstance(processo.atualizado_em, datetime)
    
    def test_processo_to_dict(self, session, parte_factory, processo_factory):
        parte = parte_factory()
        processo = processo_factory(
            parte_id=parte.id,
            numero="9876543-21.2024.8.13.0000",
            autor="TESTE AUTOR"
        )
        
        resultado = processo.to_dict()
        
        assert isinstance(resultado, dict)
        assert resultado["id"] == processo.id
        assert resultado["numero_processo"] == "9876543-21.2024.8.13.0000"
        assert resultado["autor"] == "TESTE AUTOR"
        assert resultado["parte_id"] == parte.id
        assert "criado_em" in resultado
        assert "atualizado_em" in resultado
    
    def test_processo_repr(self, session, parte_factory, processo_factory):
        parte = parte_factory()
        processo = processo_factory(
            parte_id=parte.id,
            numero="1111111-11.2024.8.13.0000"
        )
        
        resultado = repr(processo)
        
        assert "Processo" in resultado
        assert str(processo.id) in resultado
        assert "1111111-11.2024.8.13.0000" in resultado
    
    def test_buscar_processo_por_numero(self, session, parte_factory, processo_factory):
        parte = parte_factory()
        numero = "5555555-55.2024.8.13.0000"
        processo_factory(parte_id=parte.id, numero=numero)
        
        processo_encontrado = session.query(Processo).filter(
            Processo.numero_processo == numero
        ).first()
        
        assert processo_encontrado is not None
        assert processo_encontrado.numero_processo == numero
    
    def test_atualizar_processo(self, session, parte_factory, processo_factory):
        parte = parte_factory()
        processo = processo_factory(parte_id=parte.id, ultimo_evento="Evento Antigo")
        data_criacao = processo.criado_em
        
        processo.ultimo_evento = "Evento Atualizado"
        session.commit()
        session.refresh(processo)
        
        assert processo.ultimo_evento == "Evento Atualizado"
        assert processo.criado_em == data_criacao
        assert processo.atualizado_em > data_criacao
    
    def test_deletar_processo(self, session, parte_factory, processo_factory):
        parte = parte_factory()
        processo = processo_factory(parte_id=parte.id)
        processo_id = processo.id
        
        session.delete(processo)
        session.commit()

        processo_deletado = session.query(Processo).filter(
            Processo.id == processo_id
        ).first()
        assert processo_deletado is None