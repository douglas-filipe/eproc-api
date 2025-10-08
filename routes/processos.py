from fastapi import APIRouter, HTTPException
from utils.eproc_scraper import EProcService

router = APIRouter(
    prefix="/processos",
    tags=["Processos"]
)

@router.get("/{nome}")
def consultar_processos(nome: str):
    nome = nome.upper().strip()
    print(f"🔎 Consultando processos para: {nome}")
    
    service = EProcService()
    
    try:
        resultados = service.buscar_e_salvar(nome)
        
        if not resultados:
            raise HTTPException(
                status_code=404, 
                detail=f"Nenhum processo encontrado para '{nome}'"
            )
        
        processos_formatados = []
        for resultado in resultados:
            for processo in resultado['processos']:
                processos_formatados.append({
                    **processo,
                    "parte": resultado['nome_parte'],
                    "cpf_cnpj": resultado['cpf_cnpj']
                })
        
        return {
            "nome_consultado": nome,
            "total_partes": len(resultados),
            "total_processos": len(processos_formatados),
            "processos": processos_formatados
        }
        
    except HTTPException:
        raise
        
    except Exception as e:
        print(f"❌ Erro ao processar: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao processar: {str(e)}"
        )
    
    finally:
        service.close()
