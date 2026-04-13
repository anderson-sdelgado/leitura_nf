import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_municipio_baureri(texto: str):

    # print("----------- NOTA BARUERI -----------")
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
        
    print("----------- NOTA SENIOR -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("-----------------------------------")

def pegar_codigo(texto):
    padrao = (
        r'Internet,\s*no\s*Endere[cç]o:'
        r'\s*(.*?)\s*\d+\s*$'
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
    padrao = r'(SECRETARIA.*?)\s{3}'
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    return match.group(1).strip()

def pegar_numero_nota(texto):
    padrao = (
        r'Internet,\s*no\s*Endere[cç]o:'
        r'\s*(?:.*?)\s*(\d+)\s*$'
    )
    match = re.search(padrao, texto, re.I | re.M)
    if not match: return None
    return match.group(1).strip()

def pegar_data_hora_emissao(texto):
        
    padrao = (
        r'Data\s*Emiss[aâãáà]o\s*Hora\s*Emiss[aâãáà]o'
        r'\s*(.*?)\s*'
        r'SERVICOS\s*E\s*FATURA'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    bloco_completo = match.group(1).strip()

    match = re.search(r'\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}', bloco_completo)
    if match: return match.group()
    return None

def pegar_dados_prestador(texto):
    dados = {
        "razao_social": None, "cnpj": None, "inscricao_municipal": None, 
        "inscricao_estadual": None, "municipio": None, "uf": None, "cep": None,
        "endereco": None, "bairro": None, "email": None
    }
            
    padrao = (
        r'Prestador\s*de\s*Servi[cç]os'
        r'\s*(.*?)\s*'
        r'Nome\s*Tomador\s*de\s*Servi[cç]os\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados
    bloco_completo = match.group(1).strip()
    linhas = [l.strip() for l in bloco_completo.split('\n') if l.strip()]
        
    dados['razao_social'] = linhas[0].strip()
    dados['endereco'] = linhas[1].strip()
    dados['bairro'] = linhas[2].strip()

    padrao = (
        r'CEP'
        r'\s*(.*?)\s-\s*(.*?)\s*-\s*(.*?)\s*'
        r'CNPJ\/CPF\s*'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        dados['cep'] = match.group(1).strip()
        dados['municipio'] = match.group(2).strip()
        dados['uf'] = match.group(3).strip()

    padrao = (
        r'CNPJ\/CPF\s*'
        r'\s*(.*?)\s*'
        r'Inscri[cç][aãáàâ]o\s*Municipal\s*'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['cnpj'] = match.group(1).strip()

    padrao = (
        r'Inscri[cç][aãáàâ]o\s*Municipal\s*'
        r'\s*(.*?)\s*'
        r'Telefone\s*'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['inscricao_municipal'] = match.group(1).strip()

    padrao = r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}'
    match = re.search(padrao, bloco_completo)
    if match: dados["email"] = match.group().lower()

    return dados

def pegar_dados_tomador(texto):
    dados = {"razao_social": None, "cnpj": None}
    
    padrao = (
        r'CPF\/CNPJ\s*'
        r'\s*(.*?)\s{3}(.*?)\s*'
        r'Endere[cç]o\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if match: 
        dados['razao_social'] = match.group(1).strip()
        dados['cnpj'] = match.group(2).strip()

    return dados

def pegar_discriminacao_servico(texto):
    padrao = (
        r'DISCRIMINA[CÇ][AÁÀÃÂ]O\s*DOS\s*SERVI[CÇ]OS\s*E\s*INFORMA[CÇ][OÓÒÔÕ]ES\s*RELEVANTES'
        r'\s*(.*?)\s*'
        r'VALORES\s*DE\s*REPASSE\s*A\s*TERCEIROS\s*'
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
        r'VALOR\s*TOTAL\s*DA\s*NOTA\s*(\d[\d\.]*,\d{2})\s*$'
    )
    match = re.search(padrao, texto,  re.I | re.M)
    if match: 
        dados["bruto"] = match.group(1).strip()

    padrao = (
        r'CSLL\s*'
        r'\s*(.*?)\s*'
        r'VALOR\s*TOTAL\s*DA\s*NOTA\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if match: 
        valores = re.findall(r"(\d[\d\.]*,\d{2})", match.group(1).strip())
        if valores:
            dados['ir'] = valores[0]
            dados['pis'] = valores[1]
            dados['cofins'] = valores[2]
            dados['csll'] = valores[2]
    
    padrao = (
        r'Forma\s*Pagamento\s*'
        r'\s*(.*?)\s*'
        r'Valor\s*por\s*Extenso\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if match: 
        valores = re.findall(r"(\d[\d\.]*,\d{2})", match.group(1).strip())
        if valores:
            dados['liquido'] = valores[0]
            
    return dados

def pegar_dados_servico(texto):
    dados = {"codigo": None, "descricao": None}
    print(texto)
    padrao = (
        r'Valor\s*Total'
        r'\s*(?:\d+)\s{3}(.*?)\s*(\d+)\s*(.*?)\s*'
        r'DISCRIMINA[CÇ][AÁÀÃÂ]O\s*DOS\s*SERVI[CÇ]OS\s*E\s*INFORMA[CÇ][OÓÒÔÕ]ES\s*RELEVANTES'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if match: 
        codigo = match.group(2).strip()
        descricao = match.group(1).strip()
        dados['descricao'] = f'{codigo} - {descricao}'
        dados['codigo'] = f'{codigo[:2]}.{codigo[2:4]}'
    return dados