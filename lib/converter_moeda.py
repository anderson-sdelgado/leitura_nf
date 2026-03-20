import re

def extrair_valor(texto):
    if texto is None:
        return None # Retornar número em vez de None ajuda em cálculos
    
    # Se já for um número (float/int), retorna ele mesmo
    if isinstance(texto, (float, int)):
        return float(texto)
        
    # Garante que é string para o re.sub não dar erro
    texto_str = str(texto).strip()
    if texto_str == "-" or not texto_str:
        return None

    valor = re.sub(r"[^\d,.-]", "", texto_str)
    
    if "," in valor:
        # Transforma o padrão brasileiro 1.234,56 em 1234.56
        valor = valor.replace(".", "").replace(",", ".")
    
    try:
        return float(valor)
    except:
        return None