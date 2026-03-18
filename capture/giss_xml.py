import xml.etree.ElementTree as ET
from datetime import datetime
from lib.limpar_cnpj import limpar_cnpj, formatar_cnpj # Importe a nova função

def leitura_xml_giss(caminho_xml: str):
    try:
        tree = ET.parse(caminho_xml)
        root = tree.getroot()
        ns = {'ns': 'http://www.abrasf.org.br/nfse.xsd'}
        inf_nfse = root.find('.//ns:InfNfse', ns)
        
        if inf_nfse is None:
            print(f"Erro: Estrutura do XML {caminho_xml} inválida.")
            return None
    
        cod_municipio_prestador = inf_nfse.findtext('.//ns:PrestadorServico//ns:Endereco/ns:CodigoMunicipio', namespaces=ns)

        # 2. Dicionário de Tradução (Para trazer o nome inteiro)
        tabela_prefeituras = {
            "3543402": "PREFEITURA MUNICIPAL DE RIBEIRAO PRETO",
            "3532900": "PREFEITURA MUNICIPAL DE MOCOCA",
            "3550308": "PREFEITURA MUNICIPAL DE SAO PAULO"
        }

        tabela_cidades = {
            "3543402": "RIBEIRAO PRETO",
            "3532900": "MOCOCA",
            "3550308": "SAO PAULO"
        }


        endereco_base = inf_nfse.find('.//ns:PrestadorServico//ns:Endereco', namespaces=ns)
        rua = endereco_base.findtext('ns:Endereco', namespaces=ns) # Rua Tambaú
        numero = endereco_base.findtext('ns:Numero', namespaces=ns)
        data_bruta = inf_nfse.findtext('ns:DataEmissao', namespaces=ns)
        data_formatada = None
        valores = inf_nfse.find('.//ns:Servico/ns:Valores', namespaces=ns)
        valores_nfse = inf_nfse.find('.//ns:ValoresNfse', namespaces=ns)
        
        if data_bruta:
            # Converte de 2026-03-17T13:50:49 para objeto de data e depois para texto BR
            dt_obj = datetime.fromisoformat(data_bruta)
            data_formatada = dt_obj.strftime("%d/%m/%Y %H:%M:%S")

        nota = {}
        nota["DT_HR_INCL"] = None # Data e hora da inclusão da linha.
        nota["DT_HR_ALT"] = None # Data e hora da alteração da linha.
        nota["CDDOCUMENT"] = None # Código do documento no SE Suite. Idem V_NF_SERV.
        nota["NRO_CHAVE"] = None # Chave para registro da NFs-e. Gerada na integração.
        nota["CPF_CNPJ_EMIT"] = inf_nfse.findtext('.//ns:TomadorServico/ns:IdentificacaoTomador/ns:CpfCnpj/ns:Cnpj', namespaces=ns) # CNPJ/CPF da empresa (tomador) - somente números. Vide V_NF_SERV.TS_CNPJ_CPF.
        nota["COD_PART"] = inf_nfse.findtext('.//ns:Prestador/ns:CpfCnpj/ns:Cnpj', namespaces=ns) # CNPJ/CPF do fornecedor (prestador) - somente números. Vide V_NF_SERV.PS_CNPJ_CPF.
        nota["COD_MOD"] = "99" # Código do modelo de documento fiscal para registro. Fixo "99".
        nota["SERIE"] = "A" # Série do documento fiscal para registro. Fixo "A".
        nota["DTINSERT"] = None # Data da inclusão no SE Suite. Idem V_NF_SERV.
        nota["DTUPDATE"] = None # Data da alteração no SE Suite. Idem V_NF_SERV.
        nota["ID_DOC"] = inf_nfse.findtext('ns:CodigoVerificacao', namespaces=ns) # ID do documento na view. Idem V_NF_SERV.
        nota["PREFEIT"] = tabela_prefeituras.get(cod_municipio_prestador, cod_municipio_prestador)
        nota["SECRET_PREFEIT"] = None # Secretaria da prefeitura. Idem V_NF_SERV.
        nota["NRO_NF"] = inf_nfse.findtext('ns:Numero', namespaces=ns) # Número da NF. Idem V_NF_SERV.
        nota["DT_EMISS"] = data_formatada # Data de emissão da NF. Idem V_NF_SERV.
        nota["PS_RAZ_SOC_NOME"] = inf_nfse.findtext('.//ns:PrestadorServico/ns:RazaoSocial', namespaces=ns) # Nome do prestador de serviço. Idem V_NF_SERV.
        nota["PS_CNPJ_CPF"] = formatar_cnpj(inf_nfse.findtext('.//ns:Prestador/ns:CpfCnpj/ns:Cnpj', namespaces=ns)) # CNPJ do prestador de serviço. Idem V_NF_SERV.
        nota["PS_INSC_MUNIC"] = inf_nfse.findtext('.//ns:Prestador/ns:InscricaoMunicipal', namespaces=ns) # Inscrição municipal do prestador de serviço. Idem V_NF_SERV.
        nota["PS_INSC_EST"] = None # Inscrição estadual do prestador de serviço. Idem V_NF_SERV.
        nota["PS_MUNIC"] = tabela_cidades.get(cod_municipio_prestador, cod_municipio_prestador) # Nome do município do prestador de serviço. Idem V_NF_SERV.
        nota["PS_UF"] = inf_nfse.findtext('.//ns:PrestadorServico//ns:Endereco/ns:Uf', namespaces=ns) # Sigla da UF do prestador de serviço. Idem V_NF_SERV.
        nota["PS_ENDERECO"] = f"{rua}, {numero}" if rua and numero else rua # Endereço do prestador de serviço. Idem V_NF_SERV.
        nota["PS_BAIRRO"] = endereco_base.findtext('ns:Bairro', namespaces=ns) # Bairro do prestador de serviço. Idem V_NF_SERV.
        nota["PS_CEP"] = endereco_base.findtext('ns:Cep', namespaces=ns) # CEP do prestador de serviço. Idem V_NF_SERV.
        nota["PS_EMAIL"] = inf_nfse.findtext('.//ns:PrestadorServico//ns:Contato/ns:Email', namespaces=ns) # E-mail do prestador de serviço. Idem V_NF_SERV.
        nota["TS_RAZ_SOC_NOME"] = inf_nfse.findtext('.//ns:TomadorServico/ns:RazaoSocial', namespaces=ns) # Nome do tomador de serviço - empresa usuária. Idem V_NF_SERV.
        nota["TS_CNPJ_CPF"] = formatar_cnpj(inf_nfse.findtext('.//ns:TomadorServico/ns:IdentificacaoTomador/ns:CpfCnpj/ns:Cnpj', namespaces=ns)) # CNPJ do tomador de serviço - empresa usuária. Idem V_NF_SERV.
        nota["DESC_SERV"] = inf_nfse.findtext('.//ns:Servico/ns:Discriminacao', namespaces=ns).strip() # Descrição do serviço. Idem V_NF_SERV.
        nota["VL_BRUTO"] = valores.findtext('ns:ValorServicos', namespaces=ns) # Valor bruto. Idem V_NF_SERV.
        nota["VL_LIQ"] = valores_nfse.findtext('ns:ValorLiquidoNfse', namespaces=ns) # Valor líquido. Idem V_NF_SERV.
        nota["VL_PIS"] = valores.findtext('ns:ValorPis', namespaces=ns) # Valor do PIS. Idem V_NF_SERV.
        nota["VL_COFINS"] = valores.findtext('ns:ValorCofins', namespaces=ns) # Valor da Cofins. Idem V_NF_SERV.
        nota["VL_IR"] = valores.findtext('ns:ValorIr', namespaces=ns) # Valor do IR. Idem V_NF_SERV.
        nota["VL_INSS"] = valores.findtext('ns:ValorInss', namespaces=ns) # Valor do INSS. Idem V_NF_SERV.
        nota["VL_CSLL"] = valores.findtext('ns:ValorCsll', namespaces=ns) # Valor da CSLL. Idem V_NF_SERV.
        nota["VL_ISS"] = valores.findtext('ns:ValorIss', namespaces=ns) # Valor do ISS. Idem V_NF_SERV.
        nota["COD_SERVICO"] = inf_nfse.findtext('.//ns:Servico/ns:ItemListaServico', namespaces=ns) # Código do serviço. Idem V_NF_SERV.
        nota["COD_SERVICO_ORIGINAL"] = f"{inf_nfse.findtext('.//ns:Servico/ns:ItemListaServico', namespaces=ns)} - {inf_nfse.findtext('ns:DescricaoCodigoTributacaoMunicípio', namespaces=ns)}" # Código do serviço - informação original. Idem V_NF_SERV.

        print("----------- NOTA GISS XML -----------")
        for chave, valor in nota.items():
            print(f"{chave}: {valor}")
        print("-----------------------------------")


    except Exception as e:
        print(f"Erro ao processar XML: {e}")
        return None
