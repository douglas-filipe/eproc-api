import pytest
from sqlalchemy.exc import IntegrityError
from models.parte import Parte

class TestParteModel:
    
    def test_criar_parte_sucesso(self, session):
        parte = Parte(nome="MARIA SANTOS")
        session.add(parte)
        session.commit()
        session.refresh(parte)
        
        assert parte.id is not None
        assert parte.nome == "MARIA SANTOS"
        assert parte.processos == []
    
    def test_criar_parte_nome_obrigatorio(self, session):
        parte = Parte(nome=None)
        session.add(parte)
        
        with pytest.raises(IntegrityError):
            session.commit()
    
    def test_nome_parte_deve_ser_unico(self, session, parte_factory):
        parte_factory(nome="JOSÉ SILVA")
        
        parte_duplicada = Parte(nome="JOSÉ SILVA")
        session.add(parte_duplicada)
        
        with pytest.raises(IntegrityError):
            session.commit()
    
    def test_parte_to_dict(self, session, parte_factory):
        parte = parte_factory(nome="PEDRO OLIVEIRA")
        
        resultado = parte.to_dict()
        
        assert isinstance(resultado, dict)
        assert resultado["id"] == parte.id
        assert resultado["nome"] == "PEDRO OLIVEIRA"
        assert resultado["total_processos"] == 0
    
    def test_parte_repr(self, session, parte_factory):
        parte = parte_factory(nome="ANA COSTA")
        
        resultado = repr(parte)
        
        assert "Parte" in resultado
        assert str(parte.id) in resultado
        assert "ANA COSTA" in resultado
    
    def test_buscar_parte_por_nome(self, session, parte_factory):
        parte_factory(nome="CARLOS MENDES")
        
        parte_encontrada = session.query(Parte).filter(
            Parte.nome == "CARLOS MENDES"
        ).first()
        
        assert parte_encontrada is not None
        assert parte_encontrada.nome == "CARLOS MENDES"
    
    def test_deletar_parte(self, session, parte_factory):
        parte = parte_factory(nome="LUCIA FERREIRA")
        parte_id = parte.id
        
        session.delete(parte)
        session.commit()
        
        parte_deletada = session.query(Parte).filter(Parte.id == parte_id).first()
        assert parte_deletada is None
    
    def test_atualizar_nome_parte(self, session, parte_factory):
        parte = parte_factory(nome="NOME ANTIGO")
        
        parte.nome = "NOME NOVO"
        session.commit()
        session.refresh(parte)
        
        assert parte.nome == "NOME NOVO"
