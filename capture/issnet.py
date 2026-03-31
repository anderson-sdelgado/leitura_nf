
import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_issnet(texto: str):

    # print("----------- NOTA ISSNET -----------")
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
    padrao = r'\s*(.*)\s\s(\d+)\s*Dados\s*do\s*Prestador\s*de\s*Servi[cç]o'
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    return match.group(2).strip()

def pegar_data_hora_emissao(texto):
    padrao = r'Data\s*de\s*Gera[cç][aâãáà]o\s*da\s*NFS-e\s*(\d{2}/\d{2}/\d{4}).*?(\d{2}:\d{2}:\d{2})'
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
        r'Identifica[cç][aâãáà]o\s*'
    )
    match = re.search(padrao, texto, re.IGNORECASE | re.S)
    if not match: return dados
    bloco_completo = match.group(1).strip()

    padrao = (
        r'\s*\d{2}/\d{2}/\d{4}.*?\d{2}:\d{2}:\d{2}'
        r'\s*(.*?)\s*'
        r'Data\s*de\s*Compet[eêéè]ncia'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['razao_social'] = match.group(1).strip()

    padrao = (
        r'CPF/CNPJ'
        r'\s*(.*?)\s*'
        r'Respons[aâãáà]vel\s*pela\s*Reten[cç][aâãáà]o'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['cnpj'] = match.group(1).strip()

    padrao = (
        r'Inscri[cç][aâãáà]o\s*Municipal'
        r'\s*(.*?)\s*'
        r'-'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['inscricao_municipal'] = match.group(1).strip()

    match = re.search(r'\d{5}-\d{3}', bloco_completo)
    if match: dados["cep"] = match.group()

    padrao = r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}'
    match = re.search(padrao, bloco_completo)
    if match: dados["email"] = match.group().lower()

    padrao = (
        r'Data\s*de\s*Compet[eêéè]ncia'
        r'\s*(.*?)\s*'
        r'-'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        endereco = match.group(1).strip()
        padrao = r'\d{2}/\d{2}/\d{4}'
        end = re.sub(padrao, '', endereco)
        end = " ".join(end.split())
        dados['endereco'] = end
        
    padrao = (
        r'Data\s*de\s*Compet[eêéè]ncia'
        r'\s*.*?\s*'
        r'-'
        r'\s*(.*?)\s*'
        r'\s*CEP\s*'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        sujeira = [
            r'C[oóõôò]d.\s*de\s*Autenticidade',
            r'\d{2}/\d{2}/\d{4}',              # Datas, se houver
        ]
        texto_limpo = match.group(1).strip()
        for termo in sujeira:
            texto_limpo = re.sub(termo, '', texto_limpo, flags=re.I | re.S)
        dados['bairro'] =  re.sub(r'\s+', '', texto_limpo)

            
    padrao = r'-\s*([^-\/]+)\s*\/([A-Z]{2})'
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: 
        dados['municipio'] = match.group(1).strip()
        dados['uf'] = match.group(2).strip()

    return dados

def pegar_dados_tomador(texto):
    dados = {"razao_social": None, "cnpj": None}

    padrao = (
        r'Tomador\s*de\s*Servi[cç]o'
        r'\s*(.*?)\s*'
        r'Dados\s*do\s*Intermedi[aâãáà]rio'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados
    bloco_completo = match.group(1).strip()

    padrao = (
        r'Raz[aâãáà]o\s*Social\s*:?'
        r'\s*(.*?)$'
    )
    match = re.search(padrao, bloco_completo, re.I | re.M)
    if  match: dados['razao_social'] = match.group(1).strip()

    padrao = (
        r'CNPJ/CPF\s*:'
        r'\s*(.*?)\s*'
        r'IM\s*'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if  match: dados['cnpj'] = match.group(1).strip()

    return dados

def pegar_discriminacao_servico(texto):
    padrao = (
        r'Descri[cç][aâãáà]o\s*dos\s*Serviços'
        r'\s*(.*?)\s*'
        r'Detalhamento\s*dos\s*Tributos'
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
        r'\s*Total\s*dos\s*Servi[cç]os\s*'
        r'\s*(.*?)\s*'
        r'Constru[cç][aâãáà]o\s*Civil\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados
    bloco_completo = match.group(1).strip()
    padrao = r"R\$\s*[\d\.,]+|-"
    valores = re.findall(padrao, bloco_completo)
    dados['bruto'] = valores[0].replace("R$", "").strip()
    dados['liquido'] = valores[-1].replace("R$", "").strip()
    dados['pis'] = valores[6].replace("R$", "").strip()
    dados['cofins'] = valores[7].replace("R$", "").strip()
    dados['ir'] = valores[9].replace("R$", "").strip()
    dados['inss'] = valores[8].replace("R$", "").strip()
    dados['csll'] = valores[10].replace("R$", "").strip()
    dados['iss'] = valores[-2].replace("R$", "").strip()
    return dados

def pegar_dados_servico(texto):
    dados = {
        "codigo": None,
        "descricao": None,
    }
    padrao = (
        r'C[oóòõô]d.\s*CNAE\s*'
        r'\s*(.*?)\s*'
        r'\s*Total\s*dos\s*Servi[cç]os\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados
    bloco_completo = match.group(1).strip()
    padrao = r"(.*?)\s[\d\.,]+"
    match = re.search(padrao, bloco_completo)
    if not match: return dados
    descricao = match.group(1).strip()
    dados['descricao'] = descricao

    padrao = r"(.*?)\s*-"
    match = re.search(padrao, descricao)
    if not match: return dados

    codigo = match.group(1).strip()
    codigo = codigo.zfill(6)

    codigo = f"{codigo[:2]}.{codigo[2:4]}"
    dados['codigo'] = codigo
    
    return dados