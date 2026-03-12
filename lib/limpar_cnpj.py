import re

def limpar_cnpj(valor):
    if valor:
        return re.sub(r"\D", "", valor)
    return None
