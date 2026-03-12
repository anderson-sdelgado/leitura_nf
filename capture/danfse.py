import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor
from lib.leitura_arquivo import ler_pymupedf

def leitura_danfse(arquivo: str):
    texto = ler_pymupedf(arquivo)
    linhas = texto.splitlines()

    nota = {}
    municipios = pegar_municipios(linhas)

    cidade, uf = separar_municipio_uf(municipios[0]) if municipios else (None, None)
    endereco = pegar_endereco(linhas)
    logradouro, bairro = separar_endereco_bairro(endereco)
    pis, cofins, irrf, cs = pegar_tributos_federais(linhas)
    valor_liq, valor_bruto, iss = pegar_valores_gerais(linhas)
    codigo_servico, desc_servico_completa = pegar_servico_tributacao(linhas)

    secao_prestador = pegar_secao(linhas, "PRESTADOR", "TOMADOR")
    secao_tomador = pegar_secao(linhas, "TOMADOR", "INTERMEDI")


    nota["DT_HR_INCL"] = None # Data e hora da inclusão da linha.
    nota["DT_HR_ALT"] = None # Data e hora da alteração da linha.
    nota["CDDOCUMENT"] = None # Código do documento no SE Suite. Idem V_NF_SERV.
    nota["NRO_CHAVE"] = None # Chave para registro da NFs-e. Gerada na integração.
    nota["CPF_CNPJ_EMIT"] = limpar_cnpj(pegar_valor(secao_tomador, "CNPJ / CPF / NIF")) # CNPJ/CPF da empresa (tomador) - somente números. Vide V_NF_SERV.TS_CNPJ_CPF.
    nota["COD_PART"] = limpar_cnpj(pegar_valor(secao_prestador, "CNPJ / CPF / NIF")) # CNPJ/CPF do fornecedor (prestador) - somente números. Vide V_NF_SERV.PS_CNPJ_CPF.
    nota["COD_MOD"] = "99" # Código do modelo de documento fiscal para registro. Fixo "99".
    nota["SERIE"] = "A" # Série do documento fiscal para registro. Fixo "A".
    nota["DTINSERT"] = None # Data da inclusão no SE Suite. Idem V_NF_SERV.
    nota["DTUPDATE"] = None # Data da alteração no SE Suite. Idem V_NF_SERV.
    nota["ID_DOC"] = pegar_valor(linhas, "Chave de Acesso da NFS-e") # ID do documento na view. Idem V_NF_SERV.
    nota["PREFEIT"] = pegar_prefeitura(linhas) # Nome da prefeitura. Idem V_NF_SERV.
    nota["SECRET_PREFEIT"] = pegar_secretaria(linhas) # Secretaria da prefeitura. Idem V_NF_SERV.
    nota["NRO_NF"] = pegar_valor(linhas, "Número da NFS-e") # Número da NF. Idem V_NF_SERV.
    nota["DT_EMISS"] = pegar_valor(linhas, "Data e Hora da emissão da NFS-e") # Data de emissão da NF. Idem V_NF_SERV.
    nota["PS_RAZ_SOC_NOME"] = pegar_valor(secao_prestador, "Nome / Nome Empresarial") # Nome do prestador de serviço. Idem V_NF_SERV.
    nota["PS_CNPJ_CPF"] = pegar_valor(secao_prestador, "CNPJ / CPF / NIF") # CNPJ do prestador de serviço. Idem V_NF_SERV.
    nota["PS_INSC_MUNIC"] = pegar_valor(secao_prestador, "Inscrição Municipal") # Inscrição municipal do prestador de serviço. Idem V_NF_SERV.
    nota["PS_INSC_EST"] = None # Inscrição estadual do prestador de serviço. Idem V_NF_SERV.
    nota["PS_MUNIC"] = cidade # Nome do município do prestador de serviço. Idem V_NF_SERV.
    nota["PS_UF"] = uf # Sigla da UF do prestador de serviço. Idem V_NF_SERV.
    nota["PS_ENDERECO"] = logradouro # Endereço do prestador de serviço. Idem V_NF_SERV.
    nota["PS_BAIRRO"] = bairro # Bairro do prestador de serviço. Idem V_NF_SERV.
    nota["PS_CEP"] = pegar_valor(secao_prestador, "CEP") # CEP do prestador de serviço. Idem V_NF_SERV.
    nota["PS_EMAIL"] = pegar_valor(secao_prestador, "E-mail") # E-mail do prestador de serviço. Idem V_NF_SERV.
    nota["TS_RAZ_SOC_NOME"] = pegar_valor(secao_tomador, "Nome / Nome Empresarial") # Nome do tomador de serviço - empresa usuária. Idem V_NF_SERV.
    nota["TS_CNPJ_CPF"] = pegar_valor(secao_tomador, "CNPJ / CPF / NIF") # CNPJ do tomador de serviço - empresa usuária. Idem V_NF_SERV.
    nota["DESC_SERV"] = pegar_descricao_servico(linhas) # Descrição do serviço. Idem V_NF_SERV.
    nota["VL_BRUTO"] = valor_bruto # Valor bruto. Idem V_NF_SERV.
    nota["VL_LIQ"] = valor_liq # Valor líquido. Idem V_NF_SERV.
    nota["VL_PIS"] = pis # Valor do PIS. Idem V_NF_SERV.
    nota["VL_COFINS"] = cofins # Valor da Cofins. Idem V_NF_SERV.
    nota["VL_IR"] = irrf # Valor do IR. Idem V_NF_SERV.
    nota["VL_INSS"] = None # Valor do INSS. Idem V_NF_SERV.
    nota["VL_CSLL"] = cs # Valor da CSLL. Idem V_NF_SERV.
    nota["VL_ISS"] = iss # Valor do ISS. Idem V_NF_SERV.
    nota["COD_SERVICO"] = codigo_servico # Código do serviço. Idem V_NF_SERV.
    nota["COD_SERVICO_ORIGINAL"] = desc_servico_completa # Código do serviço - informação original. Idem V_NF_SERV.

    # print("----------- NOTA DANF-----------")
    # for chave, valor in nota.items():
    #     print(f"{chave}: {valor}")
    # print("--------------------------")
    
    # print("----------- NOTA DANF-----------")
    # for numero, linha in enumerate(linhas, start=1): 
    #     print(f"{linha}")
    # print("-------------------------")


def pegar_secao(linhas, inicio, fim=None):
    capturando = False
    resultado = []
    inicio = inicio.upper()
    fim = fim.upper() if fim else None
    for linha in linhas:
        texto = linha.upper()
        if inicio in texto:
            capturando = True
            continue
        if capturando:
            if fim and fim in texto:
                break
            resultado.append(linha)
    return resultado


def pegar_valor(linhas, campo):
    campo = campo.upper()
    for i, linha in enumerate(linhas):
        texto = linha.strip().upper()
        if campo in texto:
            if i + 1 < len(linhas):
                valor = linhas[i + 1].strip()
                if valor:
                    return valor
    return None

def pegar_endereco(linhas):
    for i, linha in enumerate(linhas):
        if "ENDEREÇO" in linha.upper():
            endereco = []
            for j in range(i + 1, len(linhas)):
                texto = linhas[j].strip()
                if "MUNICÍPIO" in texto.upper():
                    break
                if texto:
                    endereco.append(texto)
            return " ".join(endereco)
    return None


def separar_endereco_bairro(endereco):
    if endereco and "," in endereco:
        partes = endereco.rsplit(",", 1)
        return partes[0].strip(), partes[1].strip()
    return endereco, None


def pegar_municipios(linhas):
    municipios = []
    for i, linha in enumerate(linhas):
        if "MUNICÍPIO" in linha.upper():
            if i + 1 < len(linhas):
                municipios.append(linhas[i + 1].strip())
    return municipios


def separar_municipio_uf(valor):
    if valor:
        match = re.match(r"(.+?)\s*-\s*([A-Z]{2})$", valor.strip())
        if match:
            return match.group(1), match.group(2)
    return valor, None


def pegar_prefeitura(linhas):
    for i, linha in enumerate(linhas[:20]):
        texto = linha.strip()
        texto_upper = texto.upper()
        if re.search(r"MUNIC[IÍ]PIO\s+DE", texto_upper):
            return texto
        if "PREFEITURA MUNICIPAL DE" in texto_upper:
            if i + 1 < len(linhas):
                cidade = linhas[i + 1].strip()
                return f"{texto} {cidade}"
    return None


def pegar_secretaria(linhas):
    for linha in linhas[:20]:
        if "SECRETARIA" in linha.upper():
            return linha.strip()
    return None


def pegar_descricao_servico(linhas):
    capturando = False
    descricao = []
    for linha in linhas:
        texto = linha.strip()
        if "DESCRIÇÃO DO SERVIÇO" in texto.upper():
            capturando = True
            continue
        if capturando:
            if "TRIBUTAÇÃO MUNICIPAL" in texto.upper():
                break
            if texto:
                descricao.append(texto)
    return " ".join(descricao) if descricao else None


def pegar_valores_gerais(linhas):
    dentro_secao = False
    valor_liq = None
    valor_bruto = None
    iss = None
    for i, linha in enumerate(linhas):
        texto = linha.strip().upper()
        if "VALOR TOTAL DA NFS-E" in texto:
            dentro_secao = True
            continue
        if dentro_secao:
            if "VALOR LÍQUIDO" in texto:
                valor_liq = extrair_valor(linhas[i + 1])
            if "VALOR DO SERVIÇO" in texto:
                valor_bruto = extrair_valor(linhas[i + 1])
            if "ISSQN RETIDO" in texto:
                iss = extrair_valor(linhas[i + 1])
            if "TOTAIS APROXIMADOS DOS TRIBUTOS" in texto:
                break
    return valor_liq, valor_bruto, iss


def pegar_tributos_federais(linhas):
    dentro_secao = False
    pis = None
    cofins = None
    irrf = None
    cs = None
    for i, linha in enumerate(linhas):
        texto = linha.strip().upper()
        if "TRIBUTAÇÃO FEDERAL" in texto:
            dentro_secao = True
            continue
        if dentro_secao:
            if "PIS" in texto:
                pis = extrair_valor(linhas[i + 1])
            if "COFINS" in texto:
                cofins = extrair_valor(linhas[i + 1])
            if "IRRF" in texto:
                irrf = extrair_valor(linhas[i + 1])
            if "CONTRIBUIÇÕES SOCIAIS" in texto:
                cs = extrair_valor(linhas[i + 1])
            if "VALOR TOTAL DA NFS-E" in texto:
                break
    return pis, cofins, irrf, cs


def pegar_servico_tributacao(linhas):
    capturando = False
    partes = []
    for linha in linhas:
        texto = linha.strip()
        if "CÓDIGO DE TRIBUTAÇÃO NACIONAL" in texto.upper():
            capturando = True
            continue
        if capturando:
            if "CÓDIGO DE TRIBUTAÇÃO MUNICIPAL" in texto.upper():
                break
            if texto:
                partes.append(texto)
    if not partes:
        return None, None
    texto_completo = " ".join(partes)
    match = re.search(r"\d{2}\.\d{2}", texto_completo)
    codigo_servico = match.group(0) if match else None
    return codigo_servico, texto_completo