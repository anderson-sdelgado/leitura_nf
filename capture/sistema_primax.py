import re
from lib.limpar_cnpj import formatar_cnpj, limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_sistema_primax(texto: str):

    # print("----------- NOTA PRIMAX -----------")
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
    nota["COD_PART"] = prestador['cnpj'] # CNPJ/CPF do fornecedor (prestador) - somente números. Vide V_NF_SERV.PS_CNPJ_CPF.
    nota["COD_MOD"] = "99" # Código do modelo de documento fiscal para registro. Fixo "99".
    nota["SERIE"] = "A" # Série do documento fiscal para registro. Fixo "A".
    nota["DTINSERT"] = None # Data da inclusão no SE Suite. Idem V_NF_SERV.
    nota["DTUPDATE"] = None # Data da alteração no SE Suite. Idem V_NF_SERV.
    nota["ID_DOC"] = pegar_codigo_verificacao(texto) # ID do documento na view. Idem V_NF_SERV.
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
    nota["VL_BRUTO"] = extrair_valor(financeiro["bruto"]) # Valor bruto. Idem V_NF_SERV. 
    nota["VL_LIQ"] = extrair_valor(financeiro["liquido"])# Valor líquido. Idem V_NF_SERV.
    nota["VL_PIS"] = extrair_valor(financeiro["pis"]) # Valor do PIS. Idem V_NF_SERV.
    nota["VL_COFINS"] = extrair_valor(financeiro["cofins"]) # Valor da Cofins. Idem V_NF_SERV.
    nota["VL_IR"] = extrair_valor(financeiro["ir"]) # Valor do IR. Idem V_NF_SERV.
    nota["VL_INSS"] = extrair_valor(financeiro["inss"]) # Valor do INSS. Idem V_NF_SERV.
    nota["VL_CSLL"] = extrair_valor(financeiro["csll"]) # Valor da CSLL. Idem V_NF_SERV.
    nota["VL_ISS"] = extrair_valor(financeiro["iss"]) # Valor do ISS. Idem V_NF_SERV.
    nota["COD_SERVICO"] = servico["codigo"] # Código do serviço. Idem V_NF_SERV.
    nota["COD_SERVICO_ORIGINAL"] = servico["descricao"] # Código do serviço - informação original. Idem V_NF_SERV.
    
    print("----------- NOTA PRIMAX -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("--------------------------------------")

def pegar_codigo_verificacao(texto):
    
    padrao = (
        r'Chave\s*de\s*Seguran[cç]a'
        r'\s*(.*?)\s*'
        r'Dados\s*do\s*Tomador\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    bloco_completo = match.group(1).strip()

    padrao = (
        r'\s*\d+\s*de\s*\d+'
        r'\s*(.*?)$'                       
    )

    match = re.search(padrao, bloco_completo, re.I | re.M)
    if not match: return None
    return match.group(1).strip()

def pegar_prefeitura(texto):
    padrao = r'(PREFEITURA.*?)\s{3}'
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    return match.group(1).strip()

def pegar_secretaria(texto):
    padrao = r'(SECRETARIA.*?)\s{3}'
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    return match.group(1).strip()

def pegar_numero_nf(texto):
        
    padrao = (
        r'Chave\s*de\s*Seguran[cç]a'
        r'\s*(.*?)\s*'
        r'Dados\s*do\s*Tomador\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    bloco_completo = match.group(1).strip()

    match = re.search(r'\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}\s+\d{2}/\d{4}\s+\d+\s+(\d+)', bloco_completo)
    if match: return match.group(1)
    return None

def pegar_data_hora_emissao(texto):
        
    padrao = (
        r'Chave\s*de\s*Seguran[cç]a'
        r'\s*(.*?)\s*'
        r'Dados\s*do\s*Tomador\s*'
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
        r'Dados\s*do\s*Contribuinte'
        r'\s*(.*?)\s*'
        r'NOTA\s*FISCAL\s*DE\s*SERVI[CÇ]OS\s*ELETR[OÓÒÕÔ]NICA\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    bloco_completo = match.group(1).strip()

    padrao = (
        r'CPF/CNPJ'
        r'\s*(.*?)\s\s\s(.*?)\s*'
        r'Inscri[cç][aâãáà]o\s*'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        dados['razao_social'] = match.group(1).strip()
        dados['cnpj'] = match.group(2).strip()
            
    padrao = (
        r'(\d+)(?:\s+(\d+))?\s+([\w\.-]+@[\w\.-]+)\s+'
        r'Endere[ç]o\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if match: 
        dados['inscricao_municipal'] = match.group(1).strip()
        dados['inscricao_estadual'] = match.group(2).strip() if match.group(2) else None
        dados['email'] = match.group(3).strip()

    padrao = (
        r'Bairro'
        r'\s*(.*?)\s\s\s(.*?)\s*'
        r'Cidade\/UF\s*'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        dados['endereco'] = match.group(1).strip()
        dados['bairro'] = match.group(2).strip()

    
    padrao = (
        r'DDD\/Fone'
        r'\s*(.*?)\/\s*([A-Z]{2})\s*(\d{5}-\d{3})\s*'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        dados['municipio'] = match.group(1).strip()
        dados['uf'] = match.group(2).strip()
        dados['cep'] = match.group(3).strip()

    return dados

def pegar_dados_tomador(texto):
    dados = {"razao_social": None, "cnpj": None}
                
    padrao = (
        r'Dados\s*do\s*Tomador\s*'
        r'\s*(.*?)\s*'
        r'Descri[cç][aâãáà]o\s*do\s*Servi[cç]o\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    bloco_completo = match.group(1).strip()

    padrao = (
        r'CPF/CNPJ'
        r'\s*(.*?)\s\s\s(.*?)\s*'
        r'Inscri[cç][aâãáà]o\s*'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        dados['razao_social'] = match.group(1).strip()
        dados['cnpj'] = match.group(2).strip()
            
    return dados

def pegar_discriminacao_servico(texto):
                    
    padrao = (
        r'Descri[cç][aâãáà]o\s*do\s*Servi[cç]o\s*'
        r'\s*(.*?)\s*'
        r'Base\s*de\s*C[aâãáà]lculo\s*das\s*Reten[cç][oóòõô]es\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    return match.group(1).strip()


def pegar_valores(texto):
    dados = {
        "bruto": None, 
        "liquido": None, 
        "inss": None, 
        "ir": None, 
        "csll": None, 
        "cofins": None, 
        "pis": None, 
        "iss": None
    }

    match = re.search(r'Valor\s*do\s*Servi[cç]o\s*R\$\s+([\d.,]+)', texto)
    if match: dados["bruto"] = match.group(1)

    match = re.search(r'Vlr\s*L[ií]quido\s*NFS-e\s+([\d.,]+)', texto)
    if match: dados["liquido"] = match.group(1)

    match = re.search(r'ISSQN\s*([\d.,]+)\s*Vlr\s*L[ií]quido', texto)
    if match: dados["iss"] = match.group(1)

    match = re.search(r'\(PIS\)\s*R\$\s+([\d.,]+)', texto)
    if match: dados["pis"] = match.group(1)

    match = re.search(r'\(COFINS\)\s*R\$\s+([\d.,]+)', texto)
    if match: dados["cofins"] = match.group(1)

    match = re.search(r'\(CSLL\)\s*R\$\s+([\d.,]+)', texto)
    if match: dados["csll"] =match.group(1)

    match = re.search(r'\(IRRF\)\s*R\$\s+([\d.,]+)', texto)
    if match: dados["ir"] = match.group(1)

    match = re.search(r'\(INSS\)\s*R\$\s+([\d.,]+)', texto)
    if match: dados["inss"] = match.group(1)

    return dados

def pegar_dados_servico(texto):
    dados = {"codigo": None, "descricao": None}

    padrao = (
        r'\s*Aliq.\s*\(\%\)\s*B.\s*C[aâãáà]lculo\s*'
        r'\s*(.*?)\s*'
        r'iNFORMA[CÇ][OÓÒÕÔ]ES\sADICIONAIS*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    bloco_completo = match.group(1).strip()
    padrao = r'\d{1,3}(?:\.\d{3})*,\d+'
    bloco_completo = re.sub(padrao, '', bloco_completo)
    bloco_completo = bloco_completo[:8] + " - " + bloco_completo[8:]
    dados["descricao"] = bloco_completo
    dados["codigo"] = bloco_completo[:5]
    return dados