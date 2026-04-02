import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_sistema_ginfes(texto: str):
        
    # print("----------- NOTA GINFES -----------")
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

    print("----------- NOTA GINFES -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("--------------------------------------")

def pegar_codigo_verificacao(texto):
    padrao = r'C[oóòõô]digo\s*de\s*Verifica[cç][aâãáà]o\s*(.*)$'
    match = re.search(padrao, texto, re.I | re.M)
    if not match: return None
    return match.group(1).strip()
    
def pegar_prefeitura(texto):
    padrao = r'(PREFEITURA.*?)\s*N[uú]mero\s*'
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    return match.group(1).strip()

def pegar_secretaria(texto):
    padrao = r'(SECRETARIA.*?)\s*NFS-e\s*'
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    return match.group(1).strip()

def pegar_numero_nf(texto):
    padrao = r'SERVI[CÇ]O\s*-\s*NFS-e\s*(.*)$'
    match = re.search(padrao, texto, re.I | re.M)
    if not match: return None
    return match.group(1).strip()

def pegar_data_hora_emissao(texto):
    padrao = r'Data\s*e\s*Hora\s*d[ae]\s*Emiss[aâãáà]o\s*(\d{2}/\d{2}/\d{4}).*?(\d{2}:\d{2}:\d{2})'
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
        r'Prestador\s*de\s*Servi[cç]o'
        r'\s*(.*?)\s*'
        r'Tomador\s*de\s*Servi[cç]o'
    )
    match = re.search(padrao, texto, re.IGNORECASE | re.S)
    if not match: return dados
    bloco_completo = match.group(1).strip()

    padrao = r'Raz[aâãáà]oSocial/Nome\s*(.*)$'
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if match: dados["razao_social"] = match.group(1).strip()

    padrao = (
        r'CNPJ/CPF\s*'
        r'\s*(.*?)\s*'
        r'\s*[iI]nscri[cç][aâãáà]o\s*Municipal\s*'
    )
    match = re.search(padrao, bloco_completo)
    if match: dados["cnpj"] = match.group(1).strip()

    padrao = (
        r'\s*[iI]nscri[cç][aâãáà]o\s*Municipal\s*'
        r'\s*(.*?)\s*'
        r'Munic[ií]pio\s*'
    )
    match = re.search(padrao, bloco_completo)
    if match: dados["inscricao_municipal"] = match.group(1).strip()

    padrao = r'Munic[ií]pio\s*(.*?)\s*-\s*([A-Z]{2})$'
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if match: 
        dados["municipio"] = match.group(1).strip()
        dados["uf"] = match.group(2).strip()

    padrao = r'Endere[cç]o\s*e\s*CEP\s*(.*?)\s*-\s*(.*?)\s*CEP:\s*(\d{5}-\d{3})'
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        endereco = match.group(1).strip()
        dados["bairro"] = match.group(2).strip()
        dados['cep'] = match.group(3).strip()

    padrao = r'Complemento \s*(.*?)\s*Telefone\s*'
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: complemento = match.group(1).strip()

    dados['endereco'] = f'{endereco}'
    if complemento: dados['endereco'] = f'{dados['endereco']}, {complemento}'

    padrao = r'\s*e-mail\s*(.*)$'
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if match: dados["email"] = match.group(1).strip()

    padrao = r'\s*e-mail\s*(.*)$'
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if match: dados["email"] = match.group(1).strip()

    return dados

def pegar_dados_tomador(texto):
    dados = {"cnpj": None, "razao_social": None}
    padrao = (
        r'Tomador\s*de\s*Servi[cç]o'
        r'\s*(.*?)\s*'
        r'Discrimina[cç][aâãáà]o\s*do\s*Servi[cç]o'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados
    bloco_completo = match.group(1).strip()

    padrao = r'Raz[aâãáà]oSocial/Nome\s*(.*)$'
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if match: dados["razao_social"] = match.group(1).strip()

    dados["cnpj"] = bloco_completo

    padrao = (
        r'\s*CNPJ/CPF\s*'
        r'\s*(.*?)\s*'
        r'\s*[iI]nscri[cç][aâãáà]o\s*Municipal\s*'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados["cnpj"] = match.group(1).strip()

    return dados

def pegar_discriminacao_servico(texto):
    padrao = (
        r'Discrimina[cç][aâãáà]o\s*do\s*Servi[cç]o'
        r'\s*(.*?)\s*'
        r'C[oóòõô]digo\s*do\s*Servi[cç]o\s*'
    )
    match = re.search(padrao, texto, re.S | re.I)
    if not match: return None
    return match.group(1).strip()

def pegar_valores(texto):
    dados = {
        "pis": None, "cofins": None, "csll": None, 
        "ir": None, "inss": None, "iss": None, 
        "bruto": None, "liquido": None
    }
    padrao = (
        r'Tributos\s*Federais\s*(.*+)'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados
    bloco_completo = match.group(1)

    padrao = (
        r'PIS\s*\(R\$\)\s*(.*?)\s*COFINS\s*\(R\$\)\s*(.*?)\s*IR\s*\(R\$\)\s*(.*?)\s*INSS\s*\(R\$\)\s*(.*?)\s*CSLL\s*\(R\$\)\s*(.*?)'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        dados["pis"] = match.group(1).strip()
        dados["cofins"] = match.group(2).strip()
        dados["ir"] = match.group(3).strip()
        dados["inss"] = match.group(4).strip()
        dados["csll"] = match.group(5).strip()

    padrao = r'Valor\s*do\s*Servi[cç]o\s*R\$\s*(.*?)\s*Natureza\s*'
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['bruto'] = match.group(1).strip()

    padrao = r'Valor\s*L[ií]quido\s*R\$\s*(.*?)\s*\(=\)\s*'
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['liquido'] = match.group(1).strip()

    padrao = r'ISSQN\s*R\$\s*([0-9.,]*)'
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['iss'] = match.group(1).strip()

    return dados

def pegar_dados_servico(texto):
    dados = {"codigo": None, "descricao": None}
    padrao = (
        r'C[oóòõô]digo\s*do\s*Servi[cç]o\s*\/\s*Atividade'
        r'\s*(.*?)\s*'
        r'Detalhamento\s*'
    )
    match = re.search(padrao, texto, re.S | re.I)
    if match: 
        descricao = match.group(1).strip() 
        match = re.search(r'\s*(.*?)\s*\/\s*', descricao, re.IGNORECASE | re.M)
        if match: dados["codigo"] = match.group(1).strip()
        dados['descricao'] = descricao
        
    return dados