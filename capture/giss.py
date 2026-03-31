import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def limpar_linha(linha):
    return re.sub(r'^\d+:\s*', '', linha).strip()

def leitura_giss(texto: str):
        
    # print("----------- NOTA GISS -----------")
    # print(texto)
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
    nota["PS_INSC_MUNIC"] = prestador['inscricao'] # Inscrição municipal do prestador de serviço. Idem V_NF_SERV.
    nota["PS_INSC_EST"] = None # Inscrição estadual do prestador de serviço. Idem V_NF_SERV.
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
    nota["COD_SERVICO_ORIGINAL"] = servico["descricao_completa"] # Código do serviço - informação original. Idem V_NF_SERV.

    print("----------- NOTA GISS -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("-----------------------------------")

def pegar_prefeitura(texto):
    padrao = (
        r'\s*(.*?)\s*'
        r'NFS-e'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    return match.group(1).strip()

def pegar_secretaria(texto):
    padrao = r'(SECRETARIA.*?)\s*C[oõóòô]digo'
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    return match.group(1).strip()

def pegar_codigo_verificacao(texto):
    padrao = (
        r'ELETR[OÔ]NICA'
        r'\s*(.*?)\s*'
        r'Emiss[aãáàâ]o'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    conteudo = match.group(1).strip()
    padrao = r'\b[A-Z0-9]{9}\b'
    matches = re.findall(padrao, conteudo.upper())
    codigos_filtrados = [m for m in matches if not m.isdigit()]
    return codigos_filtrados[0]

def pegar_numero_nf(texto):
    padrao = r'NFS-e'r'\s*(.*)$'
    match = re.search(padrao, texto, re.I | re.M)
    if not match: return None
    return match.group(1).strip()

def pegar_data_hora_emissao(texto):
    padrao = (
        r'Emiss[aãáàâ]o\s*'
        r'\s*(.*?)\s*'
        r'RPS'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    conteudo = match.group(1).strip()
    match = re.search(r'(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2})', conteudo)
    if not match: return None
    return match.group(1)

def pegar_dados_prestador(texto):
    dados = {
        "razao_social": None, 
        "cnpj": None, 
        "inscricao": None,
        "municipio": None,
        "uf": None,
        "endereco": None,
        "bairro": None,
        "cep": None,
        "email": None 
    }
    padrao = (
        r'Prestador\s*de\s*Servi[cç]o'
        r'\s*(.*?)\s*'
        r'Tomador\s*de\s*Servi[cç]o'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()

    padrao = r'Nome/Raz[aâãáà]o\s*Social:\s*(.*)$'
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if match: dados["razao_social"] = match.group(1).strip()

    padrao = r'CPF/CNPJ:\s*(.*?)\s*Inscri[cç][aâãáà]o'
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados["cnpj"] = match.group(1).strip()

    padrao = r'Inscri[cç][aâãáà]o\s*(.*?)\s*Nome/Raz[aâãáà]o\s*Social'
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados["inscricao"] = match.group(1).strip()

    padrao = r'Endere[cç]o\s*(.*?)\s*N[uú]mero'
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: endereco = match.group(1).strip()

    padrao = r'N[uú]mero:\s*(.*?)\s*Complemento'
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: num = match.group(1).strip()

    padrao = r'Complemento:\s*(.*?)\s*Bairro'
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: complemento = match.group(1).strip()

    partes = [item for item in [endereco, num, complemento] if item and str(item).strip()]
    dados['endereco'] = ", ".join(partes)

    padrao = r'Bairro:\s*(.*?)\s*CEP'
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['bairro'] = match.group(1).strip()

    match = re.search(r'CEP:\s*([\d-]{8,9})', bloco_completo)
    if match: dados["cep"] = match.group(1).strip()

    padrao = r'Munic[ií]pio:\s*(.*?)\s*UF'
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['municipio'] = match.group(1).strip()

    match = re.search(r'UF:\s*([A-Z]{2})', bloco_completo)
    if match: dados["uf"] = match.group(1).strip()

    match = re.search(r'E-mail:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', bloco_completo)
    if match: dados["email"] = match.group(1).strip()

    return dados

def pegar_dados_tomador(texto):
    dados = {
        "razao_social": None,
        "cnpj": None
    }
    padrao = (
        r'Tomador\s*de\s*Servi[cç]o'
        r'\s*(.*?)\s*'
        r'Atividade'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()

    padrao = r'Nome/Raz[aâãáà]o\s*Social:'r'\s*(.*)$'
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if match: dados["razao_social"] = match.group(1).strip()

    padrao = r'CPF/CNPJ:\s*(.*?)\s*Inscri[cç][aâãáà]o'
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados["cnpj"] = match.group(1).strip()

    return dados

def pegar_discriminacao_servico(texto):
    padrao = (
        r'Discrimina[cç][aâãáà]o\s*do\s*Servi[cç]o'
        r'\s*(.*?)\s*'
        r'Tributos\s*Federais'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    return match.group(1).strip()

def pegar_valores(texto):
    dados = {
        "bruto": None, "liquido": None, 
        "ir": None, "pis": None, "cofins": None, "csll": None,
        "inss": None, "iss": None
    }
    padrao = (
        r'Tributos\s*Federais'
        r'\s*(.*?)\s*'
        r'Outras\s*Informa[cç][oõóòô]es'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados
    
    bloco_completo = match.group(1).strip()

    padrao = r'Valor\s*do\s*Servi[cç]o'r'\s*(.*)$'
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if match: dados["bruto"] = match.group(1).strip()

    padrao = r'Valor\s*L[ií]quido'r'\s*(.*)$'
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if match: dados["liquido"] = match.group(1).strip()

    padrao = (
        r'Municipal'
        r'\s*(.*?)\s*'
        r'Identifica[cç][aâãáà]o'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        texto = match.group(0)
        linhas = texto.split('\n')
        for i, texto_linha in enumerate(linhas):
            if i == 1:
                pis = texto_linha[1:9]
                cofins = texto_linha[10:20]
                inss = texto_linha[18:28]
                ir = texto_linha[28:36]
                csll = texto_linha[36:45]
                dados["pis"] = pis.strip()
                dados["cofins"] = cofins.strip()
                dados["inss"] = inss.strip()
                dados["ir"] = ir.strip()
                dados['csll'] = csll.strip()

    padrao = (
        r'Nacional'
        r'\s*(.*?)\s*'
        r'ISSQN\s*a\s*Reter'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match:
        texto_iss = match.group(1)
        padrao = r"ISSQN\s+([\d\.,]+)"
        match = re.search(padrao, texto_iss)
        if match: dados['iss'] = match.group(1).strip()
    return dados

def pegar_dados_servico(texto):
    dados = {
        "codigo":  None,
        "descricao_completa": None
    }
    padrao = (
        r'Atividade\s*Econ[oõóòô]mica'
        r'\s*(.*?)\s*'
        r'Discrimina[cç][aâãáà]o\s*do\s*Servi[cç]o'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados
    
    bloco_completo = match.group(1).strip()
    dados['descricao_completa'] = bloco_completo.strip()
    
    match = re.search(r'\s*(.*?)\s*/\s*', bloco_completo, re.I | re.M)
    if match: dados["codigo"] = match.group(1).strip()
    
    return dados