import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_municipio_campinas(texto: str):

    # print("------- NOTA CAMPINAS --------")
    # print(f"{texto}")
    # print("------------------------------")

    cabecalho = pegar_dados_cabecalho(texto)
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
    nota["NRO_NF"] = cabecalho['nro'] # Número da NF. Idem V_NF_SERV.
    nota["DT_EMISS"] = cabecalho['data'] # Data de emissão da NF. Idem V_NF_SERV.
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
        r'EMITENTE\s*PRESTADOR\s*DO\s*SERVI[CÇ]O'
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

def pegar_dados_cabecalho(texto):
    dados = {
        "nro": None, 
        "data": None, 
    }
    padrao = (
        r'Data\s*e\s*hora\s*de\s*emiss[aãáàâ]o'
        r'\s*(.*?)\s*'
        r'C[oóòôõ]digo\s*de\s*Verifica[cç][aãáàâ]o'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados
    bloco_completo = match.group(1).strip()

    linhas = [l.strip() for l in bloco_completo.split('\n') if l.strip()]
    bloco = linhas[1].strip()
    padrao = r'(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})\s*(?:\d{2}/\d{4})\s*(.*)\s*\/\s*'
    match = re.search(padrao, bloco, re.I | re.S)
    if match: 
        dados['data'] = match.group(1).strip()
        dados['nro'] = match.group(2).strip()

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
        r'EMITENTE\s*PRESTADOR\s*DO\s*SERVI[CÇ]O'
        r'\s*(.*?)\s*'
        r'TOMADOR\s*DO\s*SERVI[CÇ]O'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()

    padrao = (
        r'Telefone'
        r'\s*(.*?)\s+(.*?)\s+(?:.*?)\s*'
        r'Nome\s*\/\s*Nome\s*Empresarial'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        dados['cnpj'] = match.group(1).strip()
        dados['inscricao_municipal'] = match.group(2).strip()

    padrao = (
        r'E-mail'
        r'\s*(.*?)\s+([\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,})\s*'
        r'Endere[cç]o'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        dados['razao_social'] = match.group(1).strip()
        dados['email'] = match.group(2).strip()

    padrao = (
        r'CEP\s*'
        r'(.*?)\s+(\w+)\s*/\s*([A-Z]{2}).*?(\d{5}-\d{3})'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        dados['endereco'] = match.group(1).strip()
        dados['municipio'] = match.group(2).strip()
        dados['uf'] = match.group(3).strip()
        dados['cep'] = match.group(4).strip()

    return dados

def pegar_dados_tomador(texto):
    dados = {"razao_social": None, "cnpj": None}
                    
    padrao = (
        r'TOMADOR\s*DO\s*SERVI[CÇ]O'
        r'\s*(.*?)\s*'
        r'SERVI[CÇ]O\s*PRESTADO'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()

    padrao = (
        r'Telefone'
        r'\s*(.*?)\s+(?:.*?)\s+(?:.*?)\s*'
        r'Nome\s*\/\s*Nome\s*Empresarial'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        dados['cnpj'] = match.group(1).strip()

    padrao = (
        r'E-mail'
        r'\s*(.*?)\s+(?:[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,})\s*'
        r'Endere[cç]o'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        dados['razao_social'] = match.group(1).strip()

    return dados

def pegar_discriminacao_servico(texto):
    padrao = (
        r'\s*QUANTIDADE\s*E\s*O\s*PRE[CÇ]O\s*UNIT[AÁÀÃÃ]RIO\)'
        r'\s*(.*?)\s*'
        r'TRIBUTA[CÇ][AÁÀÃÃ]O\s*MUNICIPAL'
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
        r'C[AÁÀÃÃ]LCULO\s*DO\s*ISSQN'
        r'\s*(.*?)\s*'
        r'RETEN[CÇ][OÒÓÔÕ]ES'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if match: 
        bloco_calculo = match.group(1).strip()
        valores = re.findall(r"(\d[\d\.]*,\d{2})", bloco_calculo)
        if valores:
            dados['bruto'] = valores[0]
            dados['iss'] = valores[-1]
                           
    padrao = (
        r'RETEN[CÇ][OÒÓÔÕ]ES'
        r'\s*(.*?)\s*'
        r'VALOR\s*TOTAL'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if match: 
        bloco_retencoes = match.group(1).strip()
        valores = re.findall(r"(\d[\d\.]*,\d{2})", bloco_retencoes)
        if valores:
            dados['ir'] = valores[1]
            dados['pis'] = valores[2]
            dados['cofins'] = valores[3]
            dados['inss'] = valores[4]
            dados['csll'] = valores[5]
                           
    padrao = (
        r'VALOR\s*TOTAL'
        r'\s*(.*?)\s*'
        r'INFORMA[CÇ][OÒÓÔÕ]ES'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if match: 
        bloco_retencoes = match.group(1).strip()
        valores = re.findall(r"(\d[\d\.]*,\d{2})", bloco_retencoes)
        if valores:
            dados['liquido'] = valores[-1]

    return dados

def pegar_dados_servico(texto):
    dados = {"codigo": None, "descricao": None}
        
    padrao = (
        r'SERVI[CÇ]O\s*PRESTADO'
        r'\s*(.*?)\s*'
        r'DESCRI[CÇ][AÁÀÃÃ]O\s*DO\s*SERVI[CÇ]O'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()
    
    padrao = (
        r'Servi[cç]o'
        r'\s*(.*?)\s*'
        r'Local\s*da\s*presta[cç][aãáàâ]o'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()
    
    dados['descricao'] = bloco_completo
    dados['codigo'] = bloco_completo[:5]

    return dados