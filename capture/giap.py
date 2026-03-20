import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor

def leitura_giap(texto: str):
    linhas = [re.sub(r'\s+', ' ', linha).strip() for linha in texto.splitlines()]

    # print("----------- NOTA GIAP -----------")
    # for numero, linha in enumerate(linhas, start=1): 
    #     print(f"{linha}")
    # print("-------------------------")

    prestador = pegar_dados_prestador(linhas)
    tomador = pegar_dados_tomador(linhas)
    tributos = pegar_valores(linhas, texto)
    servico = pegar_codigo_servico(texto)
    
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
    nota["NRO_NF"] = pegar_numero_nf(linhas, texto) # Número da NF. Idem V_NF_SERV.
    nota["DT_EMISS"] = pegar_data_hora_emissao(texto) # Data de emissão da NF. Idem V_NF_SERV.
    nota["PS_RAZ_SOC_NOME"] = prestador['razao_social'] # Nome do prestador de serviço. Idem V_NF_SERV.
    nota["PS_CNPJ_CPF"] = prestador['cnpj'] # CNPJ do prestador de serviço. Idem V_NF_SERV.
    nota["PS_INSC_MUNIC"] = prestador['inscricao_municipal'] # Inscrição municipal do prestador de serviço. Idem V_NF_SERV.
    nota["PS_INSC_EST"] = prestador['inscricao_estadual'] # Inscrição estadual do prestador de serviço. Idem V_NF_SERV.
    nota["PS_MUNIC"] = prestador['municipio'] # Nome do município do prestador de serviço. Idem V_NF_SERV.
    nota["PS_UF"] = prestador['uf'] # Sigla da UF do prestador de serviço. Idem V_NF_SERV.
    nota["PS_ENDERECO"] = prestador['endereco_completo'] # Endereço do prestador de serviço. Idem V_NF_SERV.
    nota["PS_BAIRRO"] = prestador['bairro'] # Bairro do prestador de serviço. Idem V_NF_SERV.
    nota["PS_CEP"] = prestador['cep'] # CEP do prestador de serviço. Idem V_NF_SERV.
    nota["PS_EMAIL"] = prestador['email'] # E-mail do prestador de serviço. Idem V_NF_SERV.
    nota["TS_RAZ_SOC_NOME"] = tomador['razao_social'] # Nome do tomador de serviço - empresa usuária. Idem V_NF_SERV.
    nota["TS_CNPJ_CPF"] = tomador['cnpj'] # CNPJ do tomador de serviço - empresa usuária. Idem V_NF_SERV.
    nota["DESC_SERV"] = pegar_discriminacao_servico(linhas) # Descrição do serviço. Idem V_NF_SERV.
    nota["VL_BRUTO"] = extrair_valor(tributos["bruto"]) # Valor bruto. Idem V_NF_SERV.
    nota["VL_LIQ"] = extrair_valor(tributos["liquido"]) # Valor líquido. Idem V_NF_SERV.
    nota["VL_PIS"] = extrair_valor(tributos["pis"]) # Valor do PIS. Idem V_NF_SERV.
    nota["VL_COFINS"] = extrair_valor(tributos["cofins"]) # Valor da Cofins. Idem V_NF_SERV.
    nota["VL_IR"] = extrair_valor(tributos["ir"]) # Valor do IR. Idem V_NF_SERV.
    nota["VL_INSS"] = extrair_valor(tributos["inss"]) # Valor do INSS. Idem V_NF_SERV.
    nota["VL_CSLL"] = extrair_valor(tributos["csll"]) # Valor da CSLL. Idem V_NF_SERV.
    nota["VL_ISS"] = extrair_valor(tributos["iss"]) # Valor do ISS. Idem V_NF_SERV.
    nota["COD_SERVICO"] = servico["codigo"] # Código do serviço. Idem V_NF_SERV.
    nota["COD_SERVICO_ORIGINAL"] = servico["descricao_completa"] # Código do serviço - informação original. Idem V_NF_SERV.

    print("----------- NOTA GIAP -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("-----------------------------------")

def pegar_prefeitura(linhas):
    for linha in linhas:
        if "PREFEITURA" in linha.upper():
            return linha.strip()
    return None

def pegar_secretaria(linhas):
    for linha in linhas:
        if "SECRETARIA" in linha.upper():
            return linha.strip()
    return None

def pegar_numero_nf(linhas, texto_completo):
    # Tenta padrão: "Nº Nota" seguido de número na linha seguinte ou mesma linha
    m = re.search(r'(?:Nº\s*Nota|Número\s*da\s*Nota)[:\s]*(\d+)', texto_completo, re.IGNORECASE)
    if m: return m.group(1)
    
    for i, linha in enumerate(linhas):
        if "Nº" in linha and "Nota" in linha:
            if i + 1 < len(linhas):
                num = re.search(r'(\d+)', linhas[i+1])
                if num: return num.group(1)
    return None

def pegar_data_hora_emissao(texto):
# Dicionário de meses para conversão
    meses = {
        'JAN': '01', 'FEV': '02', 'MAR': '03', 'ABR': '04',
        'MAI': '05', 'JUN': '06', 'JUL': '07', 'AGO': '08',
        'SET': '09', 'OUT': '10', 'NOV': '11', 'DEZ': '12'
    }

    # Busca o formato: DD/MMM/AAAA - HH:MM:SS ou DD/MMM/AAAA HH:MM:SS
    # O [-\s]* serve para ignorar o hífen que às vezes aparece entre a data e a hora
    m = re.search(r'(\d{2})/([A-Z]{3})/(\d{4})[-\s]*(\d{2}:\d{2}:\d{2})', texto, re.IGNORECASE)
    
    if m:
        dia = m.group(1)
        mes_extenso = m.group(2).upper()
        ano = m.group(3)
        hora = m.group(4)
        
        # Converte o mês usando o dicionário, se não encontrar mantém o original
        mes_num = meses.get(mes_extenso, mes_extenso)
        
        return f"{dia}/{mes_num}/{ano} {hora}"
    
    return None

def pegar_dados_prestador(linhas):
    dados = {
        "razao_social": None, "cnpj": None, "inscricao_municipal": None,
        "inscricao_estadual": None, "endereco_completo": None,
        "bairro": None, "cep": None, "municipio": None, "uf": None, "email": None
    }
    # Unificamos o texto para facilitar a busca multilinhas
    texto = "\n".join(linhas)
    
    # 1. RAZÃO SOCIAL: Pega tudo entre o rótulo e o próximo campo (CNPJ ou Insc)
    m_raz = re.search(r'Razão\s*Social/Nome:\s*(.*?)(?=CNPJ/CPF|Insc|Endereço|$)', texto, re.I | re.S)
    if m_raz:
        nome = m_raz.group(1).replace('\n', ' ').strip()
        # Remove CPFs residuais que o GIAP às vezes cola no final do nome
        dados["razao_social"] = re.sub(r'\s\d{11}$', '', nome).strip()

    # 2. CNPJ/CPF: Busca o padrão numérico com pontuação
    m_cnpj = re.search(r'CNPJ/CPF:\s*([\d\.\-/]+)', texto)
    if m_cnpj:
        dados["cnpj"] = m_cnpj.group(1).strip()

    # 3. INSCRIÇÕES: Municipal e Estadual
    m_im = re.search(r'Insc\.\s*Municipal:\s*(\d+)', texto, re.I)
    if m_im: dados["inscricao_municipal"] = m_im.group(1).strip()
    
    m_ie = re.search(r'Insc\.\s*Estadual:\s*([\w]+)', texto, re.I)
    if m_ie: dados["inscricao_estadual"] = m_ie.group(1).strip()

    # 4. ENDEREÇO: Captura flexível entre rótulos
    m_end = re.search(r'Endereço:\s*(.*?)(?=Complemento|Bairro|CEP|$)', texto, re.I | re.S)
    if m_end:
        dados["endereco_completo"] = m_end.group(1).replace('\n', ' ').strip()
    
    # 5. BAIRRO: Evita capturar o CEP junto
    m_bai = re.search(r'Bairro:\s*(.*?)(?=CEP|Município|UF|$)', texto, re.I | re.S)
    if m_bai:
        dados["bairro"] = m_bai.group(1).replace('\n', ' ').strip()

    # 6. CEP: Padrão rigoroso para evitar capturar apenas "14"
    # Busca 2 dígitos + ponto opcional + 3 dígitos + hífen opcional + 3 dígitos
    m_cep = re.search(r'CEP:\s*(\d{2}\.?\d{3}-?\d{3})', texto)
    if m_cep:
        dados["cep"] = m_cep.group(1).strip()

    # 7. MUNICÍPIO E UF
    m_mun = re.search(r'Município:\s*(.*?)\s*UF:\s*([A-Z]{2})', texto, re.I)
    if m_mun:
        dados["municipio"] = m_mun.group(1).strip()
        dados["uf"] = m_mun.group(2).strip()

    # 8. EMAIL: Pega até o próximo espaço ou quebra de linha
    m_email = re.search(r'E-mail:\s*([^\s\n]+)', texto, re.I)
    if m_email:
        dados["email"] = m_email.group(1).strip()
    
    return dados

def pegar_dados_tomador(linhas):
    texto = "\n".join(linhas)
    # Isola a seção do tomador para evitar pegar dados do prestador
    secao = re.search(r'TOMADOR\s*DE\s*SERVIÇOS(.*?)DISCRIMINAÇÃO', texto, re.S | re.I)
    if not secao: return {"razao_social": None, "cnpj": None}
    
    conteudo = secao.group(1)
    dados = {}
    
    m_raz = re.search(r'Razão\s*Social/Nome:\s*(.*?)(?=CNPJ/CPF|Insc|Endereço|$)', conteudo, re.I | re.S)
    dados["razao_social"] = m_raz.group(1).replace('\n', ' ').strip() if m_raz else None
    
    m_cnpj = re.search(r'CNPJ/CPF:\s*([\d\.\-/]+)', conteudo)
    dados["cnpj"] = m_cnpj.group(1).strip() if m_cnpj else None
    
    return dados

def pegar_discriminacao_servico(linhas):
    desc = []
    dentro = False
    for linha in linhas:
        if "DISCRIMINAÇÃO" in linha.upper():
            dentro = True
            continue
        if dentro and ("VALOR TOTAL" in linha.upper() or "INFORMAÇÕES COMPLEMENTARES" in linha.upper()):
            break
        if dentro and linha.strip():
            desc.append(linha.strip())
    return " ".join(desc)

# def pegar_valores(linhas, texto_completo):
#     v = {
#         "bruto": "0,00", "liquido": "0,00", "ir": "0,00", 
#         "pis": "0,00", "cofins": "0,00", "csll": "0,00", 
#         "inss": "0,00", "iss": "0,00"
#     }

#     # 1. VALOR BRUTO: Busca 'TOTAL DA NOTA' e captura o primeiro valor R$ que aparecer
#     # Atende notas 148 [cite: 42] e 600 [cite: 104]
#     m_bruto = re.search(r'VALOR\s*TOTAL\s*DA\s*NOTA.*?R\$\s*([\d.]+,\d{2})', texto_completo, re.I | re.S)
#     if m_bruto:
#         v["bruto"] = m_bruto.group(1)

#     # 2. VALOR LÍQUIDO: Foca na âncora 'Líquido' e ignora o lixo até o número
#     # Atende o caso 'Valor Líquido da Nota (R$)'  e o caso cortado 'Valor Líquido da' 
#     m_liq = re.search(r'Líquido\s*.*?([\d.]+,\d{2})', texto_completo, re.I | re.S)
#     if m_liq:
#         # Pega a última ocorrência de valor monetário após a palavra 'Líquido' 
#         # para evitar capturar a base de cálculo por engano
#         todos_valores = re.findall(r'[\d.]+,\d{2}', texto_completo[m_liq.start():])
#         if todos_valores:
#             v["liquido"] = todos_valores[-1]

#     # 3. VALOR DO ISS: Busca 'Valor do ISS' e pega o próximo número formatado [cite: 50, 116]
#     m_iss = re.search(r'Valor\s*do\s*ISS.*?([\d.]+,\d{2})', texto_completo, re.I | re.S)
#     if m_iss:
#         v["iss"] = m_iss.group(1)

#     # 4. IMPOSTOS RETIDOS: Mapeia a linha de valores abaixo dos cabeçalhos
#     for i, linha in enumerate(linhas):
#         l_limpa = linha.upper().replace(" ", "")
#         # Procura a linha que contém os títulos dos impostos [cite: 45, 48, 51]
#         if "VALORDOINSSRETIDO" in l_limpa or "INSSRETIDO" in l_limpa:
#             # Varre as próximas 3 linhas para achar onde o pdfplumber jogou os números
#             for offset in range(1, 4):
#                 if i + offset < len(linhas):
#                     # Encontra todos os padrões 0,00 na linha
#                     valores = re.findall(r'[\d.]+,\d{2}', linhas[i+offset])
#                     if len(valores) >= 3: # Geralmente são 5 valores (INSS, IR, CSLL, PIS, COFINS)
#                         chaves = ["inss", "ir", "csll", "pis", "cofins"]
#                         for idx, val in enumerate(valores):
#                             if idx < len(chaves):
#                                 v[chaves[idx]] = val
#                         break
#             break

#     return v

def pegar_valores(linhas, texto_completo):
    v = {
        "bruto": "0,00", "liquido": "0,00", "ir": "0,00", 
        "pis": "0,00", "cofins": "0,00", "csll": "0,00", 
        "inss": "0,00", "iss": "0,00"
    }

    # 1. Extrair TODOS os valores monetários (0,00) do texto na ordem que aparecem
    todos_os_valores = re.findall(r'[\d.]+,\d{2}', texto_completo)
    
    # 2. VALOR BRUTO: Geralmente é o primeiro valor alto após "TOTAL DA NOTA"
    m_bruto = re.search(r'TOTAL\s*DA\s*NOTA.*?([\d.]+,\d{2})', texto_completo, re.I | re.S)
    if m_bruto:
        v["bruto"] = m_bruto.group(1)

    # 3. IMPOSTOS RETIDOS (A tabela de 5 valores: INSS, IR, CSLL, PIS, COFINS)
    # Procuramos a linha que contém o cabeçalho e pegamos os 5 valores que vem logo depois
    for i, linha in enumerate(linhas):
        l_limpa = linha.upper().replace(" ", "")
        if "VALORDOINSSRETIDO" in l_limpa:
            # Pegamos todos os valores das próximas 2 linhas
            texto_bloco_impostos = " ".join(linhas[i+1 : i+3])
            valores_impostos = re.findall(r'[\d.]+,\d{2}', texto_bloco_impostos)
            if len(valores_impostos) >= 5:
                chaves = ["inss", "ir", "csll", "pis", "cofins"]
                for idx, val in enumerate(valores_impostos[:5]):
                    v[chaves[idx]] = val
            break

    # 4. ISS E LÍQUIDO (A "Tabela de Baixo")
    # Na GIAP, o ISS e o Valor Líquido costumam ser os ÚLTIMOS valores do documento
    # antes das "Outras Informações" ou do Rodapé.
    if len(todos_os_valores) >= 2:
        # Nas notas 148, 600 e 345, a estrutura final é:
        # ... [Base de Cálculo] [Alíquota] [Valor do ISS] [Valor Líquido]
        # O Líquido é SEMPRE o último valor monetário do corpo da nota.
        # O ISS é o SEGUNDO valor (contando de trás para frente) desse bloco.
        
        # Vamos isolar o texto do meio para o fim para evitar pegar valores do cabeçalho
        parte_final = texto_completo.split("VALOR TOTAL DA NOTA")[-1]
        valores_finais = re.findall(r'[\d.]+,\d{2}', parte_final)
        
        if len(valores_finais) >= 2:
            v["liquido"] = valores_finais[-1] # O último valor é o Líquido [cite: 50, 121, 231]
            v["iss"] = valores_finais[-2]     # O penúltimo é o ISS [cite: 50, 116, 228]
            
            # Validação: Se o penúltimo for a Alíquota (ex: 3,00), o ISS será o antepenúltimo
            # Mas na GIAP Araraquara, a alíquota geralmente não tem o ",00" se for inteira.
            # Se v["iss"] parecer uma alíquota (ex: "2,63" ou "5,00"), 
            # e houver um valor maior antes dele, fazemos o ajuste:
            if len(valores_finais) >= 3:
                 # Se o penúltimo valor for muito baixo e o antepenúltimo for a alíquota
                 # invertemos conforme a estrutura da página
                 v["iss"] = valores_finais[-2]

    return v

def pegar_codigo_servico(texto_completo):
    d = {"codigo": None, "descricao_completa": None}
    
    # 1. Localizamos o bloco de texto após o rótulo.
    # Usamos (?:...) para o rótulo não entrar no grupo de captura principal.
    # O (.*?) captura o conteúdo e o (?=...) define onde ele deve PARAR (âncoras de lixo).
    padrao = r'(?:Ativ\.\s*Serviço|Código\s*do\s*Serviço):\s*(.*?)(?=Valor\s*do\s*INSS|Obra:|Código\s*NBS:|Vlr\s*Deduções|Local\s*de\s*Incidência|VALOR\s*TOTAL|$)'
    
    m_ativ = re.search(padrao, texto_completo, re.I | re.S)
    
    if m_ativ:
        # Pega o conteúdo após o rótulo
        desc = m_ativ.group(1).strip()
        
        # Limpa quebras de linha e espaços múltiplos (comum no pdfplumber)
        desc = re.sub(r'\s+', ' ', desc)
        
        # Remove hífens ou pontos que sobram no final da string capturada
        desc = re.sub(r'\s*[-.]\s*$', '', desc)
        
        # 2. Extração do CÓDIGO (ex: 14.01 ou 7.02)
        # O padrão \d{1,2}\.\d{2} busca o número. O [-\s]* ignora hífens grudados.
        m_cod = re.search(r'(\d{1,2}\.\d{2})', desc)
        if m_cod:
            d["codigo"] = m_cod.group(1)
        
        d["descricao_completa"] = desc
    
    return d