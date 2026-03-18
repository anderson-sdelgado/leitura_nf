import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def limpar_linha(linha):
    return re.sub(r'^\d+:\s*', '', linha).strip()

def leitura_giss(texto: str):
    linhas = texto.splitlines()
        
    # print("----------- NOTA GISS -----------")
    # for numero, linha in enumerate(linhas, start=1): 
    #     print(f"{linha}")
    # print("-------------------------")

    prestador = pegar_dados_prestador(linhas)
    tomador = pegar_dados_tomador(linhas)
    tributos = pegar_tributos_federais(linhas)
    servico = pegar_atividade_economica(linhas)

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
    nota["PREFEIT"] = pegar_prefeitura(linhas) # Nome da prefeitura. Idem V_NF_SERV.
    nota["SECRET_PREFEIT"] = pegar_secretaria(linhas) # Secretaria da prefeitura. Idem V_NF_SERV.
    nota["NRO_NF"] = pegar_numero_nf(linhas) # Número da NF. Idem V_NF_SERV.
    nota["DT_EMISS"] = pegar_data_hora_emissao(linhas) # Data de emissão da NF. Idem V_NF_SERV.
    nota["PS_RAZ_SOC_NOME"] = prestador['razao_social'] # Nome do prestador de serviço. Idem V_NF_SERV.
    nota["PS_CNPJ_CPF"] = prestador['cnpj'] # CNPJ do prestador de serviço. Idem V_NF_SERV.
    nota["PS_INSC_MUNIC"] = prestador['inscricao'] # Inscrição municipal do prestador de serviço. Idem V_NF_SERV.
    nota["PS_INSC_EST"] = None # Inscrição estadual do prestador de serviço. Idem V_NF_SERV.
    nota["PS_MUNIC"] = prestador['municipio'] # Nome do município do prestador de serviço. Idem V_NF_SERV.
    nota["PS_UF"] = prestador['uf'] # Sigla da UF do prestador de serviço. Idem V_NF_SERV.
    nota["PS_ENDERECO"] = prestador['endereco_completo'] # Endereço do prestador de serviço. Idem V_NF_SERV.
    nota["PS_BAIRRO"] = prestador['bairro'] # Bairro do prestador de serviço. Idem V_NF_SERV.
    nota["PS_CEP"] = prestador['cep'] # CEP do prestador de serviço. Idem V_NF_SERV.
    nota["PS_EMAIL"] = prestador['email'] # E-mail do prestador de serviço. Idem V_NF_SERV.
    nota["TS_RAZ_SOC_NOME"] = tomador['razao_social'] # Nome do tomador de serviço - empresa usuária. Idem V_NF_SERV.
    nota["TS_CNPJ_CPF"] = tomador['cnpj'] # CNPJ do tomador de serviço - empresa usuária. Idem V_NF_SERV.
    nota["DESC_SERV"] = pegar_discriminacao_servico(linhas) # Descrição do serviço. Idem V_NF_SERV.
    nota["VL_BRUTO"] = extrair_valor(pegar_valor_servico(linhas)) # Valor bruto. Idem V_NF_SERV.
    nota["VL_LIQ"] = extrair_valor(pegar_valor_liquido(linhas)) # Valor líquido. Idem V_NF_SERV.
    nota["VL_PIS"] = extrair_valor(tributos["pis"]) # Valor do PIS. Idem V_NF_SERV.
    nota["VL_COFINS"] = extrair_valor(tributos["cofins"]) # Valor da Cofins. Idem V_NF_SERV.
    nota["VL_IR"] = extrair_valor(tributos["ir"]) # Valor do IR. Idem V_NF_SERV.
    nota["VL_INSS"] = extrair_valor(tributos["inss"]) # Valor do INSS. Idem V_NF_SERV.
    nota["VL_CSLL"] = extrair_valor(tributos["csll"]) # Valor da CSLL. Idem V_NF_SERV.
    nota["VL_ISS"] = extrair_valor(pegar_issqn(linhas)) # Valor do ISS. Idem V_NF_SERV.
    nota["COD_SERVICO"] = servico["codigo"] # Código do serviço. Idem V_NF_SERV.
    nota["COD_SERVICO_ORIGINAL"] = servico["descricao_completa"] # Código do serviço - informação original. Idem V_NF_SERV.

    print("----------- NOTA GISS -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("-----------------------------------")

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
    proxima_e_numero = False
    for linha in linhas:
        linha_limpa = linha.strip()
        if proxima_e_numero and linha_limpa:
            match = re.search(r'(\d+)', linha_limpa)
            if match:
                return match.group(1)
        if "NFS-e" in linha:
            match_mesma_linha = re.search(r'NFS-e\s+(\d+)', linha)
            if match_mesma_linha:
                return match_mesma_linha.group(1)
            proxima_e_numero = True
    return None

def pegar_data_hora_emissao(linhas):
    pular_para_proxima = False
    for linha in linhas:
        linha_limpa = linha.strip()
        if pular_para_proxima and linha_limpa:
            match = re.search(r'(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})', linha_limpa)
            if match:
                return match.group(1)
        if "Emissão da NFS-e" in linha:
            pular_para_proxima = True
    return None

def pegar_dados_prestador(linhas):
    dentro_secao_prestador = False
    dados = {
        "razao_social": None, 
        "cnpj": None, 
        "inscricao": None, # Agora será preenchido
        "municipio": None,
        "uf": None,
        "endereco_completo": None,
        "bairro": None,
        "cep": None,
        "email": None 
    }
    rua, numero, complemento = "", "", ""
    for linha in linhas:
        if "Prestador de Serviço" in linha:
            dentro_secao_prestador = True
            continue
        if dentro_secao_prestador:
            # E-mail
            if "E-mail:" in linha:
                match_email = re.search(r'E-mail:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', linha)
                dados["email"] = match_email.group(1).strip() if match_email else None
            
            # CPF/CNPJ e INSCRIÇÃO (Correção aqui)
            if "CPF/CNPJ:" in linha:
                match_cnpj = re.search(r'CPF/CNPJ:\s*([\d./-]+)', linha)
                if match_cnpj: dados["cnpj"] = match_cnpj.group(1).strip()
                
                match_insc = re.search(r'Inscrição\s+([\w.-]+)', linha) # Pega a inscrição municipal
                if match_insc: dados["inscricao"] = match_insc.group(1).strip()

            # CEP, Município e UF
            if "CEP:" in linha:
                match_cep = re.search(r'CEP:\s*([\d-]{8,9})', linha)
                if match_cep: dados["cep"] = match_cep.group(1).strip()
            if "Município:" in linha:
                match_mun = re.search(r'Município:\s*(.*?)(?=\s+UF:|$)', linha)
                if match_mun: dados["municipio"] = match_mun.group(1).strip()
                match_uf = re.search(r'UF:\s*([A-Z]{2})', linha)
                if match_uf: dados["uf"] = match_uf.group(1).strip()

            # Bairro e Endereço
            if "Bairro:" in linha:
                dados["bairro"] = linha.split("Bairro:")[1].strip()
            if "Endereço" in linha:
                match_rua = re.search(r'Endereço[:\s]+(.*?)(?=\s+Número:|$)', linha)
                if match_rua: rua = match_rua.group(1).strip()
            if "Número:" in linha:
                match_num = re.search(r'Número:\s*([\w\s/.-]+?)(?=\s{2,}|Bairro:|$)', linha)
                if match_num: numero = match_num.group(1).strip()
            if "Complemento:" in linha:
                match_comp = re.search(r'Complemento:\s*(.*?)(?=\s{2,}|Bairro:|$)', linha)
                if match_comp: complemento = match_comp.group(1).strip()
            
            if "Nome/Razão Social:" in linha:
                dados["razao_social"] = linha.split("Nome/Razão Social:")[1].strip()
            
            if "Tomador de Serviço" in linha:
                break

    partes = [rua, numero]
    if complemento: partes.append(complemento)
    dados["endereco_completo"] = ", ".join([p for p in partes if p])
    return dados

def pegar_dados_tomador(linhas):
    dentro_secao_tomador = False
    dados = {
        "razao_social": None,
        "cnpj": None
    }
    for linha in linhas:
        if "Tomador de Serviço" in linha:
            dentro_secao_tomador = True
            continue
        if dentro_secao_tomador:
            if "CPF/CNPJ:" in linha:
                match_cnpj = re.search(r'CPF/CNPJ:\s*([\d./-]+)', linha)
                if match_cnpj:
                    dados["cnpj"] = match_cnpj.group(1).strip()
            if "Nome/Razão Social:" in linha:
                dados["razao_social"] = linha.split("Nome/Razão Social:")[1].strip()
            if "Atividade Econômica" in linha:
                break
    return dados

def pegar_discriminacao_servico(linhas):
    descricao_linhas = []
    dentro_da_secao = False
    for linha in linhas:
        if "Discriminação do Serviço" in linha:
            dentro_da_secao = True
            continue
        if "Tributos Federais" in linha:
            break
        if dentro_da_secao:
            linha_limpa = linha.strip()
            descricao_linhas.append(linha_limpa)
    texto_completo = "\n".join(descricao_linhas).strip()
    return texto_completo if texto_completo else None

def pegar_valor_servico(linhas):
    for linha in linhas:
        if "Valor do Serviço" in linha:
            match = re.search(r'Valor do Serviço\s+([\d.,]+)', linha)
            if match:
                return match.group(1).strip()
    return "0,00"

def pegar_valor_liquido(linhas):
    for linha in linhas:
        if "Valor Líquido" in linha:
            match = re.search(r'Valor Líquido\s+([\d.,]+)', linha)
            if match:
                return match.group(1).strip()
    return "0,00"

def pegar_tributos_federais(linhas):
    tributos = {
        "pis": "0,00",
        "cofins": "0,00",
        "inss": "0,00",
        "ir": "0,00",
        "csll": "0,00"
    }
    proxima_e_valor = False
    for linha in linhas:
        if "PIS" in linha and "COFINS" in linha and "CSLL" in linha:
            proxima_e_valor = True
            continue
        if proxima_e_valor:
            valores = re.findall(r'(\d{1,3}(?:\.\d{3})*,\d{2})', linha)
            if len(valores) >= 5:
                tributos["pis"] = valores[0]
                tributos["cofins"] = valores[1]
                tributos["inss"] = valores[2]
                tributos["ir"] = valores[3]
                tributos["csll"] = valores[4]
            break     
    return tributos

def pegar_issqn(linhas):
    for linha in linhas:
        if "ISSQN" in linha:
            match = re.search(r'ISSQN\s+([\d.,]+)$|ISSQN\s+(\d{1,3}(?:\.\d{3})*,\d{2})', linha)
            if match:
                valor = match.group(1) if match.group(1) else match.group(2)
                return valor.strip()
    return "0,00"

def pegar_atividade_economica(linhas):
    dados = {
        "codigo":  None,
        "descricao_completa": None
    }
    for i, linha in enumerate(linhas):
        if "Atividade Econômica" in linha:
            if i + 1 < len(linhas):
                linha_alvo = linhas[i+1].strip()
                dados["descricao_completa"] = linha_alvo
                match_codigo = re.search(r'^([\d.]+)', linha_alvo)
                if match_codigo:
                    dados["codigo"] = match_codigo.group(1).strip()
            break
    return dados