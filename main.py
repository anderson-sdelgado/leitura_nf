import re
from lib.leitura_pasta import listar_arquivos
from lib.leitura_arquivo import ler_pdfplumber
from capture.danfse import leitura_danfse
from capture.giss import leitura_giss
from capture.nota_desconhecida import leitura_desconhecida
from capture.giap import leitura_giap
from capture.municipio_sao_paulo import leitura_municipio_sao_paulo
from capture.senior import leitura_senior
from capture.ginfes import leitura_ginfes
from capture.issweb import leitura_issweb
from capture.municipo_sorocaba import leitura_municipio_sorocaba
from capture.giss_xml import leitura_xml_giss
from capture.municipio_barueri import leitura_municipio_barueri
from capture.sigcorp import leitura_sgicorp
from capture.lck_ibitinga import leitura_lck
from capture.primaxonline import leitura_primax
from capture.issnet import leitura_issnet

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
                # r'DANFSe\s*v1.0': leitura_danfse, # ok
                # r'S[eé]rie\s*RPS.*?Tipo\s*RPS': leitura_giss, # ok
                # r'Nº\s*Nota\s+\d+.*?Nº\s*RPS:': leitura_giap, #ok
                # r'Data\s*d[ao]\s*[DR]PS': leitura_issweb, #ok
                # r'N[uú]mero\s*do\s*RPS*?\s*No.\s*da\s*NFS-e\s*': leitura_ginfes, #ok
                # r'Natureza\s*da\s*Opera[cç][aâãáà]o*?\s*N[uú]mero\s*do\s*RPS\s*': leitura_issnet, #ok
                r'Lei\s+nº\s+14\.097/2005': leitura_municipio_sao_paulo,
                # r'senior\.com\.br|Gerado\s+por\s+eDocs': leitura_senior,
                # r'Número\s+/\s+Série': leitura_municipio_sorocaba,
                # r'barueri\.sp\.gov\.br/nfe': leitura_municipio_barueri,
                # r'Cálculo\s+do\s+ISSQN\s+devido': leitura_sgicorp,
                # r'LCK\s+Consultoria\s+e\s+Sistemas': leitura_lck,
                # r'No\.\s+Controle.*?Chave\s+de\s+Segurança|www\.primaxonline\.com\.br': leitura_primax,
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