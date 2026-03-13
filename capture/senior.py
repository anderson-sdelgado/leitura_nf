
import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_senior(texto: str):
    linhas = texto.splitlines()

    # print("----------- NOTA SENIOR -----------")
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

    print("----------- NOTA SENIOR -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("--------------------------------------")

def pegar_prefeitura(linhas):
    for linha in linhas:
        if "PREFEITURA" in linha.upper():
            return linha.strip()
    return None

def pegar_numero_nf(linhas):
    for i, linha in enumerate(linhas):
        if re.search(r'\d{2}/\d{2}/\d{4}', linha):
            partes = linha.split()
            if partes:
                return partes[-1]
    return None

def pegar_codigo_verificacao(linhas):
    for i, linha in enumerate(linhas):
        if re.search(r'\d{2}/\d{2}/\d{4}', linha):
            partes = linha.split()
            if len(partes) >= 2:
                return partes[-2]
    return None

def pegar_data_hora_emissao(linhas):
    for linha in linhas:
        match = re.search(r'(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2}:\d{2})', linha)
        if match:
            return f"{match.group(1)} {match.group(2)}"
    return None

def pegar_dados_prestador(linhas):
    dados = {
        "cnpj": None, "inscricao_municipal": None, "razao_social": None, 
        "endereco": None, "bairro": None, "municipio": None, 
        "uf": None, "cep": None, "email": None
    }
    linhas_prestador = []
    dentro_do_bloco = False
    for linha in linhas:
        linha_limpa = linha.strip().upper()
        if "PRESTADOR DO SERVIÇO" in linha_limpa:
            dentro_do_bloco = True
            continue
        if re.search(r'TOMADOR\s+DO\s+SERVIÇO', linha_limpa):
            break
        if dentro_do_bloco:
            linhas_prestador.append(linha.strip())
    for j, texto in enumerate(linhas_prestador):
        texto_up = texto.upper()
        tem_proxima = (j + 1 < len(linhas_prestador))
        if not tem_proxima: continue
        linha_vals = linhas_prestador[j+1]
        if texto_up == "NOME":
            dados["razao_social"] = linha_vals
        elif texto_up == "ENDEREÇO":
            dados["endereco"] = linha_vals
        elif "BAIRRO" in texto_up:
            partes = re.split(r'\s{2,}', linha_vals)
            dados["bairro"] = partes[-1].strip()
        elif "MUNICÍPIO" in texto_up:
            m_cep = re.search(r'(\d{5}-\d{3})', linha_vals)
            if m_cep: dados["cep"] = m_cep.group(1)
            m_uf = re.search(r'\s([A-Z]{2})\s', linha_vals)
            if m_uf: dados["uf"] = m_uf.group(1)
            partes = re.split(r'\s{2,}', linha_vals)
            if partes: dados["municipio"] = partes[0]
        elif "CNPJ" in texto_up:
            m_cnpj = re.search(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', linha_vals)
            if m_cnpj: dados["cnpj"] = m_cnpj.group(1)
            partes_im = linha_vals.split()
            for p in partes_im:
                if p.isdigit() and len(p) > 2:
                    dados["inscricao_municipal"] = p
            m_email = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', linha_vals)
            if m_email: dados["email"] = m_email.group(0).lower()
    return dados

def pegar_dados_tomador(linhas):
    dados = {
        "cnpj": None, 
        "razao_social": None
    }
    linhas_tomador = []
    dentro_do_bloco = False
    for linha in linhas:
        linha_limpa = linha.strip().upper()
        if re.search(r'TOMADOR\s+DO\s+SERVIÇO', linha_limpa):
            dentro_do_bloco = True
            continue
        if "DISCRIMINAÇÃO DOS SERVIÇOS" in linha_limpa or "VALOR TOTAL DA NOTA" in linha_limpa:
            break
        if dentro_do_bloco:
            linhas_tomador.append(linha.strip())
    for j, texto in enumerate(linhas_tomador):
        texto_up = texto.upper()
        tem_proxima = (j + 1 < len(linhas_tomador))
        if not tem_proxima:
            continue
        if texto_up == "NOME":
            dados["razao_social"] = linhas_tomador[j+1]
        elif "CNPJ" in texto_up:
            linha_vals = linhas_tomador[j+1]
            m_cnpj = re.search(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', linha_vals)
            if m_cnpj:
                dados["cnpj"] = m_cnpj.group(1)
    return dados

def pegar_discriminacao_servico(linhas):
    linhas_desc = []
    dentro_do_bloco = False
    for linha in linhas:
        linha_limpa = linha.strip()
        linha_up = linha_limpa.upper()
        if re.search(r'DISCRIMINA[CÇ][AÃ]O|DESCRI[CÇ][AÃ]O', linha_up):
            dentro_do_bloco = True
            continue
        if dentro_do_bloco:
            if "(LC 116/2003)" in linha_up or "VALOR TOTAL DOS SERVIÇOS" in linha_up:
                break
            if linha_limpa and "---" not in linha_limpa:
                if "ITEM" in linha_up and "VALOR" in linha_up:
                    continue
                if linha_up == "VALORES TOTAIS":
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
        if "VALOR TOTAL DOS SERVIÇOS" in linha_up:
            m_bruto = re.search(r'R\$\s*([\d.,]+)', linha)
            if m_bruto: financeiro["bruto"] = m_bruto.group(1)
        if "IMPOSTOS FEDERAIS" in linha_up or ("PIS" in linha_up and "COFINS" in linha_up):
            if i + 1 < len(linhas):
                valores = re.findall(r'R\$\s*([\d.,]+)', linhas[i+1])
                if len(valores) >= 3:
                    financeiro["pis"], financeiro["cofins"], financeiro["csll"] = valores[:3]
                if len(valores) >= 5:
                    financeiro["ir"], financeiro["inss"] = valores[3], valores[4]
        if "VALOR ISS" in linha_up and "VALOR DO ISS" not in linha_up:
            if i + 1 < len(linhas):
                valores_iss = re.findall(r'R\$\s*([\d.,]+)', linhas[i+1])
                if valores_iss: financeiro["iss"] = valores_iss[-1]
        if "VALOR LÍQUIDO DA NFS-E" in linha_up:
            m_liq = re.search(r'R\$\s*([\d.,]+)', linha)
            if m_liq:
                financeiro["liquido"] = m_liq.group(1)
            elif i + 1 < len(linhas):
                m_liq_abaixo = re.search(r'R\$\s*([\d.,]+)', linhas[i+1])
                if m_liq_abaixo: financeiro["liquido"] = m_liq_abaixo.group(1)
    return financeiro

def pegar_dados_servico(linhas):
    servico = {"codigo": None, "descricao": None}
    for i, linha in enumerate(linhas):
        linha_up = linha.upper()
        if "LC 116/2003" in linha_up:
            texto_bloco = linha + " " + (linhas[i+1] if i+1 < len(linhas) else "")
            m_cod = re.search(r'\b(\d{2}\.\d{2})\b', texto_bloco)
            if m_cod:
                servico["codigo"] = m_cod.group(1)
            linhas_descritivo = []
            for j in range(i, i + 5):
                if j >= len(linhas): break
                curr_linha = linhas[j].strip()
                curr_up = curr_linha.upper()
                if any(x in curr_up for x in ["VALOR", "PIS", "COFINS", "CSLL", "ISS"]):
                    break
                limpa = re.sub(r'SERVI[CÇ]O\s*\(LC\s*116/2003\)', '', curr_linha, flags=re.IGNORECASE).strip()
                if limpa:
                    linhas_descritivo.append(limpa)
            descricao_bruta = " ".join(linhas_descritivo)
            desc_limpa = descricao_bruta.strip().lstrip('-').strip()
            servico["descricao"] = desc_limpa
            break
    return servico
