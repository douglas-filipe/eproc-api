import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.parte import Parte
from models.processo import Processo

@pytest.fixture(scope="function")
def engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def session(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.close()

@pytest.fixture
def parte_factory(session):
    def _create_parte(nome="JOÃO DA SILVA"):
        parte = Parte(nome=nome)
        session.add(parte)
        session.commit()
        session.refresh(parte)
        return parte
    return _create_parte

@pytest.fixture
def processo_factory(session):
    def _create_processo(parte_id, numero="0000000-00.0000.0.00.0000", **kwargs):
        processo = Processo(
            parte_id=parte_id,
            numero_processo=numero,
            autor=kwargs.get("autor", "AUTOR TESTE"),
            reu=kwargs.get("reu", "RÉU TESTE"),
            assunto=kwargs.get("assunto", "Assunto Teste"),
            ultimo_evento=kwargs.get("ultimo_evento", "Evento Teste"),
            link_processo=kwargs.get("link_processo", "https://teste.com")
        )
        session.add(processo)
        session.commit()
        session.refresh(processo)
        return processo
    return _create_processo