from lib.leitura_pasta import listar_arquivos
from lib.leitura_arquivo import ler_pdfplumber
from capture.danfse import leitura_danfse
from capture.giss import leitura_giss
from capture.municipio_pontal import leitura_municipio_pontal
from capture.nota_desconhecida import leitura_desconhecida
from capture.giap import leitura_giap
from capture.municipio_sao_paulo import leitura_municipio_sao_paulo
from capture.senior import leitura_senior
from capture.ginfes import leitura_ginfes
from capture.issweb import leitura_issweb
from capture.municipo_sorocaba import leitura_municipio_sorocaba
from capture.giss_xml import leitura_xml_giss
from capture.municipio_barueri import leitura_municipio_barueri
from capture.municipio_sao_jose_do_rio_preto import leitura_municipio_sao_jose_do_rio_preto
from capture.lck_ibitinga import leitura_lck
from capture.primaxonline import leitura_primax

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

            if "DANFSe v1.0" in texto:
                ...
                # print("1")
                # print(arquivo)
                leitura_danfse(texto, arquivo)
            if "DANFSev1.0" in texto:
                ...
                # print("2")
                # print(arquivo)
                leitura_danfse(texto, arquivo)
            elif "Exigibilidade ISSQN" in texto:
                ...
                # leitura_giss(texto)
            elif "giap.com.br" in texto:
                ...
                # leitura_giap(texto)
            elif "senior.com.br" in texto or "Gerado por eDocs" in texto:
                ...
                # leitura_senior(texto)
            elif "ginfes.com.br" in texto:
                ...
                # leitura_ginfes(texto)
            elif "/issweb" in texto:
                ...
                # leitura_issweb(texto)
            elif "Prefeitura Municipal de Pontal" in texto and "Exigibilidade do ISS" in texto:
                ...
                # leitura_municipio_pontal(texto)
            elif "Lei nº 14.097/2005" in texto:
                ...
                # leitura_municipio_sao_paulo(texto)
            elif "Número / Série" in texto:
                ...
                # leitura_municipio_sorocaba(texto)
            elif "http://www.barueri.sp.gov.br/nfe" in texto:
                ...
                # leitura_municipio_barueri(texto)
            elif "SÃO JOSÉ DO RIO PRETO " in texto:
                ...
                # leitura_municipio_sao_jose_do_rio_preto(texto)
            elif "LCK Consultoria e Sistemas" in texto:
                ...
                # leitura_lck(texto)
            elif "www.primaxonline.com.br" in texto:
                ...
                # leitura_primax(texto)
            else:
                ...
                # leitura_desconhecida(texto)