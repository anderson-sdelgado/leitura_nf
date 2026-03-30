import fitz  # PyMuPDF
import pdfplumber

def ler_pdfplumber(caminho_pdf: str) -> str:
    try:
        texto = ""
        with pdfplumber.open(caminho_pdf) as pdf:
            for pagina in pdf.pages:
                texto += pagina.extract_text(layout=True) + "\n"
        return texto

    except Exception as e:
        print("Erro ao ler PDF lumber: ", e)
        return None

def ler_pymupedf(caminho_pdf: str) -> str:
    try:
        texto = ""
        with fitz.open(caminho_pdf) as pdf:
            for pagina in pdf:
                texto += pagina.get_text()
        return texto
    
    except Exception as e:
        print("Erro ao ler PDF pymupedf:", e)
        return None