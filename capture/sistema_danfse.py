import re
from lib.leitura_arquivo import ler_pymupedf
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_sistema_danfse(texto: str):
    
    # print("----------- NOTA DANFSE -----------")
    # print(texto)
    # print("-------------------------")

    prefeitura = pegar_dados_prefeitura(texto)
    prestador = pegar_dados_prestador(texto)
    tomador = pegar_dados_tomador(texto)
    financeiro = pegar_valores(texto)
    servico = pegar_dados_servico(texto)

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
    nota["ID_DOC"] = pegar_chave_acesso(texto) # ID do documento na view. Idem V_NF_SERV.
    nota["PREFEIT"] = prefeitura['prefeitura'] # Nome da prefeitura. Idem V_NF_SERV.
    nota["SECRET_PREFEIT"] = prefeitura['secretaria'] # Secretaria da prefeitura. Idem V_NF_SERV.
    nota["NRO_NF"] = pegar_numero_nota(texto) # Número da NF. Idem V_NF_SERV.
    nota["DT_EMISS"] = pegar_data_hora_emissao(texto) # Data de emissão da NF. Idem V_NF_SERV.
    nota["PS_RAZ_SOC_NOME"] = prestador['razao_social'] # Nome do prestador de serviço. Idem V_NF_SERV.
    nota["PS_CNPJ_CPF"] = prestador['cnpj'] # CNPJ do prestador de serviço. Idem V_NF_SERV.
    nota["PS_INSC_MUNIC"] = prestador['inscricao_municipal'] # Inscrição municipal do prestador de serviço. Idem V_NF_SERV.
    nota["PS_INSC_EST"] = None # Inscrição estadual do prestador de serviço. Idem V_NF_SERV.
    nota["PS_MUNIC"] = prestador['municipio'] # Nome do município do prestador de serviço. Idem V_NF_SERV.
    nota["PS_UF"] = prestador['uf'] # Sigla da UF do prestador de serviço. Idem V_NF_SERV.
    nota["PS_ENDERECO"] = prestador['endereco'] # Endereço do prestador de serviço. Idem V_NF_SERV.
    nota["PS_BAIRRO"] = prestador['bairro'] # Bairro do prestador de serviço. Idem V_NF_SERV.
    nota["PS_CEP"] = prestador['cep'] # CEP do prestador de serviço. Idem V_NF_SERV.
    nota["PS_EMAIL"] = prestador['email'] # E-mail do prestador de serviço. Idem V_NF_SERV.
    nota["TS_RAZ_SOC_NOME"] = tomador['razao_social'] # Nome do tomador de serviço - empresa usuária. Idem V_NF_SERV.
    nota["TS_CNPJ_CPF"] = tomador['cnpj'] # CNPJ do tomador de serviço - empresa usuária. Idem V_NF_SERV.
    nota["DESC_SERV"] = servico['discriminacao'] # Descrição do serviço. Idem V_NF_SERV.
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
    
    print("----------- NOTA DANFSE -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("-----------------------------------")

def pegar_dados_prefeitura(texto):
    dados = {
        "prefeitura": None, 
        "secretaria": None, 
    }
    resultado = re.search(r'^.*?Chave', texto, re.S)
    sujeira = [
        r'DANFSe?\s*v?\d+\.?\d*',         
        r'Documento\s*Auxiliar.*NFS-e',    
        r'Chave',                          
        r'S\s*N\s*e\s*o\s*r\s*t\s*v\s*a\s*iç.*nica', 
        r'fiscalizacao@[\w\.]+',           
        r'[\w\.-]+@[\w\.-]+',              # Qualquer outro e-mail
        r'\(\d{2}\)\s*\d{4,5}-\d{4}',      # Telefones (19)3403-1106
        r'tributos@[\w\.]+',               # E-mail de tributos
        r'NFSe',                           # Sigla avulsa
        r'\d{2}/\d{2}/\d{4}',              # Datas, se houver
    ]
    texto_limpo = resultado.group()
    for termo in sujeira:
        texto_limpo = re.sub(termo, '', texto_limpo, flags=re.I | re.S)
    texto_unificado = re.sub(r'\s+', '', texto_limpo)
    ancoras_principais = r'(PREFEITURA|MUNICÍPIO|MUNICIPIO|SECRETARIA|MUNICIPAL)'
    texto_final = re.sub(ancoras_principais, r' \1 ', texto_unificado, flags=re.I)
    texto_final = re.sub(r'(MUNICÍPIO|MUNICIPIO|PREFEITURA|MUNICIPAL|SECRETARIA)\s*(DE|DO|DA|DOS|DAS)', 
                         r'\1 \2 ', texto_final, flags=re.I)
    texto_final = re.sub(r'\s+', ' ', texto_final).strip().upper()
    padrao = r"^(.*?)\s*(SECRETARIA\s+.*)$"
    match = re.search(padrao, texto_final, re.I | re.S)
    if match:
        dados['prefeitura'] = match.group(1).strip()
        dados['secretaria'] = match.group(2).strip()
    else:
        dados['prefeitura'] = texto_final
    return dados


def pegar_chave_acesso(texto):
    texto_unificado = " ".join(texto.splitlines())
    padrao = (
        r'Chave\s*de\s*Acesso\s*da\s*NFS-e'
        r'\s*(.*?)\s*'
        r'N[uú]mero\s*da\s*NFS-e'
    )
    match = re.search(padrao, texto_unificado, re.I | re.S)
    if match:
        conteudo = match.group(1).strip()
        chave = re.sub(r'\D', '', conteudo)
        if len(chave) >= 30:
            return chave
        return conteudo
    return None

def pegar_numero_nota(texto):
    padrao = (
        r'Data\s*e\s*Hora\s*da\s*emiss[aâãáà]o\s*da\s*NFS-e'
        r'\s*(.*?)\s*'
        r'\d{2}/\d{2}/\d{4}'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if match:
        conteudo = match.group(1).strip()
        num = re.sub(r'\D', '', conteudo)
        return num
    return None

def pegar_data_hora_emissao(texto):
    padrao = (
        r'\d{2}/\d{2}/\d{4}'
        r'\s*(.*?)\s*'
        r'N[uú]mero\s*da\s*DPS'
    )
    match = re.search(padrao, texto, re.I)
    if match:
        conteudo = match.group(1).strip()
        texto_unificado = " ".join(conteudo.splitlines())
        padrao = r'(\d{2}/\d{2}/\d{4})\s*(\d{2}:\d{2}:\d{2})'
        match = re.search(padrao, texto_unificado)
        if match:
            data = match.group(1)
            hora = match.group(2)
            return f"{data} {hora}"
    return None

def pegar_dados_prestador(texto):
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
    padrao = (
        r'EMITENTE\s*DA\s*NFS-e'
        r'\s*(.*?)\s*'
        r'TOMADOR'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if match:
        bloco_completo = match.group(1).strip()
        padrao = (
            r'E-mail'
            r'\s*(.*?)\s*'
            r'Endere[cç]o'
        )
        match = re.search(padrao, bloco_completo, re.I | re.S)
        if match:
            conteudo = match.group(1).strip()
            padrao_email = r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}'
            match_email = re.search(padrao_email, conteudo)
            if match_email:
                dados["email"] = match_email.group().lower()
            conteudo = re.sub(padrao_email, '', conteudo)
            palavras = conteudo.split()
            conteudo = " ".join(palavras).strip().upper()
            dados["razao_social"] = conteudo
        padrao = (
            r'CEP\s*'
            r'\s*(.*?)\s*'
            r'Simples\s*'
        )
        match = re.search(padrao, bloco_completo, re.I | re.S)
        if match:
            conteudo = match.group(1).strip()
            match_cep = re.search(r'\d{5}-\d{3}', conteudo)
            if match_cep:
                dados["cep"] = match_cep.group()
                conteudo = re.sub(dados["cep"], '', conteudo)
            dados["uf"] = conteudo
            padrao = r"^([^,]+,[^,]+),\s*(.*?)\s+(?:(\d{7})\s*)?([^-]+?)\s*-\s*([A-Z]{2})$"
            match = re.search(padrao, conteudo.strip())
            dados["endereco"] = match.group(1).strip()
            dados["bairro"] = match.group(2).strip()
            dados["municipio"] = match.group(4).strip()
            dados["uf"] = match.group(5).strip()
        padrao_cnpj = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
        match_cnpj = re.search(padrao_cnpj, bloco_completo)
        if match_cnpj:
            dados["cnpj"] = match_cnpj.group()
        else:
            padrao_cpf = r'\d{3}\.\d{3}\.\d{3}-\d{2}'
            match_cpf = re.search(padrao_cpf, bloco_completo)
            if match_cpf:
                dados["cnpj"] = match_cpf.group()
        if dados["cnpj"]:
            cnpj_escapado = re.escape(dados["cnpj"])
            padrao = rf'{cnpj_escapado}\s*(.*?)\s*(?=[-(])'
            match = re.search(padrao, bloco_completo, re.I | re.S)
            if match and (im := match.group(1).strip()):
                dados["inscricao_municipal"] = im
    return dados

def pegar_dados_tomador(texto):
    dados = {"razao_social": None, "cnpj": None}
    padrao = (
        r'TOMADOR\s*'
        r'\s*(.*?)\s*'
        r'SERVI[CÇ]O\s*PRESTADO'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if match:
        bloco_completo = match.group(1).strip()
        padrao = (
            r'E-mail'
            r'\s*(.*?)\s*'
            r'Endere[cç]o'
        )
        match = re.search(padrao, bloco_completo, re.I | re.S)
        if match:
            conteudo = match.group(1).strip()
            padrao_email = r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}'
            conteudo = re.sub(padrao_email, '', conteudo)
            palavras = conteudo.split()
            conteudo = " ".join(palavras).strip().upper()
            conteudo = re.sub('-', '', conteudo).strip()
            dados["razao_social"] = conteudo
        padrao_cnpj = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
        match_cnpj = re.search(padrao_cnpj, bloco_completo)
        if match_cnpj:
            dados["cnpj"] = match_cnpj.group()
    return dados

def pegar_valores(texto):
    dados = {
        "bruto": None, "liquido": None, 
        "ir": None, "pis": None, "cofins": None, "csll": None,
        "inss": None, "iss": None
    }
    padrao = (
        r'TRIBUTA[CÇ][AÃÁÀÂ]O\s*MUNICIPAL\s*'
        r'\s*(.*?)\s*'
        r'TOTAIS\s*APROXIMADOS\s*DOS\s*TRIBUTOS'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if match:
        bloco_completo = match.group(1).strip()
        padrao = r"VALOR\s*TOTAL\s*DA\s*NFS-E([\s\S]+)"
        match = re.search(padrao, bloco_completo, re.I | re.S)
        if match:
            bloco_total = match.group(1)
            padrao = r"Valor\s*L[ií]quido\s*da\s*NFS-e([\s\S]+)"
            match = re.search(padrao, bloco_total, re.I | re.S)
            if match:
                valores = re.findall(r"R\$\s*([\d\.,]+)", match.group(1))
                if valores:
                    dados['liquido'] = valores[-1]
            padrao = (
                r'Valor\s*do\s*Servi[cç]o\s*'
                r'\s*(.*?)\s*'
                r"Total\s*das\s*Reten[cç][oõóòô]es\s*Federais"
            )
            match = re.search(padrao, bloco_total, re.I | re.S)
            if match:
                valores = re.findall(r"R\$\s*([\d\.,]+)", match.group(1))
                if valores:
                    dados['bruto'] = valores[0]
        padrao = (
            r'TRIBUTA[CÇ][AÃÁÀÂ]O\s*FEDERAL\s*'
            r'\s*(.*?)\s*'
            r'VALOR\s*TOTAL\s*DA\s*NFS-E'
        )
        match = re.search(padrao, bloco_completo, re.I | re.S)
        if match:
            bloco_federal = match.group(1)
            padrao = r"COFINS\s*-\s*D[eé]bito\s*Apura[cç][aâãáà]o\s*Pr[oõóòô]pria([\s\S]+)"
            match = re.search(padrao, bloco_federal, re.I | re.S)
            if match:
                padrao = r"R\$\s*[\d\.,]+|-"
                valores = re.findall(padrao, match.group(1))
                if len(valores) >= 2:
                    dados['pis'] = valores[0].replace("R$", "").strip() if valores[0] != "-" else None
                    dados['cofins'] = valores[1].replace("R$", "").strip() if valores[1] != "-" else None
            padrao = (
                r'\s*(.*?)\s*'
                r'PIS-D[eé]bito\s*'
            )
            match = re.search(padrao, bloco_federal, re.I | re.S)
            if match:
                texto = match.group(0)
                linhas = texto.split('\n')
                for i, texto_linha in enumerate(linhas):
                    if i == 1:
                        ir = texto_linha[0:20]
                        inss = texto_linha[20:40]
                        csll = texto_linha[40:60]
                        dados["ir"] = ir.replace("R$", "").strip() if ir != "-" else None
                        dados["inss"] = inss.replace("R$", "").strip() if inss != "-" else None
                        dados["csll"] = csll.replace("R$", "").strip() if csll != "-" else None
        padrao = (
            r'\s*(.*?)\s*'
            r'TRIBUTA[CÇ][AÃÁÀÂ]O\s*FEDERAL\s*'
        )
        match = re.search(padrao, bloco_completo, re.I | re.S)
        if match:
            padrao = r"R\$\s*[\d\.,]+|-"
            valores = re.findall(padrao, match.group(1))
            if valores:
                dados['iss'] = valores[-1]
    return dados

def pegar_dados_servico(texto):
    dados = {
        "codigo": None,
        "descricao": None,
        "discriminacao": None,
    }
    padrao = (
        r'Descri[cç][aâãáà]o\s*do\s*Servi[cç]o\s*'
        r'\s*(.*?)\s*'
        r'TRIBUTA[CÇ][AÃÁÀÂ]O\s*MUNICIPAL'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if match:
        dados['discriminacao'] = match.group(1).strip()
    padrao = (
        r'Pa[ií]s\s*da\s*Presta[cç][aâãáà]o*'
        r'\s*(.*?)\s*'
        r'Descri[cç][aâãáà]o\s*do\s*Servi[cç]o\s*'
    )
    match = re.search(padrao, texto, re.I | re.S)
    if match:
        padrao_limpeza = r"-?\s*[A-Za-zÀ-ÖØ-öø-ÿ\s\n\r]+-\s*[A-Z]{2}\s*-?"
        texto_limpo = re.sub(padrao_limpeza, "", match.group(1))
        texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
        match_cod = re.match(r'^(\d{2}\.\d{2})\s*-?\s*(.*)', texto_limpo)
        if match_cod:
            dados['codigo'] = match_cod.group(1)
        dados['descricao'] = texto_limpo
    return dados
