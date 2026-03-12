import re
from lib.limpar_cnpj import limpar_cnpj
from lib.converter_moeda import extrair_valor
from lib.leitura_arquivo import ler_pymupedf

def limpar_linha(linha):
    return re.sub(r'^\d+:\s*', '', linha).strip()

def leitura_giss(texto: str):
    linhas = texto.splitlines()
        
    # print("----------- NOTA GISS -----------")
    # for numero, linha in enumerate(linhas, start=1): 
    #     print(f"{linha}")
    # print("-------------------------")

#     nota = {}
#     nota["DT_HR_INCL"] = None # Data e hora da inclusão da linha.
#     nota["DT_HR_ALT"] = None # Data e hora da alteração da linha.
#     nota["CDDOCUMENT"] = None # Código do documento no SE Suite. Idem V_NF_SERV.
#     nota["NRO_CHAVE"] = None # Chave para registro da NFs-e. Gerada na integração.
#     nota["CPF_CNPJ_EMIT"] = limpar_cnpj(pegar_campo_tomador(linhas, "CPF/CNPJ:")) # CNPJ/CPF da empresa (tomador) - somente números. Vide V_NF_SERV.TS_CNPJ_CPF.
#     nota["COD_PART"] = limpar_cnpj(pegar_campo_prestador(linhas, "CPF/CNPJ:")) # CNPJ/CPF do fornecedor (prestador) - somente números. Vide V_NF_SERV.PS_CNPJ_CPF.
#     nota["COD_MOD"] = "99" # Código do modelo de documento fiscal para registro. Fixo "99".
#     nota["SERIE"] = "A" # Série do documento fiscal para registro. Fixo "A".
#     nota["DTINSERT"] = None # Data da inclusão no SE Suite. Idem V_NF_SERV.
#     nota["DTUPDATE"] = None # Data da alteração no SE Suite. Idem V_NF_SERV.
#     nota["ID_DOC"] = pegar_codigo_verificacao(linhas) # ID do documento na view. Idem V_NF_SERV.
#     nota["PREFEIT"] = prefeitura # Nome da prefeitura. Idem V_NF_SERV.
#     nota["SECRET_PREFEIT"] = secretaria # Secretaria da prefeitura. Idem V_NF_SERV.
#     nota["NRO_NF"] = pegar_valor(linhas, "NFS-e Substituída") # Número da NF. Idem V_NF_SERV.
#     nota["DT_EMISS"] = pegar_valor(linhas, "Emissão da NFS-e") # Data de emissão da NF. Idem V_NF_SERV.
#     nota["PS_RAZ_SOC_NOME"] = pegar_campo_prestador(linhas, "Nome/Razão Social:") # Nome do prestador de serviço. Idem V_NF_SERV.
#     nota["PS_CNPJ_CPF"] = pegar_campo_prestador(linhas, "CPF/CNPJ:") # CNPJ do prestador de serviço. Idem V_NF_SERV.
#     nota["PS_INSC_MUNIC"] = pegar_campo_prestador(linhas, "Inscrição") # Inscrição municipal do prestador de serviço. Idem V_NF_SERV.
#     nota["PS_INSC_EST"] = None # Inscrição estadual do prestador de serviço. Idem V_NF_SERV.
#     nota["PS_MUNIC"] = pegar_campo_prestador(linhas, "Município") # Nome do município do prestador de serviço. Idem V_NF_SERV.
#     nota["PS_UF"] = pegar_valor_mesma_linha_prestador(linhas, "UF") # Sigla da UF do prestador de serviço. Idem V_NF_SERV.
#     nota["PS_ENDERECO"] = pegar_endereco_completo(linhas) # Endereço do prestador de serviço. Idem V_NF_SERV.
#     nota["PS_BAIRRO"] = pegar_valor(linhas, "Bairro:") # Bairro do prestador de serviço. Idem V_NF_SERV.
#     nota["PS_CEP"] = pegar_valor(linhas, "CEP") # CEP do prestador de serviço. Idem V_NF_SERV.
#     nota["PS_EMAIL"] = pegar_email_prestador(linhas) # E-mail do prestador de serviço. Idem V_NF_SERV.
#     nota["TS_RAZ_SOC_NOME"] = pegar_campo_tomador(linhas, "Nome/Razão Social:") # Nome do tomador de serviço - empresa usuária. Idem V_NF_SERV.
#     nota["TS_CNPJ_CPF"] = pegar_campo_tomador(linhas, "CPF/CNPJ:") # CNPJ do tomador de serviço - empresa usuária. Idem V_NF_SERV.
#     nota["DESC_SERV"] = pegar_discriminacao_servico(linhas) # Descrição do serviço. Idem V_NF_SERV.
#     nota["VL_BRUTO"] = valor_bruto # Valor bruto. Idem V_NF_SERV.
#     nota["VL_LIQ"] = valor_liq # Valor líquido. Idem V_NF_SERV.
#     nota["VL_PIS"] = pis # Valor do PIS. Idem V_NF_SERV.
#     nota["VL_COFINS"] = cofins # Valor da Cofins. Idem V_NF_SERV.
#     nota["VL_IR"] = ir # Valor do IR. Idem V_NF_SERV.
#     nota["VL_INSS"] = inss # Valor do INSS. Idem V_NF_SERV.
#     nota["VL_CSLL"] = csll # Valor da CSLL. Idem V_NF_SERV.
#     nota["VL_ISS"] = pegar_issqn(linhas) # Valor do ISS. Idem V_NF_SERV.
#     nota["COD_SERVICO"] = codigo_servico # Código do serviço. Idem V_NF_SERV.
#     nota["COD_SERVICO_ORIGINAL"] = desc_servico_completa # Código do serviço - informação original. Idem V_NF_SERV.

    print("----------- NOTA GISS -----------")
    for chave, valor in nota.items():
        print(f"{chave}: {valor}")
    print("-----------------------------------")
