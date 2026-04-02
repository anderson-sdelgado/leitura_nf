import unicodedata

def buscar_uf(estado):
    # Dicionário mapeando nomes normalizados (sem acento e minúsculos) para UF
    estados_brasileiros = {
        "acre": "AC", "alagoas": "AL", "amapa": "AP", "amazonas": "AM",
        "bahia": "BA", "ceara": "CE", "distrito federal": "DF",
        "espirito santo": "ES", "goias": "GO", "maranhao": "MA",
        "mato grosso": "MT", "mato grosso do sul": "MS", "minas gerais": "MG",
        "para": "PA", "paraiba": "PB", "parana": "PR", "pernambuco": "PE",
        "piaui": "PI", "rio de janeiro": "RJ", "rio grande do norte": "RN",
        "rio grande do sul": "RS", "rondonia": "RO", "roraima": "RR",
        "santa catarina": "SC", "sao paulo": "SP", "sergipe": "SE",
        "tocantins": "TO"
    }

    def normalizar_texto(texto):
        if not texto: return ""
        texto = texto.strip().lower()
        nfkd_form = unicodedata.normalize('NFKD', texto)
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

    nome_busca = normalizar_texto(estado)
    
    return estados_brasileiros.get(nome_busca, None)