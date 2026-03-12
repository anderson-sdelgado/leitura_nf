import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_municipio_pontal(texto: str):
    linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]

    prestador = pegar_dados_prestador(texto)
    tomador = pegar_dados_tomador(texto)
    pis, cofins, irrf, inss, csll = pegar_tributos_retidos(texto)

    nota = {}

    nota["DT_HR_INCL"] = None
    nota["DT_HR_ALT"] = None
    nota["CDDOCUMENT"] = None
    nota["NRO_CHAVE"] = None
    nota["CPF_CNPJ_EMIT"] = limpar_cnpj(tomador["cnpj"]) if tomador["cnpj"] else None
    nota["COD_PART"] = limpar_cnpj(prestador["cnpj"]) if prestador["cnpj"] else None
    nota["COD_MOD"] = "99"
    nota["SERIE"] = "A"
    nota["DTINSERT"] = None
    nota["DTUPDATE"] = None
    nota["PREFEIT"] = "Prefeitura Municipal de Pontal"
    nota["NRO_NF"] = pegar_numero_nf(texto)
    nota["DT_EMISS"] = pegar_data_emissao(texto)
    nota["PS_RAZ_SOC_NOME"] = prestador["razao_social"]
    nota["PS_CNPJ_CPF"] = prestador["cnpj"]
    nota["PS_INSC_MUNIC"] = prestador["insc_mun"]
    nota["PS_INSC_EST"] = prestador["insc_est"]
    nota["PS_MUNIC"] = prestador["municipio"]
    nota["PS_UF"] = prestador["uf"]
    nota["PS_ENDERECO"] = prestador["endereco"]
    nota["PS_BAIRRO"] = prestador["bairro"]
    nota["PS_CEP"] = prestador["cep"]
    nota["PS_EMAIL"] = prestador["email"]
    nota["TS_RAZ_SOC_NOME"] = tomador["razao_social"]
    nota["TS_CNPJ_CPF"] = tomador["cnpj"]
    nota["DESC_SERV"] = pegar_discriminacao_servico(texto)
    nota["VL_BRUTO"] = extrair_valor(pegar_valor_bruto(texto))
    nota["VL_LIQ"] = extrair_valor(pegar_valor_liquido(texto))
    nota["VL_PIS"] = pis
    nota["VL_COFINS"] = cofins
    nota["VL_IR"] = irrf
    nota["VL_INSS"] = inss
    nota["VL_CSLL"] = csll
    nota["COD_SERVICO"] = pegar_cod_servico(linhas) # Código do serviço. Idem V_NF_SERV.
    nota["COD_SERVICO_ORIGINAL"] = pegar_servico_original(linhas) # Código do serviço - informação original. Idem V_NF_SERV.

    print("----------- NOTA PONTAL -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    return nota
    print("-----------------------------------")

    # print("----------- NOTA PONTAL -----------")
    # for numero, linha in enumerate(linhas, start=1): 
    #     print(f"{linha}")
    # print("-------------------------")

def pegar_numero_nf(texto):
    match = re.search(r'Número da NFS-e\s+(\d+)', texto)
    return match.group(1) if match else None

def pegar_data_emissao(texto):
    match = re.search(r'(\d{2}/\d{2}/\d{4}\s+às\s+\d{2}:\d{2}:\d{2})', texto)
    return match.group(1) if match else None

def pegar_dados_prestador(texto):
    dados = {
        "razao_social": None, "cnpj": None, "insc_est": None,
        "insc_mun": None, "endereco": None, "bairro": None,
        "municipio": "PONTAL", "uf": "SP", "cep": None, "email": None
    }
    
    match_corpo = re.search(r'CPF/CNPJ\s+RG/Inscrição Estadual\s+Inscrição Municipal\s+Cadastro\s+Nome/Razão Social\s+([\d\./-]+)\s+([\d\.]+)\s+(\d+)\s+(\d+)\s+(.+)', texto)
    if match_corpo:
        dados["cnpj"] = match_corpo.group(1)
        dados["insc_est"] = match_corpo.group(2)
        dados["insc_mun"] = match_corpo.group(3)
        dados["razao_social"] = match_corpo.group(5).strip()

    match_end = re.search(r'Logradouro\s+Complemento\s+Bairro\s+(.+?)\s{2,}(.+)', texto)
    if match_end:
        dados["endereco"] = match_end.group(1).strip()
        dados["bairro"] = match_end.group(2).strip()

    match_contato = re.search(r'(\d{5}-\d{3})\s+PONTAL-SP\s+[\d-]+\s+([\w\.-]+@[\w\.-]+)', texto)
    if match_contato:
        dados["cep"] = match_contato.group(1)
        dados["email"] = match_contato.group(2)

    return dados

def pegar_dados_tomador(texto):
    dados = {"razao_social": None, "cnpj": None}
    
    match = re.search(r'ADQUIRENTE\s+CPF/CNPJ:\s*(\d+)\s+Nome/Razão Social:(.+)', texto)
    if match:
        dados["cnpj"] = match.group(1)
        dados["razao_social"] = match.group(2).strip()
    else:
        match_p1 = re.search(r'TOMADOR DE SERVIÇOS.*?([\d\./-]+)\s+(.+)', texto, re.DOTALL)
        if match_p1:
            dados["cnpj"] = match_p1.group(1)
            linhas = texto.splitlines()
            for i, linha in enumerate(linhas):
                if "TOMADOR DE SERVIÇOS" in linha:
                    dados["razao_social"] = linhas[i+2].strip()
                    break
    return dados

def pegar_discriminacao_servico(texto):
    match = re.search(r'Discriminação dos Serviços\s+(.*?)\s+Imposto Sobre Serviços', texto, re.DOTALL)
    if match:
        return match.group(1).replace('\n', ' ').strip()
    return None

def pegar_valor_bruto(texto):
    match = re.search(r'Valor Total dos Serviços.*?R\$\s*([\d\.,]+)', texto, re.S)
    return match.group(1) if match else None

def pegar_valor_liquido(texto):
    match = re.search(r'Valor Líquido da NFS-e:\s*R\$\s*([\d\.,]+)', texto)
    return match.group(1) if match else None

def pegar_tributos_retidos(texto):
    bloco = re.search(r'Retenções de Impostos\s+PIS.*?R\$\s*([\d\.,]+)\s+R\$\s*([\d\.,]+)\s+R\$\s*([\d\.,]+)\s+R\$\s*([\d\.,]+)\s+R\$\s*([\d\.,]+)', texto, re.S)
    
    if bloco:
        pis = extrair_valor(bloco.group(1))
        cofins = extrair_valor(bloco.group(2))
        inss = extrair_valor(bloco.group(3)) # CP
        irrf = extrair_valor(bloco.group(4))
        csll = extrair_valor(bloco.group(5))
        return (
            pis if pis > 0 else None,
            cofins if cofins > 0 else None,
            irrf if irrf > 0 else None,
            inss if inss > 0 else None,
            csll if csll > 0 else None
        )
    return None, None, None, None, None

def pegar_cod_servico(linhas):
    for linha in linhas:
        match = re.search(r':(\d{4})\d{2}', linha)
        if match:
            return match.group(1)
    return None

def pegar_servico_original(linhas):
    texto_completo = " ".join(linhas)
    match_codigo = re.search(r':(\d{6})', texto_completo)
    match_desc = re.search(r'Código ART\s+(.*?)\s+\d{1,2},\d{2}%', texto_completo, re.S)
    if match_codigo and match_desc:
        codigo = match_codigo.group(1)
        descricao = re.sub(r'\s+', ' ', match_desc.group(1)).strip()
        return f"{codigo} - {descricao}"
    elif match_codigo:
        return match_codigo.group(1)
    return None