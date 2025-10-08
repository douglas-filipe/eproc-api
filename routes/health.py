from fastapi import APIRouter
from datetime import datetime
from config.database import SessionLocal
from sqlalchemy import text

router = APIRouter(
    tags=["Health"]
)

@router.get("/")
def root():
    return {
        "app": "EPROC Scraper - TJMG",
        "version": "1.0.0",
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "GET /": "Informações da API",
            "GET /health": "Status de saúde da aplicação",
            "GET /processos/{nome}": "Consulta processos por nome da parte"
        }
    }


@router.get("/health")
def health_check():
    
    db = SessionLocal()
    
    try:
        db.execute(text("SELECT 1"))
        db_status = "healthy"
        db_message = "Conexão com banco de dados OK"
    except Exception as e:
        db_status = "unhealthy"
        db_message = f"Erro na conexão: {str(e)}"
    finally:
        db.close()
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.now().isoformat(),
        "checks": {
            "database": {
                "status": db_status,
                "message": db_message
            }
        }
    }
