from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.database import init_db

from routes.processos import router as processos_router
from routes.health import router as health_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Iniciando EPROC Scraper API...")
    
    init_db()
    
    print("📊 Models carregados: Parte, Processo")
    print("📝 Documentação: http://localhost:8000/docs")
    
    yield
    
    print("👋 Encerrando EPROC Scraper API...")

app = FastAPI(
    title="EPROC Scraper - TJMG",
    description="API para consulta de processos judiciais do TJMG",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(processos_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
