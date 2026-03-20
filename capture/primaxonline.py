import re
from lib.limpar_cnpj import formatar_cnpj, limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_primax(texto: str):
    linhas = texto.splitlines()

    # print("----------- NOTA PRIMAX -----------")
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
    texto_completo = " ".join(linhas)
    match = re.search(r'Portal Nacional:\s*(\d{40,})', texto_completo)
    if match:
        return match.group(1)
    match_seguranca = re.search(r'Chave de Segurança\s+([A-Z0-9-]+)', texto_completo)
    if match_seguranca:
        return match_seguranca.group(1)
    return None

def pegar_prefeitura(linhas):
    for linha in linhas:
        if "PREFEITURA" in linha.upper():
            return linha.strip()
    return None

def pegar_secretaria(linhas):
    for linha in linhas:
        if "SECRETARIA" in linha.upper():
            return linha.strip()
    return None

def pegar_numero_nf(linhas):
    texto = " ".join(linhas)
    match = re.search(r'\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}\s+\d{2}/\d{4}\s+\d+\s+(\d+)', texto)
    if match:
        return match.group(1)
    return None

def pegar_data_hora_emissao(linhas):
    texto = " ".join(linhas)
    match = re.search(r'(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2})', texto)
    if match:
        return match.group(1)
    return None

def pegar_dados_prestador(linhas):
    dados = {
        "razao_social": None, "cnpj": None, "inscricao_municipal": None, 
        "municipio": None, "uf": None, "cep": None,
        "endereco": None, "bairro": None, "email": None
    }
    texto = "\n".join(linhas)
    try:
        bloco = texto.split("Dados do Contribuinte")[1].split("NOTA FISCAL DE SERVIÇOS")[0]
        linhas_bloco = [l.strip() for l in bloco.splitlines() if l.strip()]
        for i, l in enumerate(linhas_bloco):
            if "Nome/Razão Social" in l and "CPF/CNPJ" in l:
                linha_val = linhas_bloco[i+1]
                match = re.search(r'^(.*?)\s+(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', linha_val)
                if match: dados["razao_social"], dados["cnpj"] = match.groups()
            if "Inscrição Municipal" in l and "E-mail" in l:
                linha_val = linhas_bloco[i+1]
                dados["inscricao_municipal"] = linha_val.split()[0]
                m_email = re.search(r'[\w\.-]+@[\w\.-]+', linha_val)
                if m_email: dados["email"] = m_email.group(0)
            if "Endereço" in l and "Bairro" in l:
                linha_val = linhas_bloco[i+1]
                colunas = re.split(r'\s{2,}', linha_val)
                if len(colunas) >= 2:
                    endereco_base = colunas[0].strip()
                    resto = colunas[1].strip()
                    partes_resto = resto.rsplit(' ', 1) 
                    complemento = partes_resto[0].strip() if len(partes_resto) > 1 else ""
                    dados["bairro"] = partes_resto[-1].strip()
                    dados["endereco"] = f"{endereco_base}, {complemento}" if complemento else endereco_base
            if "Cidade/UF" in l:
                linha_val = linhas_bloco[i+1]
                m_cidade_uf = re.search(r'^(.*?)\s*/\s*([A-Z]{2})', linha_val)
                if m_cidade_uf:
                    dados["municipio"] = m_cidade_uf.group(1).strip()
                    dados["uf"] = m_cidade_uf.group(2).strip()
                m_cep = re.search(r'(\d{5}-\d{3})', linha_val)
                if m_cep: dados["cep"] = m_cep.group(1)
    except Exception:
        pass
    return dados

def pegar_dados_tomador(linhas):
    dados = {"razao_social": None, "cnpj": None}
    texto = "\n".join(linhas)
    try:
        bloco = texto.split("Dados do Tomador")[1].split("Inscrição Municipal")[0]
        linhas_bloco = [l.strip() for l in bloco.splitlines() if l.strip()]
        for i, l in enumerate(linhas_bloco):
            if "Nome/Razão Social" in l and "CPF/CNPJ" in l:
                linha_valores = linhas_bloco[i+1]
                match = re.search(r'^(.*?)\s+(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', linha_valores)
                if match:
                    dados["razao_social"] = match.group(1).strip()
                    dados["cnpj"] = match.group(2).strip()
    except Exception:
        pass
    return dados

def pegar_discriminacao_servico(linhas):
    texto_completo = "\n".join(linhas)
    try:
        bloco = texto_completo.split("Descrição do Serviço")[1].split("Base de Cálculo das Retenções")[0]
        linhas_bloco = [l.strip() for l in bloco.splitlines() if l.strip()]
        linhas_filtradas = [l for l in linhas_bloco if "CFOP:" not in l]
        descricao_final = "\n".join(linhas_filtradas)
        return descricao_final
    except Exception:
        pass
    return None

def pegar_valores(linhas):
    vals = {"bruto": "0,00", "liquido": "0,00", "ir": "0,00", "pis": "0,00", "cofins": "0,00", "csll": "0,00", "inss": "0,00", "iss": "0,00"}
    texto_completo = " ".join(linhas)
    m_bruto = re.search(r'Valor do Serviço R\$\s+([\d.,]+)', texto_completo)
    if m_bruto: vals["bruto"] = m_bruto.group(1)
    m_liq = re.search(r'Vlr Liquido NFS-e\s+([\d.,]+)', texto_completo)
    if m_liq: vals["liquido"] = m_liq.group(1)
    m_iss = re.search(r'ISSQN\s+([\d.,]+)\s+Vlr Liquido', texto_completo)
    if m_iss: vals["iss"] = m_iss.group(1)
    m_pis = re.search(r'\(PIS\) R\$\s+([\d.,]+)', texto_completo)
    m_cofins = re.search(r'\(COFINS\) R\$\s+([\d.,]+)', texto_completo)
    m_csll = re.search(r'\(CSLL\) R\$\s+([\d.,]+)', texto_completo)
    m_ir = re.search(r'\(IRRF\) R\$\s+([\d.,]+)', texto_completo)
    m_inss = re.search(r'\(INSS\) R\$\s+([\d.,]+)', texto_completo)
    if m_pis: vals["pis"] = m_pis.group(1)
    if m_cofins: vals["cofins"] = m_cofins.group(1)
    if m_csll: vals["csll"] = m_csll.group(1)
    if m_ir: vals["ir"] = m_ir.group(1)
    if m_inss: vals["inss"] = m_inss.group(1)
    return vals

def pegar_dados_servico(linhas):
    dados = {"codigo": None, "descricao": None}
    
    for i, linha in enumerate(linhas):
        if "Ativ. Descrição da Atividade" in linha:
            if i + 1 < len(linhas):
                conteudo = linhas[i+1].strip()
                match = re.search(r'^(\d{2}\.\d{2})\.?\d*\s*([a-zA-Záàâãéèêíïóôõöúçñ\s.]+)', conteudo, re.IGNORECASE)
                if match:
                    cod_curto = match.group(1).strip()
                    texto_desc = match.group(2).strip()
                    dados["codigo"] = cod_curto
                    match_completo = re.search(r'^([\d.]+)', conteudo)
                    cod_cheio = match_completo.group(1) if match_completo else cod_curto
                    dados["descricao"] = f"{cod_cheio} - {texto_desc}"
                else:
                    dados["descricao"] = conteudo
            break
    return dados