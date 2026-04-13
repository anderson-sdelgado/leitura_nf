import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_municipio_campo_grande(texto: str):

    print("------- NOTA CAMPO GRANDE --------")
    print(f"{texto}")
    print("----------------------------------")

    secretaria_data = pegar_dados_secretaria_data(texto)
    prefeitura_nro = pegar_dados_prefeitura_nro(texto)
    prestador = pegar_dados_prestador(texto)
    tomador = pegar_dados_tomador(texto)
    financeiro = pegar_valores(texto)
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
    nota["ID_DOC"] = pegar_codigo(texto) # ID do documento na view. Idem V_NF_SERV.
    nota["PREFEIT"] = prefeitura_nro['prefeitura'] # Nome da prefeitura. Idem V_NF_SERV.
    nota["SECRET_PREFEIT"] = secretaria_data['secretaria'] # Secretaria da prefeitura. Idem V_NF_SERV.
    nota["NRO_NF"] = prefeitura_nro['nro'] # Número da NF. Idem V_NF_SERV.
    nota["DT_EMISS"] = secretaria_data['data'] # Data de emissão da NF. Idem V_NF_SERV.
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
    nota["VL_BRUTO"] = extrair_valor(financeiro["bruto"]) # Valor bruto. Idem V_NF_SERV. 
    nota["VL_LIQ"] = extrair_valor(financeiro["liquido"]) # Valor líquido. Idem V_NF_SERV.
    nota["VL_PIS"] = extrair_valor(financeiro["pis"]) # Valor do PIS. Idem V_NF_SERV.
    nota["VL_COFINS"] = extrair_valor(financeiro["cofins"]) # Valor da Cofins. Idem V_NF_SERV.
    nota["VL_IR"] = extrair_valor(financeiro["ir"]) # Valor do IR. Idem V_NF_SERV.
    nota["VL_INSS"] = extrair_valor(financeiro["inss"]) # Valor do INSS. Idem V_NF_SERV.
    nota["VL_CSLL"] = extrair_valor(financeiro["csll"]) # Valor da CSLL. Idem V_NF_SERV.
    nota["VL_ISS"] = extrair_valor(financeiro["iss"]) # Valor do ISS. Idem V_NF_SERV.
    nota["COD_SERVICO"] = servico["codigo"] # Código do serviço. Idem V_NF_SERV.
    nota["COD_SERVICO_ORIGINAL"] = servico["descricao"] # Código do serviço - informação original. Idem V_NF_SERV.
        
    print("---------- NOTA CAMPINAS -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("-----------------------------------")

def pegar_codigo(texto):
    padrao = (
        r'C[oóòôõ]digo\s*de\s*Verifica[cç][aãáàâ]o'
        r'\s*(.*?)\s*'
        r'PRESTADOR\s*DE\s*SERVI[CÇ]OS'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    return match.group(1).strip()

def pegar_dados_prefeitura_nro(texto):
    dados = {
        "prefeitura": None, 
        "nro": None, 
    }
    padrao = r'(PREFEITURA.*?)\s*(\d+)\s*'
    match = re.search(padrao, texto, re.I | re.M)
    if match: 
        dados['prefeitura'] = match.group(1).strip()
        dados['nro'] = match.group(2).strip()
    return dados

def pegar_dados_secretaria_data(texto):
    dados = {
        "secretaria": None, 
        "data": None, 
    }
    padrao = r'(SECRETARIA.*?)\s*(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})\s*'
    match = re.search(padrao, texto, re.I | re.S)
    if match: 
        dados['secretaria'] = match.group(1).strip()
        dados['data'] = match.group(2).strip()

    return dados

def pegar_dados_prestador(texto):
    dados = {
        "cnpj": None, 
        "inscricao_municipal": None, 
        "inscricao_estadual": None,
        "razao_social": None, 
        "endereco": None, 
        "bairro": None, 
        "municipio": None, 
        "uf": None, 
        "cep": None, 
        "email": None
    }
                       
    padrao = (
        r'PRESTADOR\s*DE\s*SERVI[CÇ]OS'
        r'\s*(.*?)\s*'
        r'TOMADOR\s*DE\s*SERVI[CÇ]OS'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()

    padrao = (
        r'Nome\/Raz[aâãáà]o\s*Social:'
        r'\s*(.*?)\s*'
        r'CPF\/CNPJ:'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['razao_social'] = match.group(1).strip()

    padrao = (
        r'CPF\/CNPJ:'
        r'\s*(.*?)\s*'
        r'Inscri[cç][aãáàâ]o\s*Municipal:'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['cnpj'] = match.group(1).strip()

    padrao = (
        r'Inscri[cç][aãáàâ]o\s*Municipal:'
        r'\s*(.*?)\s*'
        r'Endere[cç]o:'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['inscricao_municipal'] = match.group(1).strip()

    padrao = (
        r'Endere[cç]o:'
        r'\s*(.*?)\s*'
        r'CEP:'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        bloco = match.group(1).strip()
        partes = re.split(r'[\-]+', bloco)
        partes = [p.strip() for p in partes if p.strip()]
        dados['endereco'] = partes[0]
        complemento = partes[1].replace("*","")
        if complemento:
            dados['endereco'] = f'{partes[0]} {partes[1].replace("*","")}'
        dados['bairro'] = partes[2]

    padrao = (
        r'CEP:'
        r'\s*(.*?)\s*'
        r'Munic[iíìî]pio:'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['cep'] = match.group(1).strip()

    padrao = (
        r'Munic[iíìî]pio:\s*(.*?)\s*UF:\s*([A-Z]{2})\s*'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        dados['municipio'] = match.group(1).strip()
        dados['uf'] = match.group(2).strip()
    
    return dados

def pegar_dados_tomador(texto):
    dados = {"razao_social": None, "cnpj": None}
    
    padrao = (
        r'TOMADOR\s*DE\s*SERVI[CÇ]OS'
        r'\s*(.*?)\s*'
        r'DISCRIMINA[CÇ][AÃÀÁÂ]O\s*DOS\s*SERVI[CÇ]OS'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()

    padrao = (
        r'Nome\/Raz[aâãáà]o\s*Social:'
        r'\s*(.*?)\s*'
        r'CPF\/CNPJ:'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['razao_social'] = match.group(1).strip()


    padrao = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
    match = re.search(padrao, bloco_completo)
    if match: dados["cnpj"] = match.group()

    return dados

def pegar_discriminacao_servico(texto):
    padrao = (
        r'DISCRIMINA[CÇ][AÃÀÁÂ]O\s*DOS\s*SERVI[CÇ]OS\s*Descri[cç][aãáàâ]o:'
        r'\s*(.*?)\s*'
        r'Tribut[aáàâã]vel'
    )
    match = re.search(padrao, texto, re.S | re.I)
    if not match: return None
    return match.group(1).strip()

def pegar_valores(texto):
    dados = {
        "bruto": None, "liquido": None, 
        "ir": None, "pis": None, "cofins": None, "csll": None,
        "inss": None, "iss": None
    }

    match = re.search(r"VALOR\s*TOTAL\s*DA\s*NOTA\s*=\s*R\s*\$\s*(\d[\d\.]*,\d{2})\s*", texto, re.S | re.I)
    if match: dados['bruto'] = match.group(1)
                
    padrao = (
        r'CSLL'
        r'\s*(.*?)\s*'
        r'VALOR\s*TOTAL\s*DA\s*NOTA\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()

    valores = re.findall(r"R\s*\$\s*(\d[\d\.]*,\d{2})", bloco_completo)
    if valores:
        dados['pis'] = valores[0]
        dados['cofins'] = valores[1]
        dados['inss'] = valores[2]
        dados['ir'] = valores[3]
        dados['csll'] = valores[4]
                
    padrao = (
        r'Valor\s*do\s*Iss:'
        r'\s*(.*?)\s*'
        r'OUTRAS\s*INFORMA[CÇ][OÒÓÕÔ]ES\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()

    valores = re.findall(r"(\d[\d\.]*,\d{2})", bloco_completo)
    if valores:
        dados['iss'] = valores[-1]

    return dados

def pegar_dados_servico(texto):
    dados = {"codigo": None, "descricao": None}
        
    padrao = (
        r'Tribut[aáàâã]vel'
        r'\s*(.*?)\s*'
        r'PIS\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()
    linhas = [l.strip() for l in bloco_completo.split('\n') if l.strip()]
    bloco = linhas[1].strip()
    padrao = r'(.*?)\s*\d+\s*'
    match = re.search(padrao, bloco, re.I | re.S)
    if match: 
        dados['descricao'] = match.group(1).strip()

    return dados