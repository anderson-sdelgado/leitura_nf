import re
from lib.limpar_cnpj import formatar_cnpj, limpar_cnpj
from lib.converter_moeda import extrair_valor
from lib.converter_estado import buscar_uf

def leitura_sistema_atende_net(texto: str):

    # print("----------- NOTA ATENDE -----------")
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
    nota["ID_DOC"] = pegar_chave_acesso(texto) # ID do documento na view. Idem V_NF_SERV.
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
        
    print("----------- NOTA SISGISSWEB -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("-----------------------------------")

def pegar_chave_acesso(texto):
    padrao = (
        r'Chave\s*de\s*Acesso'
        r'\s*(?:.*?)\s*(\d+)\s*'
        r'Data\s*Fato\s*Gerador'
    )
    match = re.search(padrao, texto, re.I | re.S)
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
    padrao = r'(SECRETARIA.*?)\s{3}'
    match = re.search(padrao, texto, re.I | re.S)
    if match: return match.group(1).strip()
    return None

def pegar_numero_nota(texto):
    padrao = (
        r'Situa[cç][aâãáà]o'
        r'\s*(?:.*?)\s{3}(\d+)\s*(?:.*?)\s*?'
        r'Data\s*Fato\s*Gerador'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    return match.group(1).strip()

def pegar_data_hora_emissao(texto):
    padrao = r'Data\s*\/\s*Hora\s*Emiss[aâãáà]o\s*(?:.*?)(\d{2}/\d{2}/\d{4}),\s*(\d{2}:\d{2})'
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    data = match.group(1)
    hora = match.group(2)
    return f'{data} {hora}'

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
        r'\s*(.*?)\s*'
        r'Nota\s*Fiscal\s*de\s*Servi[cç]o\s*Eletr[oôóòô]nica\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()

    padrao = (
        r'\s*(.*?)\s*'
        r'CNPJ:'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados["razao_social"] = match.group(1).strip()

    padrao = (
        r'CNPJ:'
        r'\s*(.*?)\s*'
        r'N[uúùû]mero\s*da\s*NFS-e\s*'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados["cnpj"] = match.group(1).strip()

    padrao = (
        r'Insc.\s*Municipal:\s*'
        r'\s*(.*?)\s*'
        r'\s*-'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados["inscricao_municipal"] = match.group(1).strip()

    padrao = (
        r'Insc.\s*Estadual:\s*'
        r'\s*(.*?)\s*'
        r'\s*Tipo\s*'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        ie = match.group(1).strip()
        if ie:
            dados["inscricao_estadual"] = ie

    padrao = (
        r'Munic[iíìî]pio:\s*(.*?)\s*-(.*?)$'
    )
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if match: 
        dados["municipio"] = match.group(1).strip()
        dados['uf'] = buscar_uf(match.group(2).strip())

    padrao = (
        r'Situa[cç][aâãáà]o'
        r'\s*(.*?)\s{3}\d+\s*'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados["endereco"] = match.group(1).strip()

    padrao = r'CEP:\s*([\d\.-]+)'
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados["cep"] = match.group(1).strip().replace(".", "")

    padrao = (
        r'Bairro:\s*(.*?)$'
    )
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if match: dados["bairro"] = match.group(1).strip()

    return dados

def pegar_dados_tomador(texto):
    dados = {"razao_social": None, "cnpj": None}
    padrao = (
        r'TOMADOR\s*DO\s*SERVI[CÇ]O'
        r'\s*(.*?)\s*'
        r'DESCRI[CÇ][AÃÁÀÂ]O\s*DOS\s*SERVI[CÇ]OS\s*PRESTADOS'
    )
    match = re.search(padrao, texto, re.S | re.I)
    if not match: return dados
    
    bloco_completo = match.group(1)

    padrao = (
        r'CPF/CNPJ'
        r'\s*(.*?)\s{3}(.*?)\s*'
        r'Endere[cç]o'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        dados["razao_social"] = match.group(1).strip()
        dados['cnpj'] = match.group(2).strip()
    return dados 

def pegar_discriminacao_servico(texto):
    padrao = (
        r'Descri[cç][aâãáà]o\s*do\s*Servi[cç]o:'
        r'\s*(.*?)\s*'
        r'Valor\s*Total\s*'
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
    padrao = (
        r'ISSQN'
        r'\s*(.*?)\s*'
        r'Descri[cç][aâãáà]o\s'
    )
    match = re.search(padrao, texto, re.S | re.I)
    if not match: return dados
    
    bloco_completo = match.group(1)
    valores = re.findall(r"\d[\d\.]*,\d{2}", bloco_completo)
    if valores:
        dados['bruto'] = valores[0]
        dados['iss'] = valores[3]
        dados['ir'] = valores[4]
        dados['inss'] = valores[5]
        dados['csll'] = valores[6]
        dados['cofins'] = valores[7]
        dados['pis'] = valores[8]
        dados['liquido'] = valores[-1]

    return dados

def pegar_dados_servico(texto):
    dados = {"codigo": None, "descricao": None}
    padrao = (
        r'NBS:'
        r'\s*(.*?)\s*'
        r'Descri[cç][aâãáà]o\s*do\s*Servi[cç]o:'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()

    dados['descricao'] = bloco_completo
    dados['codigo'] = bloco_completo[4:9]
    return dados