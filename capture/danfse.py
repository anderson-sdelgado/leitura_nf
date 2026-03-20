import re
from lib.leitura_arquivo import ler_pymupedf
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_danfse(texto_plumber: str, arquivo=None):

    texto_pymupedf = ler_pymupedf(arquivo)
    """
    Função principal que coordena a extração usando o melhor de cada biblioteca.
    """
    # Transformamos o texto em linhas para funções que processam linha a linha
    linhas_plumber = texto_plumber.splitlines()
    linhas_py = texto_pymupedf.splitlines()
    texto_py_full = "\n".join(linhas_py)

    # Inicialização dos dicionários de dados
    prestador = pegar_dados_prestador_danfse(texto_pymupedf)
    tomador = pegar_dados_tomador_danfse(texto_pymupedf)
    financeiro = pegar_valores_danfse(linhas_plumber, linhas_py)
    servico = pegar_dados_servico_danfse(linhas_py)

    nota = {}
    
    # 1. Metadados e Controle
    nota["DT_HR_INCL"] = None
    nota["DT_HR_ALT"] = None
    nota["CDDOCUMENT"] = None
    nota["NRO_CHAVE"] = pegar_chave_acesso(texto_py_full)
    nota["CPF_CNPJ_EMIT"] = limpar_cnpj(tomador['cnpj'])
    nota["COD_PART"] = limpar_cnpj(prestador['cnpj'])
    nota["COD_MOD"] = "99"
    nota["SERIE"] = "A"
    nota["DTINSERT"] = None
    nota["DTUPDATE"] = None
    
    # 2. Informações da Nota
    nota["ID_DOC"] = nota["NRO_CHAVE"]
    nota["PREFEIT"] = pegar_prefeitura_danfse(linhas_py)
    nota["SECRET_PREFEIT"] = None 
    nota["NRO_NF"] = pegar_numero_nf_danfse(texto_py_full)
    nota["DT_EMISS"] = pegar_data_emissao_danfse(texto_py_full)
    
    # 3. Dados do Prestador (PS)
    nota["PS_RAZ_SOC_NOME"] = prestador['razao_social']
    nota["PS_CNPJ_CPF"] = prestador['cnpj']
    nota["PS_INSC_MUNIC"] = prestador['inscricao_municipal']
    nota["PS_INSC_EST"] = None
    nota["PS_MUNIC"] = prestador['municipio']
    nota["PS_UF"] = prestador['uf']
    nota["PS_ENDERECO"] = prestador['endereco']
    nota["PS_BAIRRO"] = prestador['bairro']
    nota["PS_CEP"] = prestador['cep']
    nota["PS_EMAIL"] = prestador['email']
    
    # 4. Dados do Tomador (TS)
    nota["TS_RAZ_SOC_NOME"] = tomador['razao_social']
    nota["TS_CNPJ_CPF"] = tomador['cnpj']
    
    # 5. Descrição e Valores (Financeiro)
    nota["DESC_SERV"] = pegar_descricao_danfse(linhas_py)
    nota["VL_BRUTO"] = extrair_valor(financeiro["bruto"])
    nota["VL_LIQ"] = extrair_valor(financeiro["liquido"])
    nota["VL_PIS"] = extrair_valor(financeiro["pis"])
    nota["VL_COFINS"] = extrair_valor(financeiro["cofins"])
    nota["VL_IR"] = extrair_valor(financeiro["ir"])
    nota["VL_INSS"] = extrair_valor(financeiro["inss"])
    nota["VL_CSLL"] = extrair_valor(financeiro["csll"])
    nota["VL_ISS"] = extrair_valor(financeiro["iss"])
    
    # 6. Códigos de Serviço
    nota["COD_SERVICO"] = servico["codigo"]
    nota["COD_SERVICO_ORIGINAL"] = servico["descricao"]


    print("----------- NOTA GINFES -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("--------------------------------------")

# --- FUNÇÕES DE APOIO ESPECÍFICAS PARA O PADRÃO DANFSe ---

def pegar_prefeitura_danfse(linhas):
    for i, linha in enumerate(linhas[:20]):
        if "MUNICÍPIO DE" in linha.upper() or "PREFEITURA" in linha.upper():
            return linha.strip()
    return None

def pegar_numero_nf_danfse(texto):
    match = re.search(r"Número da NFS-e\s*\n?(\d+)", texto)
    return match.group(1) if match else None

def pegar_chave_acesso(texto):
    # Remove espaços para garantir a captura da chave de 50 dígitos
    texto_limpo = texto.replace(" ", "").replace("\n", "")
    match = re.search(r"(\d{50})", texto_limpo)
    return match.group(1) if match else None

def pegar_data_emissao_danfse(texto):
    match = re.search(r"Data e Hora da emissão da NFS-e\s*\n?(\d{2}/\d{2}/\d{4})", texto)
    return match.group(1) if match else None

def pegar_dados_prestador_danfse(texto):
    dados = {"razao_social": None, "cnpj": None, "inscricao_municipal": None, "municipio": None, "uf": None, "endereco": None, "bairro": None, "cep": None, "email": None}
    
    # Delimita o bloco do prestador
    bloco = re.split(r"TOMADOR DO SERVIÇO", texto, flags=re.I)[0]
    
    cnpj = re.search(r"(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})", bloco)
    if cnpj: dados["cnpj"] = cnpj.group(1)
    
    razao = re.search(r"Nome / Nome Empresarial\s*\n?(.*)", bloco, re.I)
    if razao: dados["razao_social"] = razao.group(1).split('\n')[0].strip().upper()
    
    # Endereço e Localidade
    mun_uf = re.search(r"([A-ZÀ-Ÿ\s]{3,})\s*-\s*([A-Z]{2})", bloco)
    if mun_uf:
        dados["municipio"] = mun_uf.group(1).split('\n')[-1].strip()
        dados["uf"] = mun_uf.group(2).strip()
        
    cep = re.search(r"(\d{5}-\d{3})", bloco)
    if cep: dados["cep"] = cep.group(1)

    return dados

def pegar_dados_tomador_danfse(texto):
    dados = {"razao_social": None, "cnpj": None}
    partes = re.split(r"TOMADOR DO SERVIÇO", texto, flags=re.I)
    if len(partes) > 1:
        bloco = partes[1].split("INTERMEDIÁRIO")[0]
        cnpj = re.search(r"(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})", bloco)
        if cnpj: dados["cnpj"] = cnpj.group(1)
        razao = re.search(r"Nome / Nome Empresarial\s*\n?(.*)", bloco, re.I)
        if razao: dados["razao_social"] = razao.group(1).split('\n')[0].strip().upper()
    return dados

def pegar_valores_danfse(linhas_plumber, linhas_py):
    financeiro = {"bruto": "0,00", "liquido": "0,00", "pis": "0,00", "cofins": "0,00", "ir": "0,00", "inss": "0,00", "csll": "0,00", "iss": "0,00"}
    
    mapeamento = {
        "VALOR DO SERVIÇO": "bruto",
        "VALOR LÍQUIDO DA NFS-E": "liquido",
        "IRRF": "ir",
        "PIS - DÉBITO": "pis",
        "COFINS - DÉBITO": "cofins",
        "CONTRIBUIÇÃO PREVIDENCIÁRIA": "inss",
        "CONTRIBUIÇÕES SOCIAIS": "csll",
        "ISSQN RETIDO": "iss"
    }

    for i, linha in enumerate(linhas_plumber):
        for termo, chave in mapeamento.items():
            if termo in linha.upper():
                # No padrão DANFSe, o valor costuma estar 1 ou 2 linhas abaixo do rótulo no PDFPlumber
                for offset in range(1, 3):
                    if i + offset < len(linhas_py):
                        valor = linhas_py[i+offset].strip()
                        if "R$" in valor or (valor and valor[0].isdigit()):
                            financeiro[chave] = valor
                            break
    return financeiro

def pegar_descricao_danfse(linhas):
    desc = []
    ativo = False
    for l in linhas:
        if "DESCRIÇÃO DO SERVIÇO" in l.upper():
            ativo = True
            continue
        if ativo:
            if "TRIBUTAÇÃO MUNICIPAL" in l.upper() or "VALOR DO SERVIÇO" in l.upper():
                break
            if l.strip(): desc.append(l.strip())
    return " ".join(desc)

def pegar_dados_servico_danfse(linhas):
    res = {"codigo": None, "descricao": None}
    for l in linhas:
        if "Código de Tributação Nacional" in l:
            m = re.search(r"(\d{2}\.\d{2}(\.\d{2})?)", l)
            if m:
                res["codigo"] = m.group(1)
                res["descricao"] = l.strip()
                break
    return res



# import re
# # from lib.limpar_cnpj import limpar_cnpj
# # from lib.converter_moeda import extrair_valor
# # from lib.leitura_arquivo import ler_pymupedf

# def leitura_danfse(texto: str, arquivo):
#     linhas = texto.splitlines()

#     # print("----------- NOTA DANFSE pdfplumber -----------")
#     # for numero, linha in enumerate(linhas, start=1): 
#     #     print(f"{linha}")
#     # print("-------------------------")


#     # texto = ler_pymupedf(arquivo)
#     # linhas = texto.splitlines()
#     # print("----------- NOTA DANFSE pymupedf -----------")
#     # for numero, linha in enumerate(linhas, start=1): 
#     #     print(f"{linha}")
#     # print("-------------------------")


#     nota = {}

#     prestador = pegar_dados_prestador(texto)
#     tomador = pegar_dados_tomador(linhas)
#     financeiro = pegar_valores(linhas)
#     servico = pegar_dados_servico(linhas)

#     nota["DT_HR_INCL"] = None # Data e hora da inclusão da linha.
#     nota["DT_HR_ALT"] = None # Data e hora da alteração da linha.
#     nota["CDDOCUMENT"] = None # Código do documento no SE Suite. Idem V_NF_SERV.
#     nota["NRO_CHAVE"] = None # Chave para registro da NFs-e. Gerada na integração.
#     nota["CPF_CNPJ_EMIT"] = limpar_cnpj(tomador['cnpj']) # CNPJ/CPF da empresa (tomador) - somente números. Vide V_NF_SERV.TS_CNPJ_CPF. ok
#     nota["COD_PART"] = limpar_cnpj(prestador['cnpj']) # CNPJ/CPF do fornecedor (prestador) - somente números. Vide V_NF_SERV.PS_CNPJ_CPF. ok
#     nota["COD_MOD"] = "99" # Código do modelo de documento fiscal para registro. Fixo "99".
#     nota["SERIE"] = "A" # Série do documento fiscal para registro. Fixo "A".
#     nota["DTINSERT"] = None # Data da inclusão no SE Suite. Idem V_NF_SERV.
#     nota["DTUPDATE"] = None # Data da alteração no SE Suite. Idem V_NF_SERV.
#     nota["ID_DOC"] = pegar_codigo_verificacao(linhas) # ID do documento na view. Idem V_NF_SERV. ok
#     nota["PREFEIT"] = pegar_prefeitura(linhas) # Nome da prefeitura. Idem V_NF_SERV.
#     nota["SECRET_PREFEIT"] = pegar_secretaria(linhas) # Secretaria da prefeitura. Idem V_NF_SERV.
#     nota["NRO_NF"] = pegar_numero_nf(linhas) # Número da NF. Idem V_NF_SERV. ok
#     nota["DT_EMISS"] = pegar_data_hora_emissao(linhas) # Data de emissão da NF. Idem V_NF_SERV. ok
#     nota["PS_RAZ_SOC_NOME"] = prestador['razao_social'] # Nome do prestador de serviço. Idem V_NF_SERV. ok
#     nota["PS_CNPJ_CPF"] = prestador['cnpj'] # CNPJ do prestador de serviço. Idem V_NF_SERV. ok
#     nota["PS_INSC_MUNIC"] = prestador['inscricao_municipal'] # Inscrição municipal do prestador de serviço. Idem V_NF_SERV. ok
#     nota["PS_INSC_EST"] = None # Inscrição estadual do prestador de serviço. Idem V_NF_SERV. ok
#     nota["PS_MUNIC"] = prestador['municipio'] # Nome do município do prestador de serviço. Idem V_NF_SERV. ok
#     nota["PS_UF"] = prestador['uf'] # Sigla da UF do prestador de serviço. Idem V_NF_SERV. ok
#     nota["PS_ENDERECO"] = prestador['endereco'] # Endereço do prestador de serviço. Idem V_NF_SERV. ok
#     nota["PS_BAIRRO"] = prestador['bairro'] # Bairro do prestador de serviço. Idem V_NF_SERV. ok
#     nota["PS_CEP"] = prestador['cep'] # CEP do prestador de serviço. Idem V_NF_SERV. ok
#     nota["PS_EMAIL"] = prestador['email'] # E-mail do prestador de serviço. Idem V_NF_SERV. ok
#     nota["TS_RAZ_SOC_NOME"] = tomador['razao_social'] # Nome do tomador de serviço - empresa usuária. Idem V_NF_SERV. ok
#     nota["TS_CNPJ_CPF"] = tomador['cnpj'] # CNPJ do tomador de serviço - empresa usuária. Idem V_NF_SERV. ok ok
#     nota["DESC_SERV"] = pegar_descricao_servico(linhas) # Descrição do serviço. Idem V_NF_SERV.
#     nota["VL_BRUTO"] = extrair_valor(financeiro["bruto"]) # Valor bruto. Idem V_NF_SERV. 
#     nota["VL_LIQ"] = extrair_valor(financeiro["liquido"])# Valor líquido. Idem V_NF_SERV.
#     nota["VL_PIS"] = extrair_valor(financeiro["pis"]) # Valor do PIS. Idem V_NF_SERV.
#     nota["VL_COFINS"] = extrair_valor(financeiro["cofins"]) # Valor da Cofins. Idem V_NF_SERV.
#     nota["VL_IR"] = extrair_valor(financeiro["ir"]) # Valor do IR. Idem V_NF_SERV.
#     nota["VL_INSS"] = extrair_valor(financeiro["inss"]) # Valor do INSS. Idem V_NF_SERV.
#     nota["VL_CSLL"] = extrair_valor(financeiro["csll"]) # Valor da CSLL. Idem V_NF_SERV.
#     nota["VL_ISS"] = extrair_valor(financeiro["iss"]) # Valor do ISS. Idem V_NF_SERV.
#     nota["COD_SERVICO"] = servico["codigo"] # Código do serviço. Idem V_NF_SERV.
#     nota["COD_SERVICO_ORIGINAL"] = servico["descricao"] # Código do serviço - informação original. Idem V_NF_SERV.

#     # print("----------- NOTA DANF-----------")
#     # for chave, valor in nota.items():
#     #     print(f"{chave}: {valor}")
#     # print("--------------------------")
    

# def pegar_codigo_verificacao(linhas):
#     texto_completo = " ".join(linhas)
#     match_chave = re.search(r'Chave de Acesso da NFS-e\s+(\d{50})', texto_completo)
#     if match_chave:
#         return match_chave.group(1)
#     try:
#         for i, linha in enumerate(linhas):
#             if "Chave de Acesso da NFS-e" in linha:
#                 candidato = "".join(linhas[i+1:i+3]).replace(" ", "").strip()
#                 match_num = re.search(r'(\d{50})', candidato)
#                 if match_num:
#                     return match_num.group(1)
#     except Exception:
#         pass
#     match_avulso = re.search(r'(\d{50})', texto_completo)
#     if match_avulso:
#         return match_avulso.group(1)
#     return None

# def pegar_prefeitura(linhas):
#     for i, linha in enumerate(linhas[:20]):
#         texto = linha.strip()
#         texto_upper = texto.upper()
#         if re.search(r"MUNIC[IÍ]PIO\s+DE", texto_upper):
#             return texto
#         if "PREFEITURA MUNICIPAL DE" in texto_upper:
#             if i + 1 < len(linhas):
#                 cidade = linhas[i + 1].strip()
#                 return f"{texto} {cidade}"
#     return None

# def pegar_secretaria(linhas):
#     for linha in linhas[:20]:
#         if "SECRETARIA" in linha.upper():
#             return linha.strip()
#     return None

# def pegar_numero_nf(linhas):
#     for i, linha in enumerate(linhas):
#         if "Número da NFS-e" in linha:
#             if i + 1 < len(linhas):
#                 numero = linhas[i+1].strip()
#                 if numero.isdigit():
#                     return numero
#     texto_completo = " ".join(linhas)
#     match = re.search(r'Número da NFS-e\s+(\d+)', texto_completo)
#     if match:
#         return match.group(1)
#     return None

# def pegar_data_hora_emissao(linhas):
#     for i, linha in enumerate(linhas):
#         if "Data e Hora da emissão da NFS-e" in linha:
#             if i + 1 < len(linhas):
#                 valor = linhas[i+1].strip()
#                 match = re.search(r'(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})', valor)
#                 if match:
#                     return match.group(1)
#     texto_completo = " ".join(linhas)
#     match_horizontal = re.search(r'Data e Hora da emissão da NFS-e\s+(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})', texto_completo)
#     if match_horizontal:
#         return match_horizontal.group(1)
#     match_generico = re.search(r'(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})', texto_completo)
#     if match_generico:
#         return match_generico.group(1)
#     return None

# def pegar_dados_prestador(texto_completo):
#     dados = {
#         "razao_social": None, "cnpj": None, "inscricao_municipal": None, 
#         "municipio": None, "uf": None, "cep": None,
#         "endereco": None, "bairro": None, "email": None
#     }

#     # 1. Delimita o Bloco (Pega tudo antes do Tomador)
#     try:
#         # Usamos split com ignore case para garantir que pegue o bloco certo
#         partes = re.split(r"TOMADOR DO SERVIÇO|TOMADOR DO SERVICO", texto_completo, flags=re.I)
#         bloco = partes[0]
#     except:
#         bloco = texto_completo

#     # 2. CNPJ (Procura o formato em todo o bloco do prestador)
#     match_cnpj = re.search(r"(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})", bloco)
#     if match_cnpj:
#         dados["cnpj"] = match_cnpj.group(1)

#     # 3. INSCRIÇÃO MUNICIPAL (Ajustado para pegar números ou o traço '-')
#     # O padrão [0-9.\-/]+ agora aceita o "-" sozinho ou números
#     im_match = re.search(r"(?:Inscrição Municipal|Inscricao Municipal)\s*\n?\s*([0-9.\-/]+|(?<=\s)-(?=\s|$))", bloco, re.I)
#     if im_match:
#         dados["inscricao_municipal"] = im_match.group(1).strip()

#     # 4. RAZÃO SOCIAL
#     razao = re.search(r"(?:Nome / Nome Empresarial|Nome Empresarial)\s*\n?(.*?)(?=E-mail|Inscrição|CNPJ|Endereço|Telefone|Simples|$)", bloco, re.S | re.I)
#     if razao:
#         nome_bruto = razao.group(1).strip()
#         # Remove lixos de colunas e dados de emissão que grudam no nome na nota de Piracicaba
#         nome_limpo = re.split(r'Endereço|Endereco|TOMADOR|CNPJ|E-mail|Data e Hora|Inscrição|Municipio', nome_bruto, flags=re.I)[0].strip()
#         dados["razao_social"] = " ".join(nome_limpo.split())

#     # 5. MUNICÍPIO E UF (Busca o padrão "Cidade - UF")
#     match_mun_uf = re.search(r"([A-Za-zÀ-ÿ\s]+)\s*\n?\s*-\s*([A-Z]{2})", bloco)
#     if match_mun_uf:
#         # Pega a última linha (evita nomes de prefeituras no topo)
#         cidade_bruta = match_mun_uf.group(1).strip().split('\n')[-1].strip()
#         dados["municipio"] = cidade_bruta
#         dados["uf"] = match_mun_uf.group(2).strip()

#     # 6. ENDEREÇO E BAIRRO
#     end = re.search(r"Endereço\s*\n?(.*?)(?=Município|Municipio|CEP|E-mail|Simples|TOMADOR|$)", bloco, re.S | re.I)
#     if end:
#         end_limpo = " ".join(end.group(1).split())
#         end_limpo = re.split(r'Município|Municipio|CEP|E-mail|Data e Hora', end_limpo, flags=re.I)[0].strip()
#         if "," in end_limpo:
#             partes = end_limpo.rsplit(",", 1)
#             dados["endereco"], dados["bairro"] = partes[0].strip(), partes[1].strip()
#         else:
#             dados["endereco"] = end_limpo

#     # 7. CEP E E-MAIL
#     match_cep = re.search(r"(\d{5}-\d{3})", bloco)
#     if match_cep: dados["cep"] = match_cep.group(1)
    
#     match_email = re.search(r"([\w\.-]+@[\w\.-]+\.\w+)", bloco)
#     if match_email: dados["email"] = match_email.group(1).lower()

#     return dados

# def pegar_dados_tomador(linhas):
#     dados = {"razao_social": None, "cnpj": None}
#     texto = "\n".join(linhas)
#     try:
#         bloco = texto.split("TOMADOR DO SERVIÇO")[1].split("INTERMEDIÁRIO DO SERVIÇO")[0]
#         linhas_bloco = [l.strip() for l in bloco.splitlines() if l.strip()]
#         for i, l in enumerate(linhas_bloco):
#             if "CNPJ / CPF / NIF" in l:
#                 dados["cnpj"] = linhas_bloco[i+1]
#             if "Nome / Nome Empresarial" in l:
#                 nome_partes = []
#                 for j in range(i + 1, len(linhas_bloco)):
#                     if "E-MAIL" in linhas_bloco[j].upper():
#                         break
#                     nome_partes.append(linhas_bloco[j])
#                 dados["razao_social"] = " ".join(nome_partes)
#     except Exception:
#         pass
#     return dados

# def pegar_descricao_servico(linhas):
#     capturando = False
#     descricao = []
#     for linha in linhas:
#         texto = linha.strip()
#         if "DESCRIÇÃO DO SERVIÇO" in texto.upper():
#             capturando = True
#             continue
#         if capturando:
#             if "TRIBUTAÇÃO MUNICIPAL" in texto.upper():
#                 break
#             if texto:
#                 descricao.append(texto)
#     return " ".join(descricao) if descricao else None

# def pegar_valores(linhas):
#     vals = {
#         "bruto": None, "liquido": None, "ir": None, 
#         "pis": None, "cofins": None, "csll": None, 
#         "inss": None, "iss": None
#     }
    
#     for i, linha in enumerate(linhas):
#         texto = linha.strip().upper()
#         if i + 1 < len(linhas):
#             proxima_linha = linhas[i + 1].strip()
#             if "VALOR DO SERVIÇO" in texto:
#                 vals["bruto"] = extrair_valor(proxima_linha)
#             elif "VALOR LÍQUIDO DA NFS-E" in texto:
#                 vals["liquido"] = extrair_valor(proxima_linha)
#             elif "ISSQN RETIDO" in texto:
#                 vals["iss"] = extrair_valor(proxima_linha)
#             elif "IRRF" in texto:
#                 vals["ir"] = extrair_valor(proxima_linha)
#             elif "PIS - DÉBITO" in texto or (texto == "PIS"):
#                 vals["pis"] = extrair_valor(proxima_linha)
#             elif "COFINS - DÉBITO" in texto or (texto == "COFINS"):
#                 vals["cofins"] = extrair_valor(proxima_linha)
#             elif "CONTRIBUIÇÕES SOCIAIS" in texto:
#                 vals["csll"] = extrair_valor(proxima_linha)
#             elif "CONTRIBUIÇÃO PREVIDENCIÁRIA" in texto:
#                 vals["inss"] = extrair_valor(proxima_linha)
#     return vals

# def pegar_dados_servico(linhas):
#     dados = {"codigo": None, "descricao": None}
#     capturando = False
#     partes = []
#     for linha in linhas:
#         texto = linha.strip()
#         if "CÓDIGO DE TRIBUTAÇÃO NACIONAL" in texto.upper():
#             capturando = True
#             continue
#         if capturando:
#             if "CÓDIGO DE TRIBUTAÇÃO MUNICIPAL" in texto.upper():
#                 break
#             if texto:
#                 partes.append(texto)
#     if partes:
#         texto_completo = " ".join(partes)
#         match_curto = re.search(r'(\d{2}\.\d{2})', texto_completo)
#         match_split = re.search(r'^([\d.]+)\s*[-]?\s*(.*)', texto_completo)
#         if match_split:
#             cod_cheio = match_split.group(1).strip()
#             texto_desc = match_split.group(2).strip()
#             dados["codigo"] = match_curto.group(1) if match_curto else cod_cheio[:5]
#             dados["descricao"] = f"{cod_cheio} - {texto_desc}"
#         else:
#             dados["codigo"] = match_curto.group(1) if match_curto else None
#             dados["descricao"] = texto_completo

#     return dados
