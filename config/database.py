from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from pathlib import Path

# Configurações
DATABASE_DIR = Path("data")
DATABASE_DIR.mkdir(exist_ok=True)

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    f"sqlite:///{DATABASE_DIR}/eproc.db"
)

# Engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    poolclass=StaticPool if "sqlite" in DATABASE_URL else None,
    echo=False
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """Dependency para obter sessão do banco"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas.
    IMPORTANTE: Base deve ser importado dos models, não do database!
    """
    # Importa Base LOCALMENTE (não no topo do arquivo)
    from models.base import Base
    
    print("🔧 Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("✅ Banco de dados inicializado!")
    
    # Verifica tabelas criadas
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    if tables:
        print(f"📊 Tabelas criadas: {', '.join(tables)}")
    else:
        print("⚠️ Nenhuma tabela foi criada!")