import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_sgicorp(texto: str):
    linhas = texto.splitlines()

    # print("----------- NOTA SAO JOSE DO RIO PRETO -----------")
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
    nota["PS_EMAIL"] = prestador['email'] # E-mail do prestador de serviço. Idem V_NF_SERV. ok
    nota["TS_RAZ_SOC_NOME"] = tomador['razao_social'] # Nome do tomador de serviço - empresa usuária. Idem V_NF_SERV. ok
    nota["TS_CNPJ_CPF"] = tomador['cnpj'] # CNPJ do tomador de serviço - empresa usuária. Idem V_NF_SERV. ok ok
    nota["DESC_SERV"] = pegar_discriminacao(linhas) # Descrição do serviço. Idem V_NF_SERV. ok
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

    print("----------- NOTA SAO JOSE DO RIO PRETO -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("--------------------------------------")

def pegar_autenticidade(linhas):
    texto_topo = " ".join(linhas[:15])
    match = re.search(r'Código de Verificação\s+([A-Z0-9]{5,15})', texto_topo)
    if match:
        return match.group(1).strip()
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
    texto_topo = " ".join(linhas[:10])
    match = re.search(r'NFS-e\s+(\d+)', texto_topo)
    return match.group(1) if match else None

def pegar_data_hora_emissao(linhas):
    texto_topo = " ".join(linhas[:10])
    match = re.search(r'Emissão\s+(\d{2}/\d{2}/\d{4})', texto_topo)
    return match.group(1) if match else None

def pegar_dados_prestador(linhas):
    dados = {
        "razao_social": None, 
        "cnpj": None, 
        "inscricao_municipal": None, 
        "endereco": None, 
        "bairro": None, 
        "cep": None,
        "uf": None,
        "municipio": None,
        "email": None
    }
    texto_bloco = " ".join(linhas)
    match_rs = re.search(r"Razão Social / Nome\s+(.*?)\s+CNPJ", texto_bloco)
    if match_rs: dados["razao_social"] = match_rs.group(1).strip()
    match_cnpj = re.search(r"CNPJ / CPF\s+([\d./-]{14,18})", texto_bloco)
    if match_cnpj: dados["cnpj"] = match_cnpj.group(1).strip()
    match_im = re.search(r"Inscrição Municipal\s+(\d+)", texto_bloco)
    if match_im: dados["inscricao_municipal"] = match_im.group(1).strip()
    match_mun_uf = re.search(r"Municipio\s+(.*?)\s+UF\s+([A-Z]{2})", texto_bloco)
    if match_mun_uf:
        dados["municipio"] = match_mun_uf.group(1).strip()
        dados["uf"] = match_mun_uf.group(2).strip()
    match_email = re.search(r'E-mail\s*:\s*([\w\.-]+@[\w\.-]+\.\w+)', texto_bloco, re.IGNORECASE)
    if match_email:
        dados["email"] = match_email.group(1).strip()
    else:
        match_email_solto = re.search(r'([\w\.-]+@[\w\.-]+\.\w+)', texto_bloco)
        if match_email_solto:
            dados["email"] = match_email_solto.group(1).strip()
    match_end_total = re.search(r"Endereço e Cep\s+(.*?)\s+-\s+CEP\s*:\s*(\d{8})", texto_bloco)
    if match_end_total:
        conteudo_endereco = match_end_total.group(1).strip()
        dados["cep"] = match_end_total.group(2).strip()
        match_divisao = re.search(r"(.*?\d+)[ ,]+(.*?)$", conteudo_endereco)
        if match_divisao:
            dados["endereco"] = match_divisao.group(1).strip()
            dados["bairro"] = match_divisao.group(2).strip()
        else:
            dados["endereco"] = conteudo_endereco
    return dados

def pegar_dados_tomador(linhas):
    dados = {"razao_social": None, "cnpj": None}
    texto_completo = " ".join(linhas)
    if "Dados do Tomador de Serviços" in texto_completo:
        try:
            bloco_tomador = texto_completo.split("Dados do Tomador de Serviços")[1].split("Discriminação dos Serviços")[0]
            match_rs = re.search(r"Razão Social / Nome\s+(.*?)\s+CNPJ", bloco_tomador)
            if match_rs:
                dados["razao_social"] = match_rs.group(1).strip()
            match_cnpj = re.search(r"CNPJ / CPF\s+([\d./-]{11,18})", bloco_tomador)
            if match_cnpj:
                dados["cnpj"] = match_cnpj.group(1).strip()
        except IndexError:
            pass
    return dados

def pegar_discriminacao(linhas):
    texto_total = "\n".join(linhas)
    match = re.search(
        r'Discriminação dos Serviços\s*(.*?)\s*(?=Código do Serviço / Atividade|Valor Total da NFS-e|$)', 
        texto_total, 
        re.DOTALL | re.IGNORECASE
    )
    
    if match:
        conteudo = match.group(1).strip()
        return conteudo.replace("\n", " ").strip()
    return None

def pegar_valores(linhas):
    vals = {
        "bruto": "0,00", "liquido": "0,00", 
        "ir": "0,00", "pis": "0,00", "cofins": "0,00", "csll": "0,00",
        "inss": "0,00", "iss": "0,00"
    }
    texto_completo = " ".join(linhas)
    m_bruto = re.search(r'Valor dos Serviços\s*R\$\s*([\d.,]+)', texto_completo, re.IGNORECASE)
    if m_bruto: vals["bruto"] = m_bruto.group(1).strip()
    m_liq = re.search(r'VALOR TOTAL DA NFS-e\s*R\$\s*([\d.,]+)', texto_completo, re.IGNORECASE)
    if m_liq: vals["liquido"] = m_liq.group(1).strip()
    m_iss = re.search(r'Valor ISS\s*R\$\s*([\d.,]+)', texto_completo, re.IGNORECASE)
    if m_iss: 
        vals["iss"] = m_iss.group(1).strip()
    m_inss = re.search(r'INSS\s*\(R\$\)\s*([\d.,]+)', texto_completo, re.IGNORECASE)
    if m_inss: vals["inss"] = m_inss.group(1).strip()
    m_pis = re.search(r'PIS\s*\(R\$\)\s*([\d.,]+)', texto_completo, re.IGNORECASE)
    if m_pis: vals["pis"] = m_pis.group(1).strip()
    m_cofins = re.search(r'COFINS\s*\(R\$\)\s*([\d.,]+)', texto_completo, re.IGNORECASE)
    if m_cofins: vals["cofins"] = m_cofins.group(1).strip()
    m_ir = re.search(r'IRRF\s*\(R\$\)\s*([\d.,]+)', texto_completo, re.IGNORECASE)
    if m_ir: vals["ir"] = m_ir.group(1).strip()
    m_csll = re.search(r'CSLL\s*\(R\$\)\s*([\d.,]+)', texto_completo, re.IGNORECASE)
    if m_csll: vals["csll"] = m_csll.group(1).strip()
    return vals

def pegar_dados_servico(linhas):
    dados = {"codigo": None, "descricao": None}
    texto_total = " ".join(linhas)
    match_bloco = re.search(
        r'Código do Serviço / Atividade\s*(.*?)\s*(?=Detalhamento Especifico da Construção Civil|$)', 
        texto_total, 
        re.IGNORECASE
    )
    if match_bloco:
        conteudo_bloco = match_bloco.group(1).strip()
        match_cod = re.search(r'^([\d.]+)', conteudo_bloco)
        if match_cod:
            dados["codigo"] = match_cod.group(1).strip()
        match_desc = re.search(r'[/ ]+\s*([\d.]+.*)', conteudo_bloco)
        if match_desc:
            dados["descricao"] = match_desc.group(1).strip()
        else:
            dados["descricao"] = conteudo_bloco
    return dados