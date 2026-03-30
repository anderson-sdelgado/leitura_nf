
import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_issweb(texto: str):

    # print("----------- NOTA ISSWEB -----------")
    # print(texto)
    # print("-------------------------")

    prestador = pegar_dados_prestador(texto)
    tomador = pegar_dados_tomador(texto)
    financeiro = pegar_valores(texto)
    servico = pegar_dados_servico(texto)

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
    nota["ID_DOC"] = pegar_codigo_verificacao(texto) # ID do documento na view. Idem V_NF_SERV. ok
    nota["PREFEIT"] = pegar_prefeitura(texto) # Nome da prefeitura. Idem V_NF_SERV.
    nota["SECRET_PREFEIT"] = None # Secretaria da prefeitura. Idem V_NF_SERV. ok
    nota["NRO_NF"] = pegar_numero_nf(texto) # Número da NF. Idem V_NF_SERV. ok
    nota["DT_EMISS"] = pegar_data_hora_emissao(texto) # Data de emissão da NF. Idem V_NF_SERV. ok
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
    nota["DESC_SERV"] = pegar_discriminacao_servico(texto) # Descrição do serviço. Idem V_NF_SERV. ok
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

def pegar_prefeitura(texto):
    padrao = (
        r'P[aâãáà]gina\s*\d+\s*de\s*\d+'
        r'\s*(.*?)\s*'                 
        r'N[uú]mero\s*'                        
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    return match.group(1).strip()

def pegar_codigo_verificacao(texto):
    padrao = (
        r'C[oóòõô]digo\s*de\s*Verifica[cç][aâãáà]o\s*de\s*Autenticidade'
        r'\s*(.*?)\s*'                 
        r'NOTA\s*'                        
    )
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    return match.group(1).strip()

def pegar_numero_nf(texto):
    padrao = r'N[uú]mero\s*da\s*NFS-e\s*(\d+)'
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    return match.group(1).strip()


def pegar_data_hora_emissao(texto):
    padrao = r'Data\s*e\s*Hora\s*de\s*Emiss[aâãáà]o\s*da\s*NFS-e\s*(\d{2}/\d{2}/\d{4}).*?(\d{2}:\d{2}:\d{2})'
    match = re.search(padrao, texto, re.I | re.S)
    if not match: return None
    data = match.group(1)
    hora = match.group(2)
    return f'{data} {hora}'

def pegar_dados_prestador(texto):
    dados = {
        "cnpj": None, "inscricao_estadual": None, "inscricao_municipal": None, 
        "razao_social": None, "endereco": None, "bairro": None, 
        "municipio": None, "uf": None, "cep": None, "email": None
    }
    padrao = (
        r'PRESTADOR\s*DE\s*SERVI[CÇ]OS'
        r'\s*(.*?)\s*'
        r'TOMADOR\s*'
    )
    match = re.search(padrao, texto, re.IGNORECASE | re.S)
    if not match: return dados
    bloco_completo = match.group(1).strip()

    padrao = r'(?:\d[\d.\-/]*\s+){2,}(.+?)\s+(?=Logradouro)'
    match = re.search(padrao, bloco_completo, re.IGNORECASE | re.S)
    if match: dados["razao_social"] = match.group(1).strip()

    padrao = r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})[\s\n]+([^\s\n]+)[\s\n]+([^\s\n]+)'
    match = re.search(padrao, bloco_completo)
    if match:
        dados["cnpj"] = match.group(1) 
        dados["inscricao_estadual"] = match.group(2)
        dados["inscricao_municipal"] = match.group(3)

    padrao = (
        r'Logradouro\s+Complemento\s+Bairro\s+'
        r'(?P<logradouro>.+?)\s{3,}'
        r'(?P<complemento>.*?)\s*'
        r'(?P<bairro>[A-Z0-9\s.\-]+?)'
        r'\s+(?=CEP|Cidade)'
    )
    match = re.search(padrao, bloco_completo, re.IGNORECASE | re.S)
    if match:
        rua = match.group('logradouro').strip()
        comp = match.group('complemento').strip()
        dados['endereco'] = f"{rua}, {comp}" if comp else rua
        bairro = match.group('bairro').strip()
        dados['bairro'] = bairro

    padrao = (
        r'E-mail\s+'
        r'(?P<cep>\d{5}-\d{3})\s+'
        r'(?P<municipio>[^-\n]+)-(?P<uf>[A-Z]{2})'
        r'.*?\s{1,}'
        r'(?P<email>[^\s\n]+@[^\s\n]+\.[^\s\n]+)'
    )
    match = re.search(padrao, bloco_completo, re.IGNORECASE | re.S)
    if match:
        dados['cep'] = match.group('cep').strip()
        dados['municipio'] = match.group('municipio').strip()
        dados['uf'] = match.group('uf').strip()
        dados['email'] = match.group('email').strip()
    return dados

def pegar_dados_tomador(texto):
    dados = {
        "cnpj": None, 
        "razao_social": None
    }
    padrao = (
        r'TOMADOR\s*DE\s*SERVI[CÇ]OS'
        r'\s*(.*?)\s*'
        r'Discrimina[cç][aâãáà]o\s*'
    )
    match = re.search(padrao, texto, re.IGNORECASE | re.S)
    if not match: return dados
    bloco_completo = match.group(1).strip()

    padrao = r'(?P<cnpj>\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})(?:[\s\d./-]+)*\s+(?P<razao_social>.+?)(?=\s{2,}|\.|$)'
    match = re.search(padrao, bloco_completo)
    if match:
        dados["cnpj"] = match.group('cnpj')
        razao = match.group('razao_social').strip()
        dados["razao_social"] = razao.rstrip('.')
    return dados

def pegar_discriminacao_servico(texto):
    padrao = (
        r'Discrimina[cç][aâãáà]o\s*dos\s*Servi[cç]os'
        r'\s*(.*?)\s*'
        r'Imposto\s*'
    )
    match = re.search(padrao, texto, re.S | re.I)
    if not match: return None
    bloco_completo = match.group(1).strip()
    if  not bloco_completo.strip().startswith("Qtde. Un."): return bloco_completo
    discriminacao_formatada = []
    temp_item = None 
    linhas = bloco_completo.splitlines()
    for linha in linhas:
        linha_up = linha.upper().strip()
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

def pegar_valores(texto):
    dados = {
        "bruto": None, "liquido": None, "ir": None, 
        "pis": None, "cofins": None, "csll": None, 
        "inss": None, "iss": None
    }
    
    padrao = r'Valor\s*L[ií]quido\s*da\s*NFS-e:\s*R\$\s*([\d.]+,\d{2})'
    match = re.search(padrao, texto, re.I | re.S)
    if match: dados["liquido"] = match.group(1)

    padrao = (
        r'Desconto\s*Condicionado'
        r'\s*(.*?)\s*'
        r"Reten[cç][oóòõô]es\s*de\s*Impostos"
    )
    match = re.search(padrao, texto, re.IGNORECASE | re.S)
    if match:
        valores = re.findall(r"R\$\s*([\d\.,]+)", match.group(1))
        if valores:
            dados['bruto'] = valores[0]
            dados['iss'] = valores[4]

    padrao = (
        r'Outras\s*Reten[cç][oóòõô]es'
        r'\s*(.*?)\s*'
        r'Valor\s*'
    )
    match = re.search(padrao, texto, re.IGNORECASE | re.S)
    if match:
        valores = re.findall(r"R\$\s*([\d\.,]+)", match.group(1))
        if valores:
            dados['pis'] = valores[0]
            dados['cofins'] = valores[1]
            dados['inss'] = valores[2]
            dados['ir'] = valores[3]
            dados["csll"] = valores[4]
    return dados

def pegar_dados_servico(texto):
    dados = {"codigo": None, "descricao": None}
    padrao = (
        r'LC\s*116/2003:'
        r'\s*(.*?)\s*'
        r'Valor\s*Total\s*'
    )
    match = re.search(padrao, texto, re.IGNORECASE | re.S)
    if not match: return dados
    bloco_completo = match.group(1).strip()
    padrao = (
        r'\s*(.*?)\s*'
        r'Al[ií]quota\s*'
    )
    match = re.search(padrao, bloco_completo, re.IGNORECASE | re.S)
    if match: 
        codigo = match.group(1).strip()
        limpo = "".join(filter(str.isdigit, str(codigo)))
        if len(limpo) >= 4: dados['codigo'] = f"{limpo[:2]}.{limpo[2:4]}"

    padrao = r'(?<=ART)\s+(?P<descricao>.+?)\s+(?=\d+,\d{2}%)'
    match = re.search(padrao, texto, re.S)
    if match: descricao = match.group('descricao').strip()

    dados["descricao"] = f"{codigo} - {descricao}"
    return dados