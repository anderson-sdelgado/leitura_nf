import re

from lib.leitura_pasta import listar_arquivos
from lib.leitura_arquivo import ler_pdfplumber

from capture.sistema_xml_giss import leitura_sistema_xml_giss
from capture.sistema_danfse import leitura_sistema_danfse
from capture.sistema_giap import leitura_sistema_giap
from capture.sistema_ginfes import leitura_sistema_ginfes
from capture.sistema_giss import leitura_sistema_giss
from capture.sistema_issnet import leitura_sistema_issnet
from capture.sistema_issweb import leitura_sistema_issweb
from capture.sistema_primax import leitura_sistema_primax
from capture.sistema_sigissweb import leitura_sistema_sigissweb
from capture.sistema_atende_net import leitura_sistema_atende_net
from capture.sistema_senior import leitura_sistema_senior
from capture.sistema_ferrisoft import leitura_sistema_ferrisoft

from capture.municipio_sao_paulo import leitura_municipio_sao_paulo
from capture.municipio_barueri import leitura_municipio_baureri
from capture.municipio_cajamar import leitura_municipio_cajamar
from capture.municipio_campinas import leitura_municipio_campinas
from capture.municipio_campo_grande import leitura_municipio_campo_grande

from capture.nota_desconhecida import leitura_desconhecida

if __name__ == "__main__":
    arquivos_pdf = listar_arquivos("download")

    todas_notas = []

    for arquivo in arquivos_pdf:
        nome_arquivo = arquivo.lower()

        if nome_arquivo.endswith(".xml"):
            print(f"Processando XML: {arquivo}")
            # leitura_xml_giss(arquivo)
            continue # Vai para o próximo arquivo

        elif nome_arquivo.endswith(".pdf"):
            texto = ler_pdfplumber(arquivo)

            # Verificação crucial: se o texto for None (erro), pula para o próximo
            if texto is None:
                ...
                # print(f"Pulando arquivo devido a erro de leitura: {arquivo}")
                continue

            identificadores = {
                # r'DANFSe\s*v1.0': leitura_sistema_danfse, # ok
                # r'Nº\s*Nota\s+\d+.*?Nº\s*RPS:': leitura_sistema_giap, #ok
                # r'N[uú]mero\s*do\s*RPS*?\s*No.\s*da\s*NFS-e\s*': leitura_sistema_ginfes, #ok
                # r'S[eé]rie\s*RPS.*?Tipo\s*RPS': leitura_sistema_giss, # ok
                # r'Natureza\s*da\s*Opera[cç][aâãáà]o*?\s*N[uú]mero\s*do\s*RPS\s*': leitura_sistema_issnet, #ok
                # r'Data\s*d[ao]\s*[DR]PS': leitura_sistema_issweb, #ok
                # r'No\.\s+Controle.*?Chave\s+de\s+Segurança|www\.primaxonline\.com\.br': leitura_sistema_primax, #ok
                # r'N[uúùû]mero\s*e\s*S[eéèê]rie\s*do\s*RPS': leitura_sistema_sigissweb, #ok
                # r'\s*atende.net\s*': leitura_sistema_atende_net, #ok
                # r'\s*senior.com\s*': leitura_sistema_senior, #ok
                # r'\s*FerriSoft\s*': leitura_sistema_ferrisoft, #ok
                # r'Lei\s+nº\s+14\.097/2005': leitura_municipio_sao_paulo, #ok
                # r'\s*barueri.sp.gov.br\s*': leitura_municipio_baureri, #ok
                # r'\s*CAJAMAR\s*': leitura_municipio_cajamar, #ok
                # r'\s*NFSe\s*Campinas\s*': leitura_municipio_campinas, #ok
                r'\s*-\s*SEFIN\s*': leitura_municipio_campo_grande, 
            }
            nota_processada = False
            
            for regex, funcao_leitura in identificadores.items():
                if re.search(regex, texto, re.I | re.S):
                    print(f"Identificado padrão para: {arquivo}")
                    dados = funcao_leitura(texto)
                    if dados:
                        todas_notas.append(dados)
                    nota_processada = True
                    break # Para de procurar após encontrar o primeiro padrão correspondente

            if not nota_processada:
                ...
                # print(f"Padrão desconhecido para: {arquivo}")
                # leitura_desconhecida(texto)