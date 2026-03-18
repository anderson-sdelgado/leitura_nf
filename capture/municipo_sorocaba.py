import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_municipio_sorocaba(texto: str):
    linhas = texto.splitlines()

    # print("----------- NOTA SOROCABA -----------")
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
    nota["SECRET_PREFEIT"] = pegar_secretaria(linhas) # Secretaria da prefeitura. Idem V_NF_SERV. ok
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

    print("----------- NOTA SOROCABA -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("--------------------------------------")

def pegar_codigo_verificacao(linhas):
    for i, linha in enumerate(linhas):
        linha_up = linha.upper().strip()
        if "CÓDIGO DE VERIFICAÇÃO" in linha_up or "CODIGO DE VERIFICACAO" in linha_up:
            m_mesma = re.search(r'\b[A-Za-z0-9]{8,12}\b', linha_up.split("VERIFICAÇÃO")[-1])
            if m_mesma:
                return m_mesma.group(0)
            for j in range(i + 1, i + 3):
                if j < len(linhas):
                    candidato = linhas[j].strip()
                    match = re.search(r'\b(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9]{8,12}\b', candidato)
                    if match:
                        return match.group(0)
    return None

def pegar_prefeitura(linhas):
    for linha in linhas:
        linha_up = linha.upper().strip()
        if "PREFEITURA" in linha_up or "MUNICÍPIO" in linha_up or "MUNICIPIO" in linha_up:
            if any(x in linha_up for x in ["INCIDÊNCIA", "INCIDENCIA", "ENDEREÇO", "ENDERECO", "ESTRADA", "RUA"]):
                continue
            termos_para_remover = [
                r"NÚMERO DA NFS-E.*", 
                r"NUMERO DA NFS-E.*",
                r"PÁGINA.*",
                r"PAGINA.*",
                r"NFS-E.*",
                r"DADOS DA.*",
                r"SECRETARIA.*"
            ]
            
            linha_limpa = linha
            for termo in termos_para_remover:
                linha_limpa = re.sub(termo, '', linha_limpa, flags=re.IGNORECASE)
            resultado = " ".join(linha_limpa.split()).strip()
            if len(resultado) > 10:
                return resultado
    return None

def pegar_secretaria(linhas):
    for linha in linhas:
        if "SECRETARIA" in linha.upper():
            return linha.strip()
    return None

def pegar_numero_nf(linhas):
    for i, linha in enumerate(linhas):
        linha_up = linha.upper().strip()
        
        if "NÚMERO / SÉRIE" in linha_up or "NUMERO / SERIE" in linha_up:
            if i + 1 < len(linhas):
                linha_valores = linhas[i + 1].strip()
                match = re.search(r'(\d+\s*/\s*[A-Z])', linha_valores)
                if match:
                    return match.group(1).strip()
                partes = linha_valores.split()
                if len(partes) >= 4:
                    if "/" in partes[3] or (len(partes) > 4 and partes[4] == "/"):
                         return f"{partes[2]} {partes[3]} {partes[4] if len(partes) > 4 else ''}".strip()
    return None

def pegar_data_hora_emissao(linhas):
    for i, linha in enumerate(linhas):
        linha_up = linha.upper().strip()
        if "DATA E HORA DE EMISSÃO" in linha_up or "DATA E HORA DE EMISSAO" in linha_up:
            d_mesma = re.search(r'(\d{2}/\d{2}/\d{4})', linha)
            h_mesma = re.search(r'(\d{2}:\d{2}:\d{2})', linha)
            if d_mesma and h_mesma:
                return f"{d_mesma.group(1)} {h_mesma.group(1)}"
            data_encontrada = None
            hora_encontrada = None
            for j in range(i + 1, i + 4):
                if j < len(linhas):
                    txt_proximo = linhas[j].strip()
                    if not data_encontrada:
                        d = re.search(r'(\d{2}/\d{2}/\d{4})', txt_proximo)
                        if d: data_encontrada = d.group(1)
                    if not hora_encontrada:
                        h = re.search(r'(\d{2}:\d{2}:\d{2})', txt_proximo)
                        if h: hora_encontrada = h.group(1)
                    if data_encontrada and hora_encontrada:
                        return f"{data_encontrada} {hora_encontrada}"
            if data_encontrada:
                return data_encontrada
    return None


def pegar_dados_prestador(linhas):
    dados = {
        "cnpj": None, "inscricao_estadual": None, "inscricao_municipal": None, 
        "razao_social": None, "endereco": None, "bairro": None, 
        "municipio": None, "uf": None, "cep": None, "email": None
    }
    linhas_prestador = []
    dentro_do_bloco = False
    for linha in linhas:
        linha_limpa = linha.strip().upper()
        if "EMITENTE DA NFS-E" in linha_limpa:
            dentro_do_bloco = True
            continue
        if "TOMADOR DO SERVIÇO" in linha_limpa:
            dentro_do_bloco = False
            break
        if dentro_do_bloco and linha.strip():
            linhas_prestador.append(linha.strip())
    texto_bloco = "\n".join(linhas_prestador)
    m_cnpj = re.search(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', texto_bloco)
    if m_cnpj:
        dados["cnpj"] = m_cnpj.group(1)
    for i, linha in enumerate(linhas_prestador):
        if "INSCRIÇÃO MUNICIPAL" in linha.upper():
            for offset in range(1, 4):
                if i + offset < len(linhas_prestador):
                    candidato = linhas_prestador[i + offset].strip()
                    m_im = re.search(r'^\d{5,8}$', candidato)
                    if m_im:
                        dados["inscricao_municipal"] = m_im.group(0)
                        break
            if dados["inscricao_municipal"]: break
    for i, linha in enumerate(linhas_prestador):
        if "NOME/RAZÃO SOCIAL" in linha.upper():
            if i + 1 < len(linhas_prestador):
                razao_bruta = linhas_prestador[i+1]
                razao_limpa = re.split(r'E-MAIL:', razao_bruta, flags=re.IGNORECASE)[0]
                dados["razao_social"] = razao_limpa.strip()
    for linha in linhas_prestador:
        if "ENDEREÇO:" in linha.upper():
            end_total = linha.split("Endereço:")[-1].strip()
            partes = re.split(r'\s{3,}', end_total)
            dados["endereco"] = partes[0].strip()
            if len(partes) > 1:
                dados["bairro"] = partes[-1].strip()
    m_loc = re.search(r'([A-Z\s]+)\s*/\s*([A-Z]{2}).*?(\d{5}-\d{3})', texto_bloco.upper())
    if m_loc:
        dados["municipio"] = m_loc.group(1).replace("BRASIL", "").strip()
        dados["uf"] = m_loc.group(2).strip()
        dados["cep"] = m_loc.group(3).strip()
    for i, linha in enumerate(linhas_prestador):
        if "E-MAIL:" in linha.upper() or "@" in linha:
            email_candidato = ""
            if "@" in linha:
                email_candidato = linha.split(":")[-1]
            elif i + 1 < len(linhas_prestador) and "@" in linhas_prestador[i+1]:
                email_candidato = linhas_prestador[i+1]
            m_email = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', email_candidato + (linhas_prestador[i+2] if i+2 < len(linhas_prestador) else ""))
            if m_email:
                dados["email"] = m_email.group(0).lower()
                break
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
        if "TOMADOR DO SERVIÇO" in linha_limpa or "TOMADOR DO SERVICO" in linha_limpa:
            dentro_do_bloco = True
            continue
        if "DESCRIÇÃO DO SERVIÇO" in linha_limpa or "DESCRICAO DO SERVICO" in linha_limpa:
            dentro_do_bloco = False
            break
        if dentro_do_bloco and linha.strip():
            linhas_tomador.append(linha.strip())
    texto_bloco = "\n".join(linhas_tomador)
    m_cnpj = re.search(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', texto_bloco)
    if m_cnpj:
        dados["cnpj"] = m_cnpj.group(1)
    for i, linha in enumerate(linhas_tomador):
        linha_up = linha.upper()
        if "NOME/NOME" in linha_up or "RAZÃO SOCIAL" in linha_up:
            if i + 1 < len(linhas_tomador):
                razao_bruta = linhas_tomador[i+1].strip()
                razao_limpa = re.split(r'E-MAIL:', razao_bruta, flags=re.IGNORECASE)[0]
                razao_limpa = re.split(r'\s{3,}', razao_limpa)[0]
                if dados["cnpj"]:
                    razao_limpa = razao_limpa.replace(dados["cnpj"], "")
                dados["razao_social"] = razao_limpa.strip("- ").strip()
                break
    return dados

def pegar_discriminacao_servico(linhas):
    descricao_linhas = []
    dentro_da_secao = False
    for linha in linhas:
        linha_up = linha.strip().upper()
        if "DESCRIÇÃO DO SERVIÇO" in linha_up or "DESCRICAO DO SERVICO" in linha_up:
            dentro_da_secao = True
            continue
        if "DETALHAMENTO DO SERVIÇO" in linha_up or "DETALHAMENTO DO SERVICO" in linha_up:
            dentro_da_secao = False
            break
        if dentro_da_secao:
            linha_limpa = linha.strip()
            if linha_limpa and linha_limpa != "-":
                descricao_linhas.append(linha_limpa)
    texto_completo = "\n".join(descricao_linhas).strip()
    return texto_completo if texto_completo else None

def pegar_valores(linhas):
    financeiro = {
        "pis": "0,00", "cofins": "0,00", "csll": "0,00", 
        "ir": "0,00", "inss": "0,00", "iss": "0,00", 
        "bruto": "0,00", "liquido": "0,00"
    }
    for i, linha in enumerate(linhas):
        linha_up = linha.upper().strip()
        if "VALOR SERVIÇO" in linha_up and "DEDUÇÕES" in linha_up:
            if i + 1 < len(linhas):
                valores = re.findall(r'[\d.,]+', linhas[i+1])
                if valores:
                    financeiro["bruto"] = valores[0]
        if "ALÍQUOTA" in linha_up and "VALOR ISSQN" in linha_up:
            if i + 1 < len(linhas):
                valores = re.findall(r'[\d.,]+', linhas[i+1])
                if valores:
                    financeiro["iss"] = valores[-1]
        if "ISSQN (R$)" in linha_up and "IRRF (R$)" in linha_up:
            if i + 1 < len(linhas):
                valores = re.findall(r'[\d.,]+', linhas[i+1])
                if len(valores) >= 6:
                    financeiro["ir"] = valores[1]
                    financeiro["pis"] = valores[2]
                    financeiro["cofins"] = valores[3]
                    financeiro["inss"] = valores[4]
                    financeiro["csll"] = valores[5]
        if "RETENÇÕES (R$)" in linha_up and "VALOR LÍQUIDO" in linha_up:
            if i + 1 < len(linhas):
                valores = re.findall(r'[\d.,]+', linhas[i+1])
                if valores:
                    financeiro["liquido"] = valores[-1]
    for k in financeiro:
        if not financeiro[k]:
            financeiro[k] = "0,00"
    return financeiro


def pegar_dados_servico(linhas):
    servico = {"codigo": None, "descricao": None}
    for i, linha in enumerate(linhas):
        linha_up = linha.upper().strip()
        if "SERVIÇO:" in linha_up and "DETALHAMENTO" not in linha_up:
            texto_servico = linha.split("Serviço:")[-1].strip()
            if len(texto_servico) < 5 and i + 1 < len(linhas):
                texto_servico = linhas[i+1].strip()
            m_cod = re.search(r'(\d{2}\.\d{2})', texto_servico)
            if m_cod:
                cod_encontrado = m_cod.group(1)
                servico["codigo"] = cod_encontrado
                partes = re.split(rf'{re.escape(cod_encontrado)}\s*-\s*', texto_servico)
                if len(partes) > 1:
                    desc_limpa = partes[1].strip()
                    servico["descricao"] = f"{cod_encontrado} - {desc_limpa}"
                else:
                    desc_limpa = texto_servico.replace(cod_encontrado, "").strip("- ").strip()
                    servico["descricao"] = f"{cod_encontrado} - {desc_limpa}"
                break
    return servico