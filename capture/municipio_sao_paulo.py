import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_municipio_sao_paulo(texto: str):
    linhas = texto.splitlines()

    # print("----------- NOTA SÃO PAULO -----------")
    # for numero, linha in enumerate(linhas, start=1): 
    #     print(f"{linha}")
    # print("-------------------------")

    linhas = texto.splitlines()
    
    # Extração de blocos de dados
    prestador = pegar_dados_prestador(linhas)
    tomador = pegar_dados_tomador(linhas)
    financeiro = pegar_valores(linhas)
    servico = pegar_codigo_servico(linhas)

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
    nota["ID_DOC"] = pegar_codigo_verificacao(linhas) # ID do documento na view. Idem V_NF_SERV. ok
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
    nota["DESC_SERV"] = pegar_discriminacao_servico(linhas) # Descrição do serviço. Idem V_NF_SERV. ok
    nota["VL_BRUTO"] = extrair_valor(financeiro["bruto"]) # Valor bruto. Idem V_NF_SERV. 
    nota["VL_LIQ"] = None # Valor líquido. Idem V_NF_SERV.
    nota["VL_PIS"] = extrair_valor(financeiro["pis"]) # Valor do PIS. Idem V_NF_SERV.
    nota["VL_COFINS"] = extrair_valor(financeiro["cofins"]) # Valor da Cofins. Idem V_NF_SERV.
    nota["VL_IR"] = extrair_valor(financeiro["irrf"]) # Valor do IR. Idem V_NF_SERV.
    nota["VL_INSS"] = extrair_valor(financeiro["inss"]) # Valor do INSS. Idem V_NF_SERV.
    nota["VL_CSLL"] = extrair_valor(financeiro["csll"]) # Valor da CSLL. Idem V_NF_SERV.
    nota["VL_ISS"] = extrair_valor(financeiro["iss"]) # Valor do ISS. Idem V_NF_SERV.
    nota["COD_SERVICO"] = servico["codigo"] # Código do serviço. Idem V_NF_SERV.
    nota["COD_SERVICO_ORIGINAL"] = servico["descricao"] # Código do serviço - informação original. Idem V_NF_SERV.

    print("----------- NOTA SÃO PAULO -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("--------------------------------------")

# --- FUNÇÕES ESPECÍFICAS SP ---

def pegar_prefeitura(linhas):
    for linha in linhas:
        if "PREFEITURA" in linha.upper():
            return linha.strip()
    return None

def pegar_secretaria(linhas):
    for linha in linhas:
        if "SECRETARIA" in linha.upper():
            partes = re.split(r'\s{2,}', linha.strip())
            if partes:
                return partes[0].strip()
    return None

def pegar_numero_nf(linhas):
    for i, linha in enumerate(linhas):
        if "Número da Nota" in linha:
            for j in range(1, 4):
                if i + j < len(linhas):
                    candidato = linhas[i + j].strip()
                    if candidato.isdigit() and len(candidato) > 1:
                        return candidato
    return None

def pegar_codigo_verificacao(linhas):
    for i, linha in enumerate(linhas):
        if "Código de Verificação" in linha:
            return linhas[i+1].strip()
    return None

def pegar_data_hora_emissao(linhas):
    for i, linha in enumerate(linhas):
        if "Data e Hora de Emissão" in linha:
            return linhas[i+1].strip()
    return None

def pegar_dados_prestador(linhas):
    dados = {
        "cnpj": None, 
        "inscricao_municipal": None, 
        "razao_social": None, 
        "endereco": None, 
        "bairro": None,
        "municipio": None, 
        "uf": None, 
        "cep": None
    }
    
    for i, linha in enumerate(linhas):
        if "PRESTADOR DE SERVIÇOS" in linha.upper():
            m_cnpj = re.search(r'CPF/CNPJ:\s*([\d./-]+)\s+Inscrição Municipal:\s*(.*)', linhas[i+1])
            if m_cnpj:
                dados["cnpj"] = m_cnpj.group(1).strip()
                dados["inscricao_municipal"] = m_cnpj.group(2).strip()
            if "Nome/Razão Social:" in linhas[i+2]:
                dados["razao_social"] = linhas[i+2].split("Social:")[1].strip()
            if "Endereço:" in linhas[i+3]:
                partes_end = linhas[i+3].split("Endereço:")[1].split(" - ")
                if len(partes_end) >= 3:
                    dados["endereco"] = partes_end[0].strip()
                    dados["bairro"] = partes_end[1].strip()
                    m_cep = re.search(r'CEP:\s*([\d-]+)', partes_end[-1])
                    if m_cep: dados["cep"] = m_cep.group(1)
            if "Município:" in linhas[i+4]:
                m_loc = re.search(r'Município:\s*(.*?)\s+UF:\s*([A-Z]{2})', linhas[i+4])
                if m_loc:
                    dados["municipio"] = m_loc.group(1).strip()
                    dados["uf"] = m_loc.group(2).strip()
            break
    return dados

def pegar_dados_tomador(linhas):
    dados = {"razao_social": None, "cnpj": None}
    for i, linha in enumerate(linhas):
        if "TOMADOR DE SERVIÇOS" in linha:
            dados["razao_social"] = linhas[i+1].split("Social:")[1].strip()
            m = re.search(r'CPF/CNPJ:\s*([\d./-]+)', linhas[i+2])
            if m: dados["cnpj"] = m.group(1).strip()
    return dados

def pegar_valores(linhas):
    v = {"bruto": "0,00", "inss": "0,00", "irrf": "0,00", "csll": "0,00", "cofins": "0,00", "pis": "0,00", "iss": "0,00"}
    for i, linha in enumerate(linhas):
        if "VALOR TOTAL DO SERVIÇO =" in linha:
            v["bruto"] = linha.split("=")[1].replace("R$", "").strip()
        if "INSS (R$)" in linha:
            valores = re.findall(r'[\d.]+,\d{2}', linhas[i+1])
            if len(valores) >= 5:
                v["inss"], v["irrf"], v["csll"], v["cofins"], v["pis"] = valores[:5]
        if "Valor do ISS (R$)" in linha:
            valores = re.findall(r'[\d.]+,\d{2}', linhas[i+1])
            if len(valores) >= 3:
                v["iss"] = valores[-2]
    return v

def pegar_codigo_servico(linhas):
    d = {"codigo": None, "descricao": None}
    for i, linha in enumerate(linhas):
        if "Código do Serviço" in linha:
            texto_completo = []
            for j in range(i + 1, len(linhas)):
                linha_atual = linhas[j].strip()
                if "VALOR TOTAL" in linha_atual.upper() or "BASE DE CÁLCULO" in linha_atual.upper():
                    break
                if linha_atual:
                    texto_completo.append(linha_atual)
            if texto_completo:
                string_total = " ".join(texto_completo).strip()
                d["descricao"] = string_total
                m = re.search(r'(\d{5})', string_total)
                if m:
                    d["codigo"] = m.group(1)
            break
    return d

def pegar_discriminacao_servico(linhas):
    desc = []; dentro = False
    for linha in linhas:
        if "DISCRIMINAÇÃO DE SERVIÇOS" in linha.upper(): dentro = True; continue
        if dentro:
            if "VALOR TOTAL DO SERVIÇO" in linha.upper(): break
            c = linha.strip()
            if c: desc.append(c)
    return " ".join(desc).strip()