import fitz  # PyMuPDF
import pdfplumber

def ler_pdfplumber(caminho_pdf: str) -> str:
    texto = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text(layout=True) + "\n"
    return texto

def ler_pymupedf(caminho_pdf: str) -> str:
    texto = ""
    with fitz.open(caminho_pdf) as pdf:
        for pagina in pdf:
            texto += pagina.get_text()
    return texto