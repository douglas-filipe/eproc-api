import time
import json
from pathlib import Path
from typing import List, Dict, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

from sqlalchemy.orm import Session
from config.database import SessionLocal
from models import Parte, Processo

EPROC_URL = "https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica"
BASE_URL = "https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/"
DATA_DIR = Path("data")
TIMEOUT = 20
WAIT_TIME = 2

class EProcScraper:
    def __init__(self, headless: bool = True):
        self.driver = self._init_driver(headless)
        DATA_DIR.mkdir(exist_ok=True)
    
    def _init_driver(self, headless: bool) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    
    def _build_full_url(self, relative_url: str) -> str:
        if not relative_url:
            return None
        return relative_url if relative_url.startswith("http") else BASE_URL + relative_url
    
    def _extract_text_from_link(self, element, tag: str = "a") -> tuple[str, Optional[str]]:
        try:
            link_elem = element.find_element(By.TAG_NAME, tag)
            text = link_elem.text.strip()
            link = self._build_full_url(link_elem.get_attribute("href"))
            return text, link
        except NoSuchElementException:
            return element.text.strip(), None
    
    def buscar_partes(self, nome: str) -> List[Dict]:
        print(f"🔍 Pesquisando pelo nome: {nome}...")
        
        self.driver.get(EPROC_URL)
        time.sleep(WAIT_TIME)
        
        campo_nome = self.driver.find_element(By.ID, "txtStrParte")
        campo_nome.clear()
        campo_nome.send_keys(nome)
        
        botao = self.driver.find_element(By.ID, "sbmNovo")
        botao.click()
        
        try:
            WebDriverWait(self.driver, TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#divInfraAreaTabela .infraTable"))
            )
            time.sleep(WAIT_TIME)
        except TimeoutException:
            print("❌ Timeout ao aguardar resultados")
            return []
        
        return self._extrair_partes_da_tabela()
    
    def _extrair_partes_da_tabela(self) -> List[Dict]:
        todas_linhas = self.driver.find_elements(By.CSS_SELECTOR, "#divInfraAreaTabela .infraTable tr")
        
        linhas_dados = [
            tr for tr in todas_linhas 
            if tr.find_elements(By.TAG_NAME, "td")
        ]
        
        print(f"✅ {len(linhas_dados)} parte(s) encontrada(s)")
        
        partes = []
        for linha in linhas_dados:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            
            if len(colunas) >= 1:
                nome, link = self._extract_text_from_link(colunas[0])
                cpf_cnpj = colunas[1].text.strip() if len(colunas) >= 2 else ""
                
                partes.append({
                    "nome": nome,
                    "cpf_cnpj": cpf_cnpj,
                    "link": link
                })
        
        return partes
    
    def coletar_processos_da_parte(self, link_parte: str) -> List[Dict]:
        if not link_parte:
            return []
        
        try:
            self.driver.get(link_parte)
            
            WebDriverWait(self.driver, TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#divInfraAreaTabela .infraTable"))
            )
            time.sleep(WAIT_TIME)
            
            return self._extrair_processos_da_tabela()
            
        except Exception as e:
            print(f"  ❌ Erro ao coletar processos: {e}")
            return []
    
    def _extrair_processos_da_tabela(self) -> List[Dict]:
        todas_linhas = self.driver.find_elements(By.CSS_SELECTOR, "#divInfraAreaTabela .infraTable tr")
        
        linhas_dados = [
            tr for tr in todas_linhas 
            if tr.find_elements(By.TAG_NAME, "td")
        ]
        
        processos = []
        for linha in linhas_dados:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            
            if len(colunas) >= 5:
                numero, link_processo = self._extract_text_from_link(colunas[0])
                
                processos.append({
                    "numero_processo": numero,
                    "autor": colunas[1].text.strip(),
                    "reu": colunas[2].text.strip(),
                    "assunto": colunas[3].text.strip(),
                    "ultimo_evento": colunas[4].text.strip(),
                    "link_processo": link_processo
                })
        
        print(f"  ✅ Coletados {len(processos)} processo(s)")
        return processos
    
    def close(self):
        self.driver.quit()


class EProcService:
    
    def __init__(self):
        self.scraper = EProcScraper(headless=True)
    
    def buscar_e_salvar(self, nome: str) -> List[Dict]:
        db = SessionLocal()
        resultados = []
        
        try:
            partes_info = self.scraper.buscar_partes(nome)
            
            if not partes_info:
                print("❌ Nenhuma parte encontrada")
                return []
            
            for idx, parte_info in enumerate(partes_info, 1):
                print(f"\n[{idx}/{len(partes_info)}] Processando: {parte_info['nome']}")
                
                parte = self._obter_ou_criar_parte(db, parte_info['nome'])
                
                processos_data = self.scraper.coletar_processos_da_parte(parte_info['link'])
                time.sleep(1)
                
                self._salvar_processos(db, parte, processos_data)
                
                resultados.append({
                    "nome_parte": parte_info['nome'],
                    "cpf_cnpj": parte_info['cpf_cnpj'],
                    "link": parte_info['link'],
                    "processos": processos_data
                })
            
            self._salvar_json(nome, resultados)
            
            total_processos = sum(len(r["processos"]) for r in resultados)
            print(f"\n📊 Busca finalizada:")
            print(f"   • {len(resultados)} parte(s) coletada(s)")
            print(f"   • {total_processos} processo(s) coletado(s)")
            
        except Exception as e:
            print(f"❌ Erro ao processar: {e}")
            db.rollback()
            raise
        finally:
            db.close()
        
        return resultados
    
    def _obter_ou_criar_parte(self, db: Session, nome: str) -> Parte:
        parte = db.query(Parte).filter(Parte.nome == nome).first()
        
        if not parte:
            parte = Parte(nome=nome)
            db.add(parte)
            db.commit()
            db.refresh(parte)
        
        return parte
    
    def _salvar_processos(self, db: Session, parte: Parte, processos_data: List[Dict]):
        for proc_data in processos_data:
            processo = Processo(
                numero_processo=proc_data["numero_processo"],
                autor=proc_data["autor"],
                reu=proc_data["reu"],
                assunto=proc_data["assunto"],
                ultimo_evento=proc_data["ultimo_evento"],
                link_processo=proc_data["link_processo"],
                parte_id=parte.id
            )
            db.add(processo)
        
        db.commit()
    
    def _salvar_json(self, nome: str, dados: List[Dict]):
        if not dados:
            return
        
        arquivo = DATA_DIR / f"resultados_{nome.replace(' ', '_')}.json"
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        
        print(f"✅ JSON salvo em: {arquivo}")
    
    def close(self):
        self.scraper.close()