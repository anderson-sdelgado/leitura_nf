import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_sistema_giap(texto: str):

    # print("----------- NOTA GIAP -----------")
    # print(f"{texto}")
    # print("-------------------------")

    prestador = pegar_dados_prestador(texto)
    tomador = pegar_dados_tomador(texto)
    tributos = pegar_valores(texto)
    servico = pegar_dados_servico(texto)
    
    nota = {}
    nota["DT_HR_INCL"] = None # Data e hora da inclusão da linha.
    nota["DT_HR_ALT"] = None # Data e hora da alteração da linha.
    nota["CDDOCUMENT"] = None # Código do documento no SE Suite. Idem V_NF_SERV.
    nota["NRO_CHAVE"] = None # Chave para registro da NFs-e. Gerada na integração.
    nota["CPF_CNPJ_EMIT"] = limpar_cnpj(tomador['cnpj']) # CNPJ/CPF da empresa (tomador) - somente números. Vide V_NF_SERV.TS_CNPJ_CPF.
    nota["COD_PART"] = limpar_cnpj(prestador['cnpj']) # CNPJ/CPF do fornecedor (prestador) - somente números. Vide V_NF_SERV.PS_CNPJ_CPF.
    nota["COD_MOD"] = "99" # Código do modelo de documento fiscal para registro. Fixo "99".
    nota["SERIE"] = "A" # Série do documento fiscal para registro. Fixo "A".
    nota["DTINSERT"] = None # Data da inclusão no SE Suite. Idem V_NF_SERV.
    nota["DTUPDATE"] = None # Data da alteração no SE Suite. Idem V_NF_SERV.
    nota["ID_DOC"] = None # ID do documento na view. Idem V_NF_SERV.
    nota["PREFEIT"] = pegar_prefeitura(texto) # Nome da prefeitura. Idem V_NF_SERV.
    nota["SECRET_PREFEIT"] = pegar_secretaria(texto) # Secretaria da prefeitura. Idem V_NF_SERV.
    nota["NRO_NF"] = pegar_numero_nf(texto) # Número da NF. Idem V_NF_SERV.
    nota["DT_EMISS"] = pegar_data_hora_emissao(texto) # Data de emissão da NF. Idem V_NF_SERV.
    nota["PS_RAZ_SOC_NOME"] = prestador['razao_social'] # Nome do prestador de serviço. Idem V_NF_SERV.
    nota["PS_CNPJ_CPF"] = prestador['cnpj'] # CNPJ do prestador de serviço. Idem V_NF_SERV.
    nota["PS_INSC_MUNIC"] = prestador['inscricao_municipal'] # Inscrição municipal do prestador de serviço. Idem V_NF_SERV.
    nota["PS_INSC_EST"] = prestador['inscricao_estadual'] # Inscrição estadual do prestador de serviço. Idem V_NF_SERV.
    nota["PS_MUNIC"] = prestador['municipio'] # Nome do município do prestador de serviço. Idem V_NF_SERV.
    nota["PS_UF"] = prestador['uf'] # Sigla da UF do prestador de serviço. Idem V_NF_SERV.
    nota["PS_ENDERECO"] = prestador['endereco'] # Endereço do prestador de serviço. Idem V_NF_SERV.
    nota["PS_BAIRRO"] = prestador['bairro'] # Bairro do prestador de serviço. Idem V_NF_SERV.
    nota["PS_CEP"] = prestador['cep'] # CEP do prestador de serviço. Idem V_NF_SERV.
    nota["PS_EMAIL"] = prestador['email'] # E-mail do prestador de serviço. Idem V_NF_SERV.
    nota["TS_RAZ_SOC_NOME"] = tomador['razao_social'] # Nome do tomador de serviço - empresa usuária. Idem V_NF_SERV.
    nota["TS_CNPJ_CPF"] = tomador['cnpj'] # CNPJ do tomador de serviço - empresa usuária. Idem V_NF_SERV.
    nota["DESC_SERV"] = pegar_discriminacao_servico(texto) # Descrição do serviço. Idem V_NF_SERV.
    nota["VL_BRUTO"] = extrair_valor(tributos["bruto"]) # Valor bruto. Idem V_NF_SERV.
    nota["VL_LIQ"] = extrair_valor(tributos["liquido"]) # Valor líquido. Idem V_NF_SERV.
    nota["VL_PIS"] = extrair_valor(tributos["pis"]) # Valor do PIS. Idem V_NF_SERV.
    nota["VL_COFINS"] = extrair_valor(tributos["cofins"]) # Valor da Cofins. Idem V_NF_SERV.
    nota["VL_IR"] = extrair_valor(tributos["ir"]) # Valor do IR. Idem V_NF_SERV.
    nota["VL_INSS"] = extrair_valor(tributos["inss"]) # Valor do INSS. Idem V_NF_SERV.
    nota["VL_CSLL"] = extrair_valor(tributos["csll"]) # Valor da CSLL. Idem V_NF_SERV.
    nota["VL_ISS"] = extrair_valor(tributos["iss"]) # Valor do ISS. Idem V_NF_SERV.
    nota["COD_SERVICO"] = servico["codigo"] # Código do serviço. Idem V_NF_SERV.
    nota["COD_SERVICO_ORIGINAL"] = servico["descricao_completa"] # Código do serviço - informação original. Idem V_NF_SERV.

    print("----------- NOTA GIAP -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("-----------------------------------")

def pegar_prefeitura(texto):
    match = re.search(r'(PREFEITURA.*?)\s*$', texto, re.I | re.M)
    if not match: return None
    return match.group(1).strip()

def pegar_secretaria(texto):
    match = re.search(r'(SECRETARIA.*?)\s*$', texto, re.I | re.M)
    if not match: return None
    sujeira = [r'\d+', r'-']
    texto_limpo = match.group(1)
    for termo in sujeira:
        texto_limpo = re.sub(termo, '', texto_limpo, flags=re.I | re.S)
    return texto_limpo.strip()

def pegar_numero_nf(texto):
    padrao = (
        r'Nº\s*Nota'
        r'\s*(.*?)\s*'
        r'PREFEITURA'
    )
    match = re.search(padrao, texto, re.I)
    if not match: return None
    return match.group(1).strip()

def pegar_data_hora_emissao(texto):
    meses = {
        'JAN': '01', 'FEV': '02', 'MAR': '03', 'ABR': '04',
        'MAI': '05', 'JUN': '06', 'JUL': '07', 'AGO': '08',
        'SET': '09', 'OUT': '10', 'NOV': '11', 'DEZ': '12'
    }
    m = re.search(r'(\d{2})/([A-Z]{3})/(\d{4})[-\s]*(\d{2}:\d{2}:\d{2})', texto, re.I)
    if m:
        dia = m.group(1)
        mes_extenso = m.group(2).upper()
        ano = m.group(3)
        hora = m.group(4)
        mes_num = meses.get(mes_extenso, mes_extenso)
        return f"{dia}/{mes_num}/{ano} {hora}"
    return None

def pegar_dados_prestador(texto):
    dados = {
        "razao_social": None, "cnpj": None, "inscricao_municipal": None,
        "inscricao_estadual": None, "endereco": None,
        "bairro": None, "cep": None, "municipio": None, "uf": None, "email": None
    }
    padrao = (
        r'PRESTADOR\s*DE\s*SERVI[CÇ]OS'
        r'\s*(.*?)\s*'
        r'TOMADOR\s*DE\s*SERVIÇOS'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()

    padrao = r'Raz[aâãáà]o\s*Social/Nome:\s*(.*)$'
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if match: dados["razao_social"] = match.group(1).strip()

    padrao = r'CNPJ/CPF:\s*([\d\.\-/]+)'
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados["cnpj"] = match.group(1).strip()

    padrao = r'Insc(?:i[cç][aâãáà]o|\.)\s*Municipal:\s*(.*?)\s*Insc\s*'
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados["inscricao_municipal"] = match.group(1).strip()
    
    padrao = r'Insc(?:i[cç][aâãáà]o|\.)\s*Estadual:\s*(.*)$'
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if match: dados["inscricao_estadual"] = match.group(1).strip()

    padrao = r'Endere[cç]o:\s*(.*)$'
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if not match: endereco = None
    endereco = match.group(1).strip()

    complemento = None
    match = re.search(r'Complemento:\s*(.*?)\s*Bairro', bloco_completo, re.I | re.S)
    if match:
        texto_raw = match.group(1).strip()
        texto_limpo = re.sub(r'N[aâãáà]o\s*Informado', '', texto_raw, flags=re.I).strip()
        if texto_limpo: complemento = texto_limpo

    partes = [item for item in [endereco, complemento] if item]
    dados['endereco'] = ", ".join(partes)

    padrao = r'Bairro:\s*(.*?)\s*CEP\s*'
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados["bairro"] = match.group(1).strip()

    match = re.search(r'CEP:\s*(\d{2}\.?\d{3}-?\d{3})', texto)
    if match: dados["cep"] = match.group(1).strip()

    padrao = r'Município:\s*(.*?)\s*UF:\s*([A-Z]{2})'
    match = re.search(padrao, texto, re.I)
    if match:
        dados["municipio"] = match.group(1).strip()
        dados["uf"] = match.group(2).strip()

    match = re.search(r'E-mail:\s*([^\s\n]+)', texto, re.I)
    if match: dados["email"] = match.group(1).strip()
    
    return dados

def pegar_dados_tomador(texto):
    dados = {"razao_social": None, "cnpj": None}
    padrao = (
        r'TOMADOR\s*DE\s*SERVI[CÇ]OS'
        r'\s*(.*?)\s*'
        r'DISCRIMINA[CÇ][AÃÁÀÂ]O'
    )
    match = re.search(padrao, texto, re.S | re.I)
    if not match: return dados
    
    bloco_completo = match.group(1)
    
    padrao = r'Raz[aâãáà]o\s*Social/Nome:\s*(.*)$'
    match = re.search(padrao, bloco_completo, re.I | re.M)
    dados["razao_social"] = match.group(1).replace('\n', ' ').strip() if match else None
    
    match = re.search(r'CNPJ/CPF:\s*([\d\.\-/]+)', bloco_completo)
    dados["cnpj"] = match.group(1).strip() if match else None
    
    return dados

def pegar_discriminacao_servico(texto):
    padrao = (
        r'DISCRIMINA[CÇ][AÃÁÀÂ]O\s*DOS\s*SERVI[CÇ]OS.'
        r'\s*(.*?)\s*'
        r'INFORMA[CÇ][OÒÓÕÔ]ES\s*COMPLEMENTARES'
    )
    match = re.search(padrao, texto, re.S | re.I)
    if not match: return None
    return match.group(1).strip()

def pegar_valores(texto):
    dados = {
        "bruto": None, "liquido": None, "ir": None, 
        "pis": None, "cofins": None, "csll": None, 
        "inss": None, "iss": None
    }

    padrao = r'VALOR\s*TOTAL\s*DA\s*NOTA.*?R\$\s*([\d.]+,\d{2})'
    match = re.search(padrao, texto, re.I | re.S)
    if match: dados["bruto"] = match.group(1)

    padrao = (
            r'Valor\s*do\s*INSS\s*Retido\s*'
            r'\s*(.*?)\s*'
            r'OUTRAS\s*INFORMA[CÇ][OÒÓÕÔ]ES'
        )
    match = re.search(padrao, texto, re.IGNORECASE | re.S)
    if match:
            padrao = r"[\d\.,]+"
            valores = re.findall(padrao, match.group(1))
            if len(valores) >= 2:
                dados['inss'] = valores[0]
                dados['ir'] = valores[1]
                dados['csll'] = valores[2]
                dados['pis'] = valores[3]
                dados['cofins'] = valores[4]
                dados['liquido'] = valores[-1]
                dados['iss'] = valores[-2]
    return dados

def pegar_dados_servico(texto):
    dados = {"codigo": None, "descricao_completa": None}
    padrao = (
        r'Ativ.\s*Servi[cç]o:\s*'
        r'\s*(.*?)\s*'
        r'Valor\s*do\s*INSS\s*Retido\s*'
    )
    match = re.search(padrao, texto, re.S | re.I)
    if not match: return None

    bloco_completo = match.group(1).strip()
    dados['descricao_completa'] = bloco_completo.strip()

    match = re.search(r'\s*(.*?)\s*-\s*', bloco_completo, re.IGNORECASE | re.M)
    if match: dados["codigo"] = match.group(1).strip()

    return dados