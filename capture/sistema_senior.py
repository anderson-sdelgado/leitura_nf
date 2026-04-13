import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_sistema_senior(texto: str):

    # print("--------- NOTA SENIOR ---------")
    # print(f"{texto}")
    # print("-------------------------------")

    cabec = pegar_dados_cabecalho(texto)
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
    nota["ID_DOC"] = cabec['codigo_verificacao'] # ID do documento na view. Idem V_NF_SERV.
    nota["PREFEIT"] = pegar_prefeitura(texto) # Nome da prefeitura. Idem V_NF_SERV.
    nota["SECRET_PREFEIT"] = None # Secretaria da prefeitura. Idem V_NF_SERV.
    nota["NRO_NF"] = cabec['numero_nf'] # Número da NF. Idem V_NF_SERV.
    nota["DT_EMISS"] = cabec['data_hora_emissao'] # Data de emissão da NF. Idem V_NF_SERV.
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

def pegar_dados_cabecalho(texto):
    dados = {
        "data_hora_emissao": None, 
        "codigo_verificacao": None, 
        "numero_nf": None,
    }

    padrao = (
        r'N[UÚÙÛ]MERO\s*NFS-e'
        r'\s*\d+\s*(\d{2}/\d{2}/\d{4})\s(\d{2}:\d{2}:\d{2})\s*(.*?)\s*(\d+)\s*'
        r'\s*SIAFI\s*'
    )
    match = re.search(padrao, texto, re.S | re.I)
    if match: 
        data = match.group(1).strip()
        hora = match.group(2).strip()
        dados['data_hora_emissao'] = f'{data} {hora}'
        dados['codigo_verificacao'] = match.group(3).strip()
        dados['numero_nf'] = match.group(4).strip()

    return dados

def pegar_prefeitura(texto):
    padrao = r'(PREFEITURA.*?)\s{3}'
    match = re.search(padrao, texto, re.I | re.S)
    if match: return match.group(1).strip()
    padrao = r'(MUNIC[IÍ]PIO.*?)\s{3}'
    match = re.search(padrao, texto, re.I | re.S)
    if match: return match.group(1).strip()
    return None

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
        r'PRESTADOR\s*DO\s*SERVI[CÇ]O'
        r'\s*(.*?)\s*'
        r'TOMADOR\s*DO\s*SERVI[CÇ]O'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()

    padrao = (
        r'NOME'
        r'\s*(.*?)\s*'
        r'ENDERE[CÇ]O'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['razao_social'] = match.group(1).strip()

    padrao = (
        r'ENDERE[CÇ]O'
        r'\s*(.*?)\s*'
        r'COMPLEMENTO'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: endereco = match.group(1).strip()

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

    padrao = (
        r'CEP'
        r'\s*(.*?)\s{3}([A-Z]{2})\s{3}(.*?)\s*'
        r'\s*CNPJ\s*'
    )
    match = re.search(padrao, bloco_completo, re.S | re.I)
    if match: 
        dados['municipio'] = match.group(1).strip()
        dados['uf'] = match.group(2).strip()
        dados['cep'] = match.group(3).strip()

    padrao = (
        r'E-MAIL'
        r'\s*(.*?)\s{3}(\d+)\s{3}(.*?)\s*'
    )
    match = re.search(padrao, bloco_completo, re.S | re.I)
    if match: 
        dados['cnpj'] = match.group(1).strip()
        dados['inscricao_municipal'] = match.group(2).strip()

    padrao = r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}'
    match = re.search(padrao, bloco_completo)
    if match:
        dados["email"] = match.group().lower()
    
    return dados

def pegar_dados_tomador(texto):
    dados = {"razao_social": None, "cnpj": None}
    
    padrao = (
        r'TOMADOR\s*DO\s*SERVI[CÇ]O'
        r'\s*(.*?)\s*'
        r'DESCRI[CÇ][AÁÀÃÂ]O\s*DO\s*SERVI[CÇ]O'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()
    dados['cnpj'] = bloco_completo

    padrao = (
        r'NOME'
        r'\s*(.*?)\s*'
        r'ENDERE[CÇ]O'
    )
    match = re.search(padrao, bloco_completo, re.I | re.S)
    if match: dados['razao_social'] = match.group(1).strip()

    padrao = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
    match = re.search(padrao, bloco_completo)
    if match: dados["cnpj"] = match.group()

    return dados

def pegar_discriminacao_servico(texto):
    padrao = (
        r'DESCRI[CÇ][AÃÀÁÂ]O\s*DO\s*SERVI[CÇ]O'
        r'\s*(.*?)\s*'
        r'SERVI[CÇ]O\s*\(LC\s*116\/2003\)'
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
        r'VALOR\s*TOTAL\s*DOS\s*SERVI[CÇ]OS'
        r'\s*(.*?)\s*'
        r'INFORMA[CÇ][OÓÒÔÕ]ES\s*ADICIONAIS'
    )
    match = re.search(padrao, texto, re.S | re.I)
    if not match: return dados
    
    bloco_completo = match.group(1)
    
    match = re.search(r"R\s*\$\s*(\d[\d\.]*,\d{2})\s*VALORES\s*TOTAIS", bloco_completo, re.S | re.I)
    if match: dados['bruto'] = match.group(1)

    padrao = (
        r'INSS'
        r'\s*(.*?)\s*'
        r'IMPOSTOS\s*MUNICIPAIS'
    )
    match = re.search(padrao, bloco_completo, re.S | re.I)
    if match: 
        impostos_federais = match.group(1)
        valores = re.findall(r"R\s*\$\s*(\d[\d\.]*,\d{2})", impostos_federais)
        if valores:
            dados['pis'] = valores[0]
            dados['cofins'] = valores[1]
            dados['csll'] = valores[2]
            dados['ir'] = valores[3]
            dados['inss'] = valores[4]

    padrao = (
        r'IMPOSTOS\s*MUNICIPAIS'
        r'\s*(.*?)\s*'
        r'VALOR\s*L[IÍÌÎ]QUIDO\s*DA\s*NFS-e:'
    )
    match = re.search(padrao, bloco_completo, re.S | re.I)
    if match: 
        impostos_federais = match.group(1)
        valores = re.findall(r"R\s*\$\s*(\d[\d\.]*,\d{2})", impostos_federais)
        if valores:
            dados['iss'] = valores[-1]
    
    match = re.search(r"VALOR\s*L[IÍÌÎ]QUIDO\s*DA\s*NFS-e:\s*R\s*\$\s*(\d[\d\.]*,\d{2})\s*", bloco_completo, re.S | re.I)
    if match: dados['liquido'] = match.group(1)

    return dados

def pegar_dados_servico(texto):
    dados = {"codigo": None, "descricao": None}
    padrao = (
        r'SERVI[CÇ]O\s*\(LC\s*116\/2003\)'
        r'\s*(.*?)\s*'
        r'VALOR\s*TOTAL\s*DOS\s*SERVI[CÇ]OS'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return dados

    bloco_completo = match.group(1).strip()

    dados['descricao'] = bloco_completo
    dados['codigo'] = bloco_completo[0:5]
    return dados