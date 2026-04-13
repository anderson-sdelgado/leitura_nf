import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_municipio_cajamar(texto: str):

    # print("----------- NOTA CAJAMAR -----------")
    # print(f"{texto}")
    # print("-------------------------")

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
    nota["PREFEIT"] = pegar_prefeitura(texto) # Nome da prefeitura. Idem V_NF_SERV.
    nota["SECRET_PREFEIT"] = pegar_secretaria(texto) # Secretaria da prefeitura. Idem V_NF_SERV.
    nota["NRO_NF"] = pegar_numero_nota(texto) # Número da NF. Idem V_NF_SERV.
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
        
    print("---------- NOTA CAJAMAR -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("-----------------------------------")

def pegar_codigo(texto):
    padrao = (
        r'C[oóòôõ]d.\s*Verifica[cç][aâãáà]o:\s*'
        r'\s*(.*?)$'
    )
    match = re.search(padrao, texto, re.I | re.M)
    if not match: return None
    return match.group(1).strip()

def pegar_prefeitura(texto):
    padrao = r'(PREFEITURA.*?)\s{3}'
    match = re.search(padrao, texto, re.I | re.S)
    if match: return match.group(1).strip()
    padrao = r'(MUNIC[IÍ]PIO.*?)\s{3}'
    match = re.search(padrao, texto, re.I | re.S)
    if match: return match.group(1).strip()
    return None

def pegar_secretaria(texto):
    padrao = r'(SECRETARIA.*?)\s*C[oóòôõ]d.\s*Verifica[cç][aâãáà]o:\s*'
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    return match.group(1).strip()

def pegar_numero_nota(texto):
    padrao = (
        r'Nº\s*NFSe:\s*(\d+)\s*$'
    )
    match = re.search(padrao, texto, re.I | re.M)
    if not match: return None
    return match.group(1).strip()

def pegar_data_hora_emissao(texto):
    padrao = (
        r'Data\s*Emiss[aâãáà]o:\s*(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    return match.group(1).strip()

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
        r'DADOS\s*DO\s*PRESTADOR'
        r'\s*(.*?)\s*'
        r'DADOS\s*DO\s*TOMADOR'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()

    padrao = (
        r'Raz[aâãáà]o\s*Social:'
        r'\s*(.*?)\s*'
        r'CNPJ:'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['razao_social'] = match.group(1).strip()

    padrao = (
        r'CNPJ:'
        r'\s*(.*?)\s*'
        r'Inscri[cç][aâãáà]o\s*Municipal:\s*'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['cnpj'] = match.group(1).strip()

    padrao = (
        r'Inscri[cç][aâãáà]o\s*Municipal:\s*(.*?)$'
    )
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if match: dados['inscricao_municipal'] = match.group(1).strip()

    padrao = (
        r'Endere[cç]o:\s*(.*?)\s*-\s*(.*?)$'
    )
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if match: 
        dados['endereco'] = match.group(1).strip()
        dados['bairro'] = match.group(2).strip()

    padrao = (
        r'Munic[iíìî]pio:\s*(.*?)\s*UF:\s*(.*?)$'
    )
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if match: 
        dados['municipio'] = match.group(1).strip()
        dados['uf'] = match.group(2).strip()

    padrao = r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}'
    match = re.search(padrao, bloco_completo)
    if match: dados["email"] = match.group().lower()

    return dados 

def pegar_dados_tomador(texto):
    dados = {"razao_social": None, "cnpj": None}
    padrao = (
        r'DADOS\s*DO\s*TOMADOR'
        r'\s*(.*?)\s*'
        r'DADOS\s*DO\s*INTERMEDIARIO'
    )
    match = re.search(padrao, texto, re.S | re.I)
    if not match: return dados
    
    bloco_completo = match.group(1)
    
    padrao = (
        r'Nome:\s*(.*?)$'
    )
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if match: dados['razao_social'] = match.group(1).strip()
    
    padrao = (
        r'CPF/CNPJ:\s*(.*?)$'
    )
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if match: dados['cnpj'] = match.group(1).strip()

    return dados 

def pegar_discriminacao_servico(texto):
    padrao = (
        r'DESCRI[CÇ][AÁÀÃÃ]O\s*DOS\s*SERVI[CÇ]OS\s*PRESTADOS'
        r'\s*(.*?)\s*'
        r'Tipo\s*de\s*tributa[cç][aâãáà]o:\s*'
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
    padrao = (
        r'TOTAIS'
        r'\s*(.*?)\s*'
        r'INFORMA[CÇ][OÒÓÕÔ]ES\s*ADICIONAIS'
    )
    match = re.search(padrao, texto, re.S | re.I)
    if not match: return dados
    
    bloco_completo = match.group(1)
    print(bloco_completo)
    
    match = re.search(r'Valor\s*dos\s*Servi[cç]os:\s*(\d[\d\.]*,\d{2})', bloco_completo, re.I | re.S)
    if match: dados['bruto'] = match.group(1).strip()

    match = re.search(r'Valor\s*l[iíìî]quido\s*da\s*nota:\s*(\d[\d\.]*,\d{2})', bloco_completo, re.I | re.S)
    if match: dados['liquido'] = match.group(1).strip()

    match = re.search(r'Valor\s*do\s*ISS:\s*(\d[\d\.]*,\d{2})', bloco_completo, re.I | re.S)
    if match: dados['iss'] = match.group(1).strip()

    return dados

def pegar_dados_servico(texto):
    dados = {"codigo": None, "descricao": None}
                
    padrao = (
        r'C[oóòôõ]digo\s*do\s*Servi[cç]o:\s*(.*?)$'
    )
    match = re.search(padrao, texto, re.I | re.M)
    if not match: return dados

    bloco_completo = match.group(1).strip()
    dados['descricao'] = bloco_completo
    dados['codigo'] = f'{bloco_completo[:2]}.{bloco_completo[2:4]}'

    return dados