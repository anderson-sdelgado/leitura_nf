import re

def limpar_cnpj(valor):
    if valor:
        return re.sub(r"\D", "", valor)
    return None

def formatar_cnpj(cnpj):
    if not cnpj:
        return None
    # Remove qualquer caractere que não seja número primeiro
    c = "".join(filter(str.isdigit, str(cnpj)))
    if len(c) == 14:
        return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}"
    return cnpj # Retorna original se não tiver 14 dígitos