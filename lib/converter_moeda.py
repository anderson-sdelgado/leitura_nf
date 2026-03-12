import re

def extrair_valor(texto):
    if not texto:
        return None
    valor = re.sub(r"[^\d,.-]", "", texto)
    if "," in valor:
        valor = valor.replace(".", "").replace(",", ".")
    try:
        return float(valor)
    except:
        return None