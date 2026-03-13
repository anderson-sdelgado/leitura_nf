import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_ginfes(texto: str):
    linhas = texto.splitlines()
        
    # print("----------- NOTA GINFES -----------")
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
    nota["COD_PART"] = limpar_cnpj(prestador['cnpj']) # CNPJ/CPF do fornecedor (prestador) - somente números. Vide V_NF_SERV.PS_CNPJ_CPF. ok
    nota["COD_MOD"] = "99" # Código do modelo de documento fiscal para registro. Fixo "99".
    nota["SERIE"] = "A" # Série do documento fiscal para registro. Fixo "A".
    nota["DTINSERT"] = None # Data da inclusão no SE Suite. Idem V_NF_SERV.
    nota["DTUPDATE"] = None # Data da alteração no SE Suite. Idem V_NF_SERV.
    nota["ID_DOC"] = pegar_codigo_verificacao(linhas) # ID do documento na view. Idem V_NF_SERV. ok
    nota["PREFEIT"] = pegar_prefeitura(linhas) # Nome da prefeitura. Idem V_NF_SERV.
    nota["SECRET_PREFEIT"] = None # Secretaria da prefeitura. Idem V_NF_SERV. ok
    nota["NRO_NF"] = pegar_numero_nf(linhas) # Número da NF. Idem V_NF_SERV. ok
    nota["DT_EMISS"] = pegar_data_hora_emissao(linhas) # Data de emissão da NF. Idem V_NF_SERV. ok
    nota["PS_RAZ_SOC_NOME"] = prestador['razao_social'] # Nome do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_CNPJ_CPF"] = prestador['cnpj'] # CNPJ do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_INSC_MUNIC"] = prestador['inscricao_municipal'] # Inscrição municipal do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_INSC_EST"] = prestador['inscricao_estadual'] # Inscrição estadual do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_MUNIC"] = prestador['municipio'] # Nome do município do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_UF"] = prestador['uf'] # Sigla da UF do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_ENDERECO"] = prestador['endereco'] # Endereço do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_BAIRRO"] = prestador['bairro'] # Bairro do prestador de serviço. Idem V_NF_SERV. ok
    nota["PS_CEP"] = prestador['cep'] # CEP do prestador de serviço. Idem V_NF_SERV. ok
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

    print("----------- NOTA GINFES -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("--------------------------------------")

def pegar_prefeitura(linhas):
    for i, linha in enumerate(linhas):
        linha_up = linha.upper()
        if "PREFEITURA" in linha_up:
            return linha.strip()
        if "MUNICÍPIO DE PRESTAÇÃO DO SERVIÇO" in linha_up or "MUNICIPIO DE PRESTACAO DO SERVICO" in linha_up:
            if i + 1 < len(linhas):
                proxima = linhas[i+1].strip()
                match = re.search(r'([A-Za-zÀ-ÿ\s]+)[/-]', proxima)
                if match:
                    return f"PREFEITURA MUNICIPAL DE {match.group(1).strip().upper()}"
                return proxima.upper()
    return None

def pegar_numero_nf(linhas):
    for i, linha in enumerate(linhas):
        linha_up = linha.upper().strip()
        if "NÚMERO DA NOTA" in linha_up or "NUMERO DA NOTA" in linha_up:
            for offset in range(1, 3): 
                if i + offset < len(linhas):
                    candidato = linhas[i + offset].strip()
                    if candidato.isdigit():
                        return candidato
    return None

def pegar_codigo_verificacao(linhas):
    for i, linha in enumerate(linhas):
        linha_up = linha.upper()
        if "CÓDIGO DE VERIFICAÇÃO:" in linha_up or "CODIGO DE VERIFICACAO:" in linha_up:
            if i + 1 < len(linhas):
                partes = linhas[i+1].split()
                if partes:
                    codigo = partes[-1].strip()
                    if len(codigo) >= 6:
                        return codigo
    return None

def pegar_data_hora_emissao(linhas):
    for i, linha in enumerate(linhas):
        linha_up = linha.upper().strip()
        if "DATA E HORA DE EMISSÃO" in linha_up or "DATA E HORA DE EMISSAO" in linha_up:
            for offset in range(1, 3):
                if i + offset < len(linhas):
                    candidato = linhas[i + offset].strip()
                    match = re.search(r'(\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2})', candidato)
                    if match:
                        return match.group(1)
    return None

def pegar_dados_prestador(linhas):
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
    linhas_prestador = []
    dentro_do_bloco = False
    for linha in linhas:
        linha_up = linha.upper().strip()
        if "PRESTADOR DE SERVIÇOS" in linha_up:
            dentro_do_bloco = True
            continue
        if "TOMADOR DE SERVIÇOS" in linha_up:
            break
        if dentro_do_bloco:
            linhas_prestador.append(linha.strip())
    texto_completo = "\n".join(linhas_prestador)
    m_rs = re.search(r'Nome/Razão Social:\s*(.*)', texto_completo, re.IGNORECASE)
    if m_rs: dados["razao_social"] = m_rs.group(1).strip()
    m_cnpj = re.search(r'CPF/CNPJ:\s*([\d./-]+)', texto_completo)
    if m_cnpj: dados["cnpj"] = m_cnpj.group(1).strip()
    m_im = re.search(r'IM:\s*(\d+)', texto_completo)
    if m_im: dados["inscricao_municipal"] = m_im.group(1).strip()
    m_ie = re.search(r'IE:\s*([\d.]+)', texto_completo)
    if m_ie: 
        dados["inscricao_estadual"] = m_ie.group(1).strip()
    m_email = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', texto_completo)
    if m_email: dados["email"] = m_email.group(0).lower()
    for linha in linhas_prestador:
        if "CEP:" in linha.upper():
            m_cep = re.search(r'CEP:\s*([\d-]+)', linha)
            if m_cep: dados["cep"] = m_cep.group(1)
            partes = linha.split(" - ")
            if len(partes) >= 3:
                dados["bairro"] = partes[0].strip()
                dados["municipio"] = partes[1].strip()
                dados["uf"] = partes[2].split()[0].strip()
        elif "," in linha and "CPF/CNPJ" not in linha.upper() and "RAZÃO SOCIAL" not in linha.upper():
            dados["endereco"] = linha.strip()
    return dados

def pegar_dados_tomador(linhas):
    dados = {"cnpj": None, "razao_social": None}
    linhas_tomador = []
    dentro_do_bloco = False
    for linha in linhas:
        linha_up = linha.upper().strip()
        if "TOMADOR DE SERVIÇOS" in linha_up:
            linhas_tomador = []
            dentro_do_bloco = True
            continue
        if "DISCRIMINAÇÃO DOS SERVIÇOS" in linha_up or "DISCRIMINACAO DOS SERVICOS" in linha_up:
            break
        if dentro_do_bloco:
            linhas_tomador.append(linha.strip())
    texto_bloco = "\n".join(linhas_tomador)
    m_rs = re.search(r'Nome/Razão Social:\s*(.*)', texto_bloco, re.IGNORECASE)
    if m_rs:
        dados["razao_social"] = m_rs.group(1).strip()
    m_cnpj = re.search(r'CPF/CNPJ:\s*([\d./-]+)', texto_bloco)
    if m_cnpj:
        dados["cnpj"] = m_cnpj.group(1).strip()
    return dados

def pegar_discriminacao_servico(linhas):
    linhas_desc = []
    dentro_do_bloco = False
    parar_em = [
        "CÓDIGO SERVIÇO", "CODIGO SERVICO", 
        "TRIBUTOS FEDERAIS", "DETALHAMENTO DE VALORES",
        "VALOR TOTAL DOS SERVIÇOS"
    ]
    for linha in linhas:
        linha_limpa = linha.strip()
        linha_up = linha_limpa.upper()
        if "DISCRIMINAÇÃO" in linha_up and "SERVIÇOS" in linha_up:
            dentro_do_bloco = True
            continue
        if dentro_do_bloco:
            if any(termo in linha_up for termo in parar_em):
                break
            if not linha_limpa:
                continue
            if "---" in linha_limpa:
                continue
            if linha_up.startswith("SERVICOS DIVERSOS") and "R$:" in linha_up:
                partes = linha_limpa.split("R$:")
                if len(partes) > 1 and partes[1].strip().replace('.', '').replace(',', '').isdigit():
                    continue 
            linhas_desc.append(linha_limpa)
    return " ".join(linhas_desc).strip() if linhas_desc else None

def pegar_valores(linhas):
    financeiro = {
        "pis": "0,00", "cofins": "0,00", "csll": "0,00", 
        "ir": "0,00", "inss": "0,00", "iss": "0,00", 
        "bruto": "0,00", "liquido": "0,00"
    }
    for i, linha in enumerate(linhas):
        linha_up = linha.upper()
        if "VALOR DOS SERVIÇOS" in linha_up:
            m_bruto = re.search(r'VALOR DOS SERVIÇOS\s*([\d.]+,\d{2})', linha_up)
            if m_bruto:
                financeiro["bruto"] = m_bruto.group(1)
        if "PIS (R$)" in linha_up and "COFINS (R$)" in linha_up:
            if i + 1 < len(linhas):
                valores_federais = re.findall(r'([\d.]+,\d{2})', linhas[i+1])
                if len(valores_federais) >= 5:
                    financeiro["pis"] = valores_federais[0]
                    financeiro["cofins"] = valores_federais[1]
                    financeiro["ir"] = valores_federais[2]
                    financeiro["inss"] = valores_federais[3]
                    financeiro["csll"] = valores_federais[4]
        if "(=) VALOR ISS" in linha_up:
            m_iss = re.search(r'VALOR ISS\s*([\d.]+,\d{2})', linha_up)
            if m_iss:
                financeiro["iss"] = m_iss.group(1)
        if "VALOR LÍQUIDO" in linha_up or "VALOR LIQUIDO" in linha_up:
            m_liq = re.search(r'VALOR LÍQUIDO\s*([\d.]+,\d{2})', linha_up)
            if m_liq:
                financeiro["liquido"] = m_liq.group(1)
            else:
                m_liq_antes = re.search(r'([\d.]+,\d{2})\s*VALOR LÍQUIDO', linha_up)
                if m_liq_antes:
                    financeiro["liquido"] = m_liq_antes.group(1)
    return financeiro

def pegar_dados_servico(linhas):
    servico = {"codigo": None, "descricao": None}
    for i, linha in enumerate(linhas):
        linha_up = linha.upper().strip()
        if "CÓDIGO SERVIÇO:" in linha_up or "CODIGO SERVICO:" in linha_up:
            m_cod = re.search(r'(\d{2}\.\d{2})', linha)
            if not m_cod and i + 1 < len(linhas):
                m_cod = re.search(r'(\d{2}\.\d{2})', linhas[i+1])
            if m_cod:
                servico["codigo"] = m_cod.group(1)
            linhas_descritivo = []
            inicio_busca = i if "CÓDIGO SERVIÇO" in linha_up else i + 1
            for j in range(inicio_busca, inicio_busca + 5):
                if j >= len(linhas): break
                curr_linha = linhas[j].strip()
                curr_up = curr_linha.upper()
                if "TRIBUTOS FEDERAIS" in curr_up or "PIS (R$)" in curr_up:
                    break
                limpa = re.sub(r'C[ÓO]DIGO\s+SERVI[ÇC]O:', '', curr_linha, flags=re.IGNORECASE).strip()
                if servico["codigo"]:
                    limpa = limpa.replace(servico["codigo"], "").strip()
                limpa = re.sub(r'^[-\s–—]+', '', limpa)
                if limpa:
                    linhas_descritivo.append(limpa)
            texto_puro = " ".join(linhas_descritivo).strip()
            if servico["codigo"] and texto_puro:
                servico["descricao"] = f"{servico['codigo']} - {texto_puro}"
            else:
                servico["descricao"] = texto_puro
            break
    return servico