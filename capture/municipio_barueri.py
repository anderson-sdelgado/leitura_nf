import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_municipio_barueri(texto: str):
    linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]

    prestador = pegar_dados_prestador(linhas)
    tomador = pegar_dados_tomador(linhas)
    financeiro = pegar_valores(linhas)
    servico = pegar_dados_servico(linhas)

    # print("----------- NOTA BARUERI -----------")
    # for numero, linha in enumerate(linhas, start=1): 
    #     print(f"{linha}")
    # print("-------------------------")

    # Extração de blocos de dados

    nota = {}
    nota["DT_HR_INCL"] = None # Data e hora da inclusão da linha.
    nota["DT_HR_ALT"] = None # Data e hora da alteração da linha.
    nota["CDDOCUMENT"] = None # Código do documento no SE Suite. Idem V_NF_SERV.
    nota["NRO_CHAVE"] = None # Chave para registro da NFs-e. Gerada na integração.
    nota["CPF_CNPJ_EMIT"] = limpar_cnpj(tomador['cnpj']) # CNPJ/CPF da empresa (tomador) - somente números. Vide V_NF_SERV.TS_CNPJ_CPF. ok
    nota["COD_PART"] = limpar_cnpj(prestador['cnpj']) # CNPJ/CPF do fornecedor (prestador) - somente números. Vide V_NF_SERV.PS_CNPJ_CPF. ok
    nota["COD_MOD"] = "99" # Código do modelo de documento fiscal para registro. Fixo "99".
    nota["SERIE"] = "A" # Série do documento fiscal para registro. Fixo "A".
    nota["DTINSERT"] = None # Data da inclusão no SE Suite. Idem V_NF_SERV.
    nota["DTUPDATE"] = None # Data da alteração no SE Suite. Idem V_NF_SERV.
    nota["ID_DOC"] = pegar_autenticidade(linhas) # ID do documento na view. Idem V_NF_SERV. ok
    nota["PREFEIT"] = pegar_prefeitura(linhas) # Nome da prefeitura. Idem V_NF_SERV. ok
    nota["SECRET_PREFEIT"] = pegar_secretaria(linhas) # Secretaria da prefeitura. Idem V_NF_SERV. ok
    nota["NRO_NF"] = pegar_numero_nf(linhas) # Número da NF. Idem V_NF_SERV. ok
    nota["DT_EMISS"] = pegar_data_hora_emissao(linhas) # Data de emissão da NF. Idem V_NF_SERV. ok
    nota["PS_RAZ_SOC_NOME"] = prestador['razao_social'] # Nome do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_CNPJ_CPF"] = prestador['cnpj'] # CNPJ do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_INSC_MUNIC"] = prestador['inscricao_municipal'] # Inscrição municipal do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_INSC_EST"] = None # Inscrição estadual do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_MUNIC"] = prestador['municipio'] # Nome do município do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_UF"] = prestador['uf'] # Sigla da UF do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_ENDERECO"] = prestador['endereco'] # Endereço do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_BAIRRO"] = prestador['bairro'] # Bairro do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_CEP"] = prestador['cep'] # CEP do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_EMAIL"] = None # E-mail do prestador de serviço. Idem V_NF_SERV. ok
    nota["TS_RAZ_SOC_NOME"] = tomador['razao_social'] # Nome do tomador de serviço - empresa usuária. Idem V_NF_SERV. ok
    nota["TS_CNPJ_CPF"] = tomador['cnpj'] # CNPJ do tomador de serviço - empresa usuária. Idem V_NF_SERV. ok ok
    nota["DESC_SERV"] = pegar_discriminacao(linhas) # Descrição do serviço. Idem V_NF_SERV. ok
    nota["VL_BRUTO"] = extrair_valor(financeiro["bruto"]) # Valor bruto. Idem V_NF_SERV. 
    nota["VL_LIQ"] = extrair_valor(financeiro["liquido"]) # Valor líquido. Idem V_NF_SERV.
    nota["VL_PIS"] = extrair_valor(financeiro["pis"]) # Valor do PIS. Idem V_NF_SERV.
    nota["VL_COFINS"] = extrair_valor(financeiro["cofins"]) # Valor da Cofins. Idem V_NF_SERV.
    nota["VL_IR"] = extrair_valor(financeiro["ir"]) # Valor do IR. Idem V_NF_SERV.
    nota["VL_INSS"] = None # Valor do INSS. Idem V_NF_SERV.
    nota["VL_CSLL"] = extrair_valor(financeiro["csll"]) # Valor da CSLL. Idem V_NF_SERV.
    nota["VL_ISS"] = None # Valor do ISS. Idem V_NF_SERV.
    nota["COD_SERVICO"] = servico["codigo"] # Código do serviço. Idem V_NF_SERV.
    nota["COD_SERVICO_ORIGINAL"] = servico["descricao"] # Código do serviço - informação original. Idem V_NF_SERV.

    print("----------- NOTA BARUERI -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("--------------------------------------")

def pegar_autenticidade(linhas):
    texto_topo = " ".join(linhas[:15])
    padrao = r'[0-9A-Z]{4}\.[0-9A-Z]{4}\.[0-9A-Z]{4}\.[0-9A-Z]{7}-[A-Z0-9]'
    match = re.search(padrao, texto_topo)
    if match:
        return match.group(0)
    for linha in linhas:
        if "Autenticidade" in linha:
            parte_apos = linha.split("Autenticidade")[-1]
            match_flex = re.search(r'[0-9A-Z]{4}\.[0-9A-Z.]+', parte_apos)
            if match_flex:
                return match_flex.group(0).strip()
    return None

def pegar_prefeitura(linhas):
    for linha in linhas:
        match = re.search(r'(PREFEITURA\s+.*?)(?:\s{2,}|$)', linha)
        if match:
            return match.group(1).strip()
    return None

def pegar_secretaria(linhas):
    for linha in linhas:
        if "SECRETARIA" in linha.upper():
            return linha.strip()
    return None

def pegar_numero_nf(linhas):
    for linha in linhas:
        match = re.search(r'-[A-Z0-9]\s+(\d{7})', linha)
        if match:
            return match.group(1)
        if "Número da Nota" in linha:
            match_simples = re.search(r'(?<!-)(\b\d{7}\b)', linha)
            if match_simples:
                return match_simples.group(1)
    return None

def pegar_data_hora_emissao(linhas):
    texto_topo = " ".join(linhas[:10])
    match = re.search(r'(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2})', texto_topo)
    if match:
        return f"{match.group(1)} {match.group(2)}"
    for linha in linhas:
        match_data = re.search(r'(\d{2}/\d{2}/\d{4})', linha)
        if match_data:
            return match_data.group(1)
    return None

def pegar_dados_prestador(linhas):
    dados = {
        "razao_social": None, 
        "cnpj": None, 
        "inscricao_municipal": None, 
        "endereco": None, 
        "bairro": None, 
        "cep": None,
        "uf": "SP",
        "municipio": "BARUERI"
    }
    texto_bloco = " ".join(linhas)
    for i, linha in enumerate(linhas):
        if "Prestador de Serviços" in linha:
            dados["razao_social"] = linha.replace("Prestador de Serviços", "").strip()
            if i + 2 < len(linhas):
                logradouro = linhas[i+1].strip()
                complemento_bairro = linhas[i+2].strip()
                if "/" in complemento_bairro:
                    partes = complemento_bairro.split("/")
                    complemento = partes[0].strip()
                    dados["bairro"] = partes[-1].strip()
                    dados["endereco"] = f"{logradouro}, {complemento}"
                else:
                    dados["endereco"] = logradouro
                    dados["bairro"] = complemento_bairro
            m_im = re.search(r'Inscrição Municipal\s+([\d.-]+)', texto_bloco)
            if m_im:
                dados["inscricao_municipal"] = m_im.group(1).strip()
            m_cnpj = re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', texto_bloco)
            m_cep = re.search(r'CEP\s+(\d{5}-\d{3})', texto_bloco)
            if m_cnpj: dados["cnpj"] = m_cnpj.group(0)
            if m_cep: dados["cep"] = m_cep.group(1)
            break
    return dados

def pegar_dados_tomador(linhas):
    dados = {"razao_social": None, "cnpj": None}
    for i, linha in enumerate(linhas):
        if "Nome Tomador de Serviços" in linha:
            if i + 1 < len(linhas):
                parts = re.split(r'\s{2,}', linhas[i+1])
                dados["razao_social"] = parts[0]
                if len(parts) > 1:
                    cnpj = re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', parts[1])
                    if cnpj: dados["cnpj"] = cnpj.group(0)
            break
    return dados

def pegar_dados_servico(linhas):
    serv = {"codigo": None, "descricao": None}
    for linha in linhas:
        match = re.search(r'\d+\s+(.*?)\s+(\d{4})(\d{5})\s+[\d,.]+', linha)
        if match:
            texto_servico = match.group(1).strip()
            codigo_reduzido = match.group(2).strip()
            codigo_completo = codigo_reduzido + match.group(3).strip()
            serv["codigo"] = codigo_reduzido
            serv["descricao"] = f"{codigo_completo} - {texto_servico}"
            break
    return serv

def pegar_discriminacao(linhas):
    texto_total = "\n".join(linhas)
    match = re.search(r'DISCRIMINAÇÃO DOS SERVIÇOS.*?\n(.*?)(?=VALORES DE REPASSE|Observações|$)', texto_total, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).replace("\n", " ").strip()
    return None

def pegar_valores(linhas):
    vals = {
        "bruto": "0,00", "liquido": "0,00", 
        "ir": "0,00", "pis": "0,00", "cofins": "0,00", "csll": "0,00"
    }
    texto_completo = " ".join(linhas)
    m_bruto = re.search(r'VALOR TOTAL DA NOTA\s+([\d.,]+)', texto_completo)
    if m_bruto:
        vals["bruto"] = m_bruto.group(1)
    m_liq = re.search(r'R\$\s+([\d.,]+)\s+CC\s+/', texto_completo)
    if not m_liq:
        m_liq = re.search(r'Valor da Fatura.*?R\$\s*([\d.,]+)', texto_completo, re.DOTALL)
    if m_liq:
        vals["liquido"] = m_liq.group(1)
    m_impostos = re.search(r'(\d+,\d{2})\s+(\d+,\d{2})\s+(\d+,\d{2})\s+(\d+,\d{2})', texto_completo)
    if m_impostos:
        vals["ir"] = m_impostos.group(1)
        vals["pis"] = m_impostos.group(2)
        vals["cofins"] = m_impostos.group(3)
        vals["csll"] = m_impostos.group(4)
    return vals