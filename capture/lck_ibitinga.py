import re
from lib.limpar_cnpj import formatar_cnpj, limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_lck(texto: str):
    linhas = texto.splitlines()

    # print("----------- NOTA LCK -----------")
    # for numero, linha in enumerate(linhas, start=1): 
    #     print(f"{linha}")
    # print("-------------------------")
     
    prestador = pegar_dados_prestador(linhas)
    tomador = pegar_dados_tomador(linhas)
    financeiro = pegar_valores(linhas)
    servico = pegar_dados_servico(linhas)

    nota = {}
    nota["DT_HR_INCL"] = None # Data e hora da inclusão da linha.
    nota["DT_HR_ALT"] = None # Data e hora da alteração da linha.
    nota["CDDOCUMENT"] = None # Código do documento no SE Suite. Idem V_NF_SERV.
    nota["NRO_CHAVE"] = None # Chave para registro da NFs-e. Gerada na integração.
    nota["CPF_CNPJ_EMIT"] = limpar_cnpj(tomador['cnpj']) # CNPJ/CPF da empresa (tomador) - somente números. Vide V_NF_SERV.TS_CNPJ_CPF. ok
    nota["COD_PART"] = prestador['cnpj'] # CNPJ/CPF do fornecedor (prestador) - somente números. Vide V_NF_SERV.PS_CNPJ_CPF. ok
    nota["COD_MOD"] = "99" # Código do modelo de documento fiscal para registro. Fixo "99".
    nota["SERIE"] = "A" # Série do documento fiscal para registro. Fixo "A".
    nota["DTINSERT"] = None # Data da inclusão no SE Suite. Idem V_NF_SERV.
    nota["DTUPDATE"] = None # Data da alteração no SE Suite. Idem V_NF_SERV.
    nota["ID_DOC"] = pegar_codigo_verificacao(linhas) # ID do documento na view. Idem V_NF_SERV. ok
    nota["PREFEIT"] = pegar_prefeitura(linhas) # Nome da prefeitura. Idem V_NF_SERV.
    nota["SECRET_PREFEIT"] = pegar_secretaria(linhas) # Secretaria da prefeitura. Idem V_NF_SERV. ok
    nota["NRO_NF"] = pegar_numero_nf(linhas) # Número da NF. Idem V_NF_SERV. ok
    nota["DT_EMISS"] = pegar_data_emissao(linhas) # Data de emissão da NF. Idem V_NF_SERV. ok
    nota["PS_RAZ_SOC_NOME"] = prestador['razao_social'] # Nome do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_CNPJ_CPF"] = formatar_cnpj(prestador['cnpj']) # CNPJ do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_INSC_MUNIC"] = prestador['inscricao_municipal'] # Inscrição municipal do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_INSC_EST"] = None # Inscrição estadual do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_MUNIC"] = prestador['municipio'] # Nome do município do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_UF"] = None # Sigla da UF do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_ENDERECO"] = prestador['endereco'] # Endereço do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_BAIRRO"] = prestador['bairro'] # Bairro do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_CEP"] = None # CEP do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_EMAIL"] = prestador['email'] # E-mail do prestador de serviço. Idem V_NF_SERV. ok
    nota["TS_RAZ_SOC_NOME"] = tomador['razao_social'] # Nome do tomador de serviço - empresa usuária. Idem V_NF_SERV. ok
    nota["TS_CNPJ_CPF"] = tomador['cnpj'] # CNPJ do tomador de serviço - empresa usuária. Idem V_NF_SERV. ok ok
    nota["DESC_SERV"] = pegar_discriminacao_servico(linhas) # Descrição do serviço. Idem V_NF_SERV. ok
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

    print("----------- NOTA LCK -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("--------------------------------------")

def pegar_codigo_verificacao(linhas):
    for i, linha in enumerate(linhas):
        if "CÓDIGO DE VERIFICAÇÃO" in linha:
            if i + 1 < len(linhas):
                proxima_linha = linhas[i+1].strip()
                match = re.search(r'(\d{10,})', proxima_linha)
                if match:
                    return match.group(1)
    return None

def pegar_prefeitura(linhas):
    for linha in linhas:
        match = re.search(r'(Prefeitura\s+.*?)(?:\s{2,}|$)', linha, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

def pegar_secretaria(linhas):
    for linha in linhas:
        match = re.search(r'(Secretaria\s+.*?)(?:\s{2,}|$)', linha, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

def pegar_numero_nf(linhas):
    for i, linha in enumerate(linhas):
        if "NÚMERO NOTA" in linha:
            return linhas[i+1].strip()
    return None

def pegar_data_emissao(linhas):
    for i, linha in enumerate(linhas):
        if "DATA E HORA DA EMISSÃO" in linha:
            match = re.search(r'(\d{2}/\d{2}/\d{4})', linhas[i+1])
            return match.group(1) if match else None
    return None

def pegar_dados_prestador(linhas):
    dados = {"razao_social": None, "cnpj": None, "inscricao_municipal": None, "municipio": None, "endereco": None, "bairro": None, "email": None}
    texto = "\n".join(linhas)
    try:
        bloco = texto.split("PRESTADOR DO(S) SERVIÇO(S)")[1].split("TOMADOR DO(S) SERVIÇO(S)")[0]
        linhas_bloco = [l.strip() for l in bloco.splitlines() if l.strip()]
        for i, l in enumerate(linhas_bloco):
            if "NOME / RAZÃO SOCIAL" in l: dados["razao_social"] = linhas_bloco[i+1]
            if "RUA" in l or "AVENIDA" in l: 
                partes = l.split(",")
                dados["endereco"] = partes[0].strip()
                if len(partes) > 1: dados["bairro"] = partes[-1].strip()
        match_cnpj = re.search(r'CNPJ\s+INSCRIÇÃO MUNICIPAL\s+E-MAIL\s+(\d+)\s+(\d+)\s+([\w\.-]+@[\w\.-]+)', bloco)
        if match_cnpj:
            dados["cnpj"] = match_cnpj.group(1)
            dados["inscricao_municipal"] = match_cnpj.group(2)
            dados["email"] = match_cnpj.group(3)
    except: pass
    return dados

def pegar_dados_tomador(linhas):
    dados = {"razao_social": None, "cnpj": None}
    texto = "\n".join(linhas)
    try:
        bloco = texto.split("TOMADOR DO(S) SERVIÇO(S)")[1].split("DISCRIMINAÇÃO DO(S) SERVIÇO(S)")[0]
        linhas_bloco = [l.strip() for l in bloco.splitlines() if l.strip()]
        if "NOME / RAZÃO SOCIAL" in linhas_bloco[0]:
            dados["razao_social"] = linhas_bloco[1]
        match_cnpj = re.search(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', bloco)
        if match_cnpj: dados["cnpj"] = match_cnpj.group(1)
    except: pass
    return dados

def pegar_discriminacao_servico(linhas):
    for i, linha in enumerate(linhas):
        if "Quant Descrição" in linha and "Valor do Serviço" in linha:
            if i + 1 < len(linhas):
                dados_linha = linhas[i+1].strip()
                match = re.search(r'^(\d+)\s+(.*?)\s+([\d.,]+)$', dados_linha)
                if match:
                    quant = match.group(1).strip()
                    desc = match.group(2).strip()
                    valor = match.group(3).strip()
                    return f"Quant: {quant}, Descrição: {desc}, Valor do Serviço: {valor};"
    return None

def pegar_valores(linhas):
    vals = {"bruto": "0,00", "liquido": "0,00", "ir": "0,00", "pis": "0,00", "cofins": "0,00", "csll": "0,00", "inss": "0,00", "iss": "0,00"}
    texto_completo = " ".join(linhas)
    m_bruto = re.search(r'VALOR DO\(S\) SERVIÇO\(S\)\s+VALOR DEDUÇÃO.*?([\d.,]+)', texto_completo)
    if not m_bruto:
         m_bruto = re.search(r'VALOR DO\(S\) SERVIÇO\(S\)\s+([\d.,]+)', texto_completo)
    if m_bruto: vals["bruto"] = m_bruto.group(1)
    for i, linha in enumerate(linhas):
        if "TOTAL DO(S) SERVIÇO(S)" in linha and "TOTAL LÍQUIDO" in linha:
            if i + 1 < len(linhas):
                valores_totais = re.findall(r'[\d.,]+', linhas[i+1])
                if len(valores_totais) >= 2:
                    vals["liquido"] = valores_totais[1]
    m_iss = re.search(r'VALOR DO ISS\s+VALOR DO ISS RETIDO.*?[\d.,]+\s+([\d.,]+)', texto_completo)
    if m_iss:
        vals["iss"] = m_iss.group(1)
    m_fed = re.search(r'IMPOSTO DE RENDA\s+([\d.,]+)\s+PIS\s+([\d.,]+)\s+COFINS\s+([\d.,]+)\s+CSLL\s+([\d.,]+)\s+INSS\s+([\d.,]+)', texto_completo)
    if m_fed:
        vals["ir"], vals["pis"], vals["cofins"], vals["csll"], vals["inss"] = m_fed.groups()
    return vals

def pegar_dados_servico(linhas):
    dados = {"codigo": None, "descricao": None}
    for i, linha in enumerate(linhas):
        if "CÓDIGO DE CLASSIFICAÇÃO DO SERVIÇO" in linha:
            if i + 1 < len(linhas):
                conteudo = linhas[i+1].strip()
                match = re.search(r'^(\d{4})(.*)', conteudo)
                if match:
                    dados["codigo"] = match.group(1).strip()
                    dados["descricao"] = (match.group(1) + match.group(2)).strip()
                else:
                    dados["codigo"] = conteudo.split()[0] if conteudo else None
                    dados["descricao"] = conteudo
    return dados
