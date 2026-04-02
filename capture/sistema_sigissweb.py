import re
from lib.limpar_cnpj import formatar_cnpj, limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_sistema_sigissweb(texto: str):

    # print("----------- NOTA SISGISSWEB -----------")
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
    nota["SECRET_PREFEIT"] = None # Secretaria da prefeitura. Idem V_NF_SERV.
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
        r'\s*(?:\d+\s+\d+|-)\s*(\d+)\s*?'
        r'Dados\s*do\s*Prestador'
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

def pegar_numero_nota(texto):
    padrao = r'Data\s*e\s*Hora\s*da\s*Emiss[aâãáà]o\s*da\s*(\d+)\s*\/'
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    return match.group(1).strip()

def pegar_data_hora_emissao(texto):
    padrao = r'Data\s*e\s*Hora\s*da\s*Emiss[aâãáà]o\s*da\s*(?:.*?)(\d{2}/\d{2}/\d{2})\s(\d{2}:\d{2})'
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
        r'Dados\s*do\s*Prestador'
        r'\s*(.*?)\s*'
        r'Dados\s*do\s*Tomador'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()

    padrao = (
        r'Raz[aâãáà]o\s*Social'
        r'\s*(.*?)\s*'
        r'Nome\s*Fantasia'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['razao_social'] = match.group(1).strip()

    padrao = (
        r'Inscri[cç][aâãáà]o\s*Estadual'
        r'\s+(.*?)\s{3}(.*?)\s{3}(.*?)\s*'
        r'Endere[cç]o'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        dados['cnpj'] = match.group(1).strip()
        dados['inscricao_municipal'] = match.group(2).strip()
        dados['inscricao_estadual'] = match.group(3).strip()

    padrao = (
        r'CEP'
        r'\s+(.*?)\s*-\s*(.*?)\s{3}(.*?)\s*'
        r'Email'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        dados['municipio'] = match.group(1).strip()
        dados['uf'] = match.group(2).strip()
        dados['cep'] = match.group(3).strip()

    padrao = (
        r'N[uúùû]mero'
        r'\s*(.*?)\s{3}(.*?)\s*'
        r'Complemento'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        endereco = f'{match.group(1).strip()}, {match.group(2).strip()}'

    padrao = r"(Bairro\s*.*?\s*Munic[ií]pio)"
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match:
        conteudo = match.group(1)
        linhas = [l.strip() for l in conteudo.split('\n') if l.strip()]
        
        if linhas:
            linha_dados = conteudo.split('\n')[1]
            partes = re.split(r'\s{3,}', linha_dados.strip())
            if len(partes) >= 2:
                complemento = f', {partes[0]}'
                bairro = partes[1]
            else:
                complemento = ""
                bairro = partes[0]

    dados['endereco'] = f'{endereco}{complemento}'
    dados['bairro'] = bairro

    padrao = r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}'
    match = re.search(padrao, bloco_completo)
    if match:
        dados["email"] = match.group().lower()

    return dados

def pegar_dados_tomador(texto):
    dados = {"razao_social": None, "cnpj": None}
    padrao = (
        r'Dados\s*do\s*Tomador'
        r'\s*(.*?)\s*'
        r'Dados\s*do\s*Intermedi[aâãáà]rio'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()

    padrao = (
        r'Raz[aâãáà]o\s*Social'
        r'\s*(.*?)\s*'
        r'CNPJ\s*'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['razao_social'] = match.group(1).strip()

    padrao = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
    match = re.search(padrao, bloco_completo)
    if match: dados["cnpj"] = match.group()

    return dados

def pegar_discriminacao_servico(texto):
    padrao = (
        r'Descri[cç][aâãáà]o\s*do\s*Servi[cç]o'
        r'\s*(.*?)\s*'
        r'IBS\s*'
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
        r'Tributa[cç][aâãáà]o\s*Federal\s*'
        r'\s*(.*?)\s*'
        r'Valor\s*Total\s*da\s*NFS-E'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if match: 
        bloco_completo = match.group(1).strip()
        if bloco_completo:
            valores = re.findall(r"R\$\s*([\d\.,]+)", bloco_completo)
            if valores:
                dados['ir'] = valores[0]
                dados['csll'] = valores[1]
                dados['pis'] = valores[2]
                dados['cofins'] = valores[3]
                dados['inss'] = valores[4]

    padrao = (
        r'Valor\s*Total\s*da\s*NFS-E\s*'
        r'\s*(.*?)\s*'
        r'Informa[cç][oóòõô]es\sComplementares'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if match: 
        bloco_completo = match.group(1).strip()
        valores = re.findall(r"R\$\s*([\d\.,]+)", bloco_completo)
        if valores:
            dados['bruto'] = valores[0]
            dados['iss'] = valores[-2]
            dados['liquido'] = valores[-1]
    return dados

def pegar_dados_servico(texto):
    dados = {"codigo": None, "descricao": None}
    padrao = (
        r'Classifica[cç][aâãáà]o\s*do\s*Servi[cç]o'
        r'\s*(.*?)\s*'
        r'Local\s*da\s*Presta[cç][aâãáà]o\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()

    dados['descricao'] = bloco_completo
    dados['codigo'] = bloco_completo[:5]
    return dados