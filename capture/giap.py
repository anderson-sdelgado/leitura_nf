import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_giap(texto: str):
    linhas = texto.splitlines()

    # print("----------- NOTA GIAP -----------")
    # for numero, linha in enumerate(linhas, start=1): 
    #     print(f"{linha}")
    # print("-------------------------")

    prestador = pegar_dados_prestador(linhas)
    tomador = pegar_dados_tomador(linhas)
    tributos = pegar_valores_giap(linhas)
    servico = pegar_codigo_servico(linhas)
    
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
    # nota["ID_DOC"] = pegar_codigo_verificacao(linhas) # ID do documento na view. Idem V_NF_SERV.
    nota["PREFEIT"] = pegar_prefeitura(linhas) # Nome da prefeitura. Idem V_NF_SERV.
    nota["SECRET_PREFEIT"] = pegar_secretaria(linhas) # Secretaria da prefeitura. Idem V_NF_SERV.
    nota["NRO_NF"] = pegar_numero_nf(linhas) # Número da NF. Idem V_NF_SERV.
    nota["DT_EMISS"] = pegar_data_hora_emissao(linhas) # Data de emissão da NF. Idem V_NF_SERV.
    nota["PS_RAZ_SOC_NOME"] = prestador['razao_social'] # Nome do prestador de serviço. Idem V_NF_SERV.
    nota["PS_CNPJ_CPF"] = prestador['cnpj'] # CNPJ do prestador de serviço. Idem V_NF_SERV.
    nota["PS_INSC_MUNIC"] = prestador['inscricao_municipal'] # Inscrição municipal do prestador de serviço. Idem V_NF_SERV.
    nota["PS_INSC_EST"] = prestador['inscricao_estadual'] # Inscrição estadual do prestador de serviço. Idem V_NF_SERV.
    nota["PS_MUNIC"] = prestador['municipio'] # Nome do município do prestador de serviço. Idem V_NF_SERV.
    nota["PS_UF"] = prestador['uf'] # Sigla da UF do prestador de serviço. Idem V_NF_SERV.
    nota["PS_ENDERECO"] = prestador['endereco_completo'] # Endereço do prestador de serviço. Idem V_NF_SERV.
    nota["PS_BAIRRO"] = prestador['bairro'] # Bairro do prestador de serviço. Idem V_NF_SERV.
    nota["PS_CEP"] = prestador['cep'] # CEP do prestador de serviço. Idem V_NF_SERV.
    nota["PS_EMAIL"] = prestador['email'] # E-mail do prestador de serviço. Idem V_NF_SERV.
    nota["TS_RAZ_SOC_NOME"] = tomador['razao_social'] # Nome do tomador de serviço - empresa usuária. Idem V_NF_SERV.
    nota["TS_CNPJ_CPF"] = tomador['cnpj'] # CNPJ do tomador de serviço - empresa usuária. Idem V_NF_SERV.
    nota["DESC_SERV"] = pegar_discriminacao_servico(linhas) # Descrição do serviço. Idem V_NF_SERV.
    nota["VL_BRUTO"] = extrair_valor(tributos["bruto"]) # Valor bruto. Idem V_NF_SERV.
    nota["VL_LIQ"] = extrair_valor(tributos["liquido"]) # Valor líquido. Idem V_NF_SERV.
    nota["VL_PIS"] = extrair_valor(tributos["pis"]) # Valor do PIS. Idem V_NF_SERV.
    nota["VL_COFINS"] = extrair_valor(tributos["cofins"]) # Valor da Cofins. Idem V_NF_SERV.
    nota["VL_IR"] = extrair_valor(tributos["ir"]) # Valor do IR. Idem V_NF_SERV.
    nota["VL_INSS"] = extrair_valor(tributos["inss"]) # Valor do INSS. Idem V_NF_SERV.
    nota["VL_CSLL"] = extrair_valor(tributos["csll"]) # Valor da CSLL. Idem V_NF_SERV.
    nota["VL_ISS"] = extrair_valor(tributos["iss"]) # Valor do ISS. Idem V_NF_SERV.
    nota["COD_SERVICO"] = servico["codigo"] # Código do serviço. Idem V_NF_SERV.
    nota["COD_SERVICO_ORIGINAL"] = servico["descricao_completa"] # Código do serviço - informação original. Idem V_NF_SERV.

    print("----------- NOTA GISS -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("-----------------------------------")

def pegar_prefeitura(linhas):
    for linha in linhas:
        if "PREFEITURA" in linha.upper():
            return linha.strip()
    return None

def pegar_secretaria(linhas):
    for linha in linhas:
        if "SECRETARIA" in linha.upper():
            return linha.strip().rstrip(" -").strip()
    return None

def pegar_numero_nf(linhas):
    for i, linha in enumerate(linhas):
        if "Nº Nota" in linha:
            if i + 1 < len(linhas):
                proxima_linha = linhas[i+1].strip()
                if proxima_linha:
                    return proxima_linha.split()[0]
    return None

def converter_mes(data_str):
    meses = {
        "JAN": "01", "FEV": "02", "MAR": "03", "ABR": "04",
        "MAI": "05", "JUN": "06", "JUL": "07", "AGO": "08",
        "SET": "09", "OUT": "10", "NOV": "11", "DEZ": "12",
        "FEB": "02", "APR": "04", "MAY": "05", "AUG": "08", "SEP": "09", "OCT": "10"
    }
    for mes_texto, mes_num in meses.items():
        if mes_texto in data_str.upper():
            return data_str.upper().replace(mes_texto, mes_num)
    return data_str

def pegar_data_hora_emissao(linhas):
    for i, linha in enumerate(linhas):
        if "Data de Emissão" in linha:
            if i + 1 < len(linhas):
                linha_alvo = linhas[i+1].strip()
                match = re.search(r'(\d{2}/[A-Z]{3}/\d{4} - \d{2}:\d{2}:\d{2})', linha_alvo)
                if match:
                    data_convertida = converter_mes(match.group(1))
                    return data_convertida.replace(" - ", " ").strip()
    return None

def pegar_dados_prestador(linhas):
    dentro_secao = False
    dados = {"razao_social": None, "cnpj": None, "inscricao_municipal": None, "inscricao_estadual": None,
             "municipio": None, "uf": None, "endereco_completo": None, "bairro": None, "cep": None, "email": None}
    rua_bruta = ""
    for i, linha in enumerate(linhas):
        if "PRESTADOR DE SERVIÇOS" in linha.upper(): dentro_secao = True; continue
        if "TOMADOR DE SERVIÇOS" in linha.upper(): break
        if dentro_secao:
            if "Razão Social/Nome:" in linha: dados["razao_social"] = linha.split("Razão Social/Nome:")[1].strip()
            if "CNPJ/CPF:" in linha:
                m_cnpj = re.search(r'CNPJ/CPF:\s*([\d./-]+)', linha)
                if m_cnpj: dados["cnpj"] = m_cnpj.group(1).strip()
                m_im = re.search(r'Insc. Municipal:\s*(.*?)(?=Insc. Estadual:|$)', linha)
                if m_im: dados["inscricao_municipal"] = m_im.group(1).strip() or None
                m_ie = re.search(r'Insc. Estadual:\s*(.*)', linha)
                if m_ie: dados["inscricao_estadual"] = m_ie.group(1).strip() or None
            if "Endereço:" in linha: rua_bruta = linha.split("Endereço:")[1].strip()
            if "Bairro:" in linha:
                m_ba = re.search(r'Bairro:\s*(.*?)(?=\s+CEP:|$)', linha)
                if m_ba: dados["bairro"] = m_ba.group(1).strip()
                m_cep = re.search(r'CEP:\s*([\d.-]+)', linha)
                if m_cep: dados["cep"] = m_cep.group(1).strip()
            if "Município:" in linha:
                m_mu = re.search(r'Município:\s*(.*?)(?=\s+UF:|$)', linha)
                if m_mu: dados["municipio"] = m_mu.group(1).strip()
                m_uf = re.search(r'UF:\s*([A-Z]{2})', linha)
                if m_uf: dados["uf"] = m_uf.group(1).strip()
            if "E-MAIL:" in linha.upper():
                m_em = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', linha)
                if m_em: dados["email"] = m_em.group(1).strip()

    if rua_bruta and dados["bairro"]:
        rua_limpa = rua_bruta.replace(dados["bairro"], "").strip()
        dados["endereco_completo"] = re.sub(r'[, \s-]+$', '', rua_limpa)
    return dados

def pegar_dados_tomador(linhas):
    dentro = False
    dados = {"razao_social": None, "cnpj": None}
    for linha in linhas:
        if "TOMADOR DE SERVIÇOS" in linha.upper(): dentro = True; continue
        if "DISCRIMINAÇÃO DOS SERVIÇOS" in linha.upper(): break
        if dentro:
            if "Razão Social/Nome:" in linha: dados["razao_social"] = linha.split("Razão Social/Nome:")[1].strip()
            if "CNPJ/CPF:" in linha:
                m = re.search(r'CNPJ/CPF:\s*([\d./-]+)', linha)
                if m: dados["cnpj"] = m.group(1).strip()
    return dados

def pegar_discriminacao_servico(linhas):
    desc = []; dentro = False
    for linha in linhas:
        if "DISCRIMINAÇÃO DOS SERVIÇOS" in linha.upper(): dentro = True; continue
        if dentro:
            if any(t in linha.upper() for t in ["RETENÇÕES DE IMPOSTOS", "VALOR TOTAL DA NOTA", "INFORMAÇÕES COMPLEMENTARES"]): break
            c = linha.strip()
            if c and not c.startswith(("-", "=")): desc.append(c)
    return " ".join(desc).strip()

def pegar_valores_giap(linhas):
    v = {"bruto": "0,00", "liquido": "0,00", "inss": "0,00", "ir": "0,00", "csll": "0,00", "pis": "0,00", "cofins": "0,00", "iss": "0,00"}
    for i, linha in enumerate(linhas):
        l_up = linha.upper()
        if "VALOR DO INSS RETIDO" in l_up and i + 1 < len(linhas):
            nums = re.findall(r'[\d.]+,\d{2}', linhas[i+1])
            if len(nums) >= 5:
                v["inss"], v["ir"], v["csll"], v["pis"], v["cofins"] = nums[:5]
        if "BASE DE CÁLCULO DO ISS" in l_up and i + 1 < len(linhas):
            nums = re.findall(r'[\d.]+,\d{2}', linhas[i+1])
            if len(nums) >= 5:
                v["bruto"], v["iss"], v["liquido"] = nums[2], nums[3], nums[4]
            elif len(nums) >= 3:
                v["bruto"], v["iss"], v["liquido"] = nums[0], nums[-2], nums[-1]
        if "VALOR TOTAL DA NOTA =" in l_up:
            m = re.search(r'R\$\s*([\d.]+,\d{2})', linha)
            if m:
                if v["bruto"] == "0,00": v["bruto"] = m.group(1)
                if v["liquido"] == "0,00": v["liquido"] = m.group(1)
    return v

def pegar_codigo_servico(linhas):
    d = {"codigo": None, "descricao_completa": None}
    for linha in linhas:
        if any(t in linha.upper() for t in ["CÓDIGO DO SERVIÇO:", "ATIV. SERVIÇO:"]):
            m = re.search(r'(\d{1,2}\.\d{2})', linha)
            if m: d["codigo"] = m.group(1).strip()
            if "Ativ. Serviço:" in linha: d["descricao_completa"] = linha.split("Ativ. Serviço:")[1].strip()
            elif "Código do Serviço:" in linha: d["descricao_completa"] = linha.split("Código do Serviço:")[1].strip()
            break
    return d