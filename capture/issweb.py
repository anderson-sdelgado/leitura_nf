
import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_issweb(texto: str):
    linhas = texto.splitlines()

    # print("----------- NOTA ISSWEB -----------")
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

    print("----------- NOTA ISSWEB -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("--------------------------------------")

def pegar_prefeitura(linhas):
    for linha in linhas:
        linha_up = linha.upper().strip()
        if "PREFEITURA" in linha_up or "MUNICÍPIO" in linha_up or "MUNICIPIO" in linha_up:
            if any(x in linha_up for x in ["INCIDÊNCIA", "ENDEREÇO", "ESTRADA", "RUA"]):
                continue
            termos_para_remover = [
                r"NÚMERO DA NFS-E.*", 
                r"NUMERO DA NFS-E.*",
                r"PÁGINA.*",
                r"PAGINA.*",
                r"NFS-E.*"
            ]
            linha_limpa = linha
            for termo in termos_para_remover:
                linha_limpa = re.sub(termo, '', linha_limpa, flags=re.IGNORECASE)
            resultado = " ".join(linha_limpa.split()).strip()
            if len(resultado) > 10:
                return resultado
    return None

def pegar_numero_nf(linhas):
    for i, linha in enumerate(linhas):
        linha_up = linha.upper().strip()
        if "NÚMERO DA NFS-E" in linha_up or "NUMERO DA NFS-E" in linha_up:
            m = re.search(r'(?<![\d\.])(\d+)(?![\d\.])', linha_up.replace("NÚMERO DA NFS-E", ""))
            if m:
                return m.group(1)
            for j in range(i + 1, i + 3):
                if j < len(linhas):
                    candidato = linhas[j].strip()
                    if candidato.isdigit():
                        return candidato
                    m_prox = re.search(r'^(\d+)$', candidato)
                    if m_prox:
                        return m_prox.group(1)
    return None

def pegar_codigo_verificacao(linhas):
    for i, linha in enumerate(linhas):
        linha_up = linha.upper().strip()
        if "CÓDIGO DE VERIFICAÇÃO" in linha_up or "CODIGO DE VERIFICACAO" in linha_up:
            for j in range(i + 1, i + 4):
                if j < len(linhas):
                    candidato = linhas[j].strip().upper()
                    if any(x in candidato for x in ["AUTENTICIDADE", "NÚMERO", "PÁGINA"]):
                        continue
                    m_prox = re.search(r'\b(?=.*\d)[A-Z0-9]{6,12}\b', candidato)
                    if m_prox:
                        return m_prox.group(0)
            linha_limpa = linha_up.replace("CÓDIGO DE VERIFICAÇÃO", "").replace("AUTENTICIDADE", "")
            m_mesma = re.search(r'\b(?=.*\d)[A-Z0-9]{6,12}\b', linha_limpa)
            if m_mesma:
                return m_mesma.group(0)
    return None

def pegar_data_hora_emissao(linhas):
    for i, linha in enumerate(linhas):
        linha_up = linha.upper().strip()
        if "DATA E HORA DE EMISSÃO" in linha_up or "DATA E HORA DE EMISSAO" in linha_up:
            data_match = re.search(r'(\d{2}/\d{2}/\d{4})', linha)
            hora_match = re.search(r'(\d{2}:\d{2}:\d{2})', linha)
            if data_match and hora_match:
                return f"{data_match.group(1)} {hora_match.group(1)}"
            for j in range(i + 1, i + 3):
                if j < len(linhas):
                    txt_proximo = linhas[j].strip()
                    d = re.search(r'(\d{2}/\d{2}/\d{4})', txt_proximo)
                    h = re.search(r'(\d{2}:\d{2}:\d{2})', txt_proximo)
                    if d and h:
                        return f"{d.group(1)} {h.group(1)}"
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
        if "PRESTADOR DE SERVIÇOS" in linha_limpa:
            dentro_do_bloco = True
            continue
        if "TOMADOR DE SERVIÇOS" in linha_limpa:
            dentro_do_bloco = False
            break
        if dentro_do_bloco and linha.strip():
            linhas_prestador.append(linha.strip())
    texto_bloco = "\n".join(linhas_prestador)
    m_cnpj = re.search(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', texto_bloco)
    if m_cnpj:
        dados["cnpj"] = m_cnpj.group(1)
    cnpj_so_numeros = re.sub(r'\D', '', dados["cnpj"] or "")
    padrao_ie = r'\b\d{3}\.\d{3}\.\d{3}\.\d{3}\b|\b\d{12}\b'
    todas_ies = re.findall(padrao_ie, texto_bloco)
    for ie in todas_ies:
        ie_limpa = re.sub(r'\D', '', ie)
        if ie_limpa != cnpj_so_numeros:
            dados["inscricao_estadual"] = ie
            break
    for i, linha in enumerate(linhas_prestador):
        linha_up = linha.upper()
        if "INSCRIÇÃO MUNICIPAL" in linha_up and i + 1 < len(linhas_prestador):
            val_line = linhas_prestador[i+1]
            cands = re.findall(r'\b\d{4,11}\b', val_line)
            ie_num = re.sub(r'\D', '', dados["inscricao_estadual"] or "")
            for c in cands:
                if c != ie_num and c not in cnpj_so_numeros:
                    if not dados["inscricao_municipal"]:
                        dados["inscricao_municipal"] = c
                        break
            nome = val_line
            if dados["cnpj"]: nome = nome.replace(dados["cnpj"], "")
            if dados["inscricao_estadual"]: nome = nome.replace(dados["inscricao_estadual"], "")
            if dados["inscricao_municipal"]: nome = nome.replace(dados["inscricao_municipal"], "")
            nome = re.sub(r'[\d\./-]{4,}', '', nome)
            nome = re.sub(r'\b\d{1,4}\b', '', nome)
            dados["razao_social"] = re.sub(r'\s{2,}', ' ', nome).strip(" -./").strip()
    for i, linha in enumerate(linhas_prestador):
        l_up = linha.upper()
        if "LOGRADOURO" in l_up and i + 1 < len(linhas_prestador):
            val = linhas_prestador[i+1].replace("RUARUA", "RUA ").strip()
            if ";" in val:
                partes_semicolon = val.split(";")
                dados["endereco"] = partes_semicolon[0].strip()
                dados["bairro"] = partes_semicolon[-1].strip()
            else:
                partes = re.split(r'\s{3,}', val)
                dados["endereco"] = partes[0].strip()
                if len(partes) > 1:
                    dados["bairro"] = partes[-1].strip()
    m_local = re.search(r'(\d{5}-?\d{3})\s+([A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇ\s.-]+)-([A-Z]{2})', texto_bloco.upper())
    if m_local:
        dados["cep"] = m_local.group(1)
        dados["municipio"] = m_local.group(2).strip()
        dados["uf"] = m_local.group(3).strip()
    m_email = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', texto_bloco)
    if m_email:
        dados["email"] = m_email.group(0).lower()
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
        if "TOMADOR DE SERVIÇOS" in linha_limpa or "TOMADOR DO SERVIÇO" in linha_limpa:
            dentro_do_bloco = True
            continue
        if any(x in linha_limpa for x in ["DISCRIMINAÇÃO DOS SERVIÇOS", "DISCRIMINACAO DOS SERVICOS", "VALOR TOTAL"]):
            break
        if dentro_do_bloco and linha.strip():
            linhas_tomador.append(linha.strip())
    texto_bloco = "\n".join(linhas_tomador)
    m_cnpj = re.search(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', texto_bloco)
    if m_cnpj:
        dados["cnpj"] = m_cnpj.group(1)
    for j, texto in enumerate(linhas_tomador):
        texto_up = texto.upper()
        if "NOME" in texto_up or "RAZÃO SOCIAL" in texto_up:
            if j + 1 < len(linhas_tomador):
                linha_vals = linhas_tomador[j+1]
                if dados["cnpj"] and dados["cnpj"] in linha_vals:
                    temp_nome = linha_vals.replace(dados["cnpj"], "")
                    temp_nome = re.sub(r'\b\d{8,15}\b', '', temp_nome)
                    dados["razao_social"] = re.sub(r'\s{2,}', ' ', temp_nome).strip("- ").strip()
                else:
                    dados["razao_social"] = linha_vals.strip()
    return dados

def pegar_discriminacao_servico(linhas):
    discriminacao_formatada = []
    dentro_do_bloco = False
    temp_item = None 
    inicio_bloco = "DISCRIMINAÇÃO DOS SERVIÇOS"
    fim_bloco = "IMPOSTO SOBRE SERVIÇOS DE QUALQUER NATUREZA"
    for linha in linhas:
        linha_up = linha.upper().strip()
        if inicio_bloco in linha_up:
            dentro_do_bloco = True
            continue
        if dentro_do_bloco and fim_bloco in linha_up:
            break
        if dentro_do_bloco and linha.strip():
            if "QTDE." in linha_up and "UNITÁRIO" in linha_up:
                continue
            m = re.search(r'^(\d+[\d.,]*)\s+([A-Z]{1,3})\s+(.*?)(?:\s+(\d+[\d.,]*)\s+(R\$\s*\d+[\d.,]*))?$', linha.strip())
            if m and m.group(1) and m.group(2):
                if temp_item:
                    discriminacao_formatada.append(self._formatar_item_servico(temp_item))
                temp_item = {
                    "qtde": m.group(1),
                    "un": m.group(2),
                    "desc": m.group(3) if m.group(3) else "",
                    "vlr_un": m.group(4) if m.group(4) else "",
                    "total": m.group(5) if m.group(5) else ""
                }
            
            elif temp_item:
                texto_extra = linha.strip()
                temp_item["desc"] += f" {texto_extra}"
            else:
                discriminacao_formatada.append(re.sub(r'\s{2,}', ' ', linha.strip()))
    if temp_item:
        item_final = f"Qtde.: {temp_item['qtde']}, Un. Medida: {temp_item['un']}, Descrição: {temp_item['desc'].strip()}, Vlr. Unitário: {temp_item['vlr_un']}, Total: {temp_item['total']};"
        discriminacao_formatada.append(item_final)
    return " ".join(discriminacao_formatada).strip()

def pegar_valores(linhas):
    financeiro = {
        "pis": "0,00", "cofins": "0,00", "csll": "0,00", 
        "ir": "0,00", "inss": "0,00", "iss": "0,00", 
        "bruto": "0,00", "liquido": "0,00"
    }
    for i, linha in enumerate(linhas):
        linha_up = linha.upper().strip()
        if "VALOR TOTAL DOS SERVIÇOS" in linha_up:
            m = re.search(r'R\$\s*([\d.,]+)', linha)
            if not m and i + 1 < len(linhas): m = re.search(r'R\$\s*([\d.,]+)', linhas[i+1])
            if m: financeiro["bruto"] = m.group(1)
        if "VALOR LÍQUIDO" in linha_up:
            m = re.search(r'R\$\s*([\d.,]+)', linha)
            if not m and i + 1 < len(linhas): m = re.search(r'R\$\s*([\d.,]+)', linhas[i+1])
            if m: financeiro["liquido"] = m.group(1)
        if "PIS" in linha_up and "COFINS" in linha_up:
            titulos = linha_up.split()
            if i + 1 < len(linhas):
                valores_linha = re.findall(r'R\$\s*([\d.,]+)', linhas[i+1])
                mapa_siglas = {
                    "PIS": "pis",
                    "COFINS": "cofins",
                    "CSLL": "csll",
                    "IRRF": "ir",
                    "IR": "ir",
                    "INSS": "inss",
                    "CP": "inss"
                }
                titulos_encontrados = [t for t in titulos if t in mapa_siglas]
                
                for idx, titulo in enumerate(titulos_encontrados):
                    if idx < len(valores_linha):
                        chave_destino = mapa_siglas[titulo]
                        financeiro[chave_destino] = valores_linha[idx]
        if "VALOR DO ISS" in linha_up:
            m = re.search(r'R\$\s*([\d.,]+)', linha)
            if not m and i + 1 < len(linhas): m = re.search(r'R\$\s*([\d.,]+)', linhas[i+1])
            if m: financeiro["iss"] = m.group(1)
    for k in financeiro:
        if financeiro[k] is None or financeiro[k] == "":
            financeiro[k] = "0,00"
    return financeiro

def pegar_dados_servico(linhas):
    servico = {"codigo": None, "descricao": None}
    for i, linha in enumerate(linhas):
        linha_up = linha.upper().strip()
        if "LC 116/2003" in linha_up:
            m_cod = re.search(r'LC\s*116/2003:(\d{6})', linha, re.IGNORECASE)
            if m_cod:
                cod_6_digitos = m_cod.group(1)
                servico["codigo"] = cod_6_digitos[:4]
                if i + 1 < len(linhas):
                    linha_desc = linhas[i+1].strip()
                    limpa = re.sub(r'\d{1,2},\d{2}%', '', linha_desc)
                    limpa = re.sub(r'\b\d{10,}\b', '', limpa)
                    limpa = re.sub(r'\b\d{7,}\s*$', '', limpa)
                    termos_lixo = ["ALÍQUOTA", "ATIVIDADE", "MUNICÍPIO", "CNAE", "OBRA", "ART"]
                    for termo in termos_lixo:
                        limpa = re.sub(termo, '', limpa, flags=re.IGNORECASE)
                    desc_final = re.sub(r'\s{2,}', ' ', limpa).strip().rstrip(',. ')
                    servico["descricao"] = f"{cod_6_digitos} - {desc_final}"
                break
    return servico