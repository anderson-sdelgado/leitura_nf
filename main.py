from lib.leitura_pasta import listar_pdfs
from lib.leitura_arquivo import ler_pdfplumber, ler_pymupedf
from capture.danfse import leitura_danfse
from capture.giss import leitura_giss
from capture.municipio_pontal import leitura_municipio_pontal
from capture.nota_desconhecida import leitura_desconhecida

if __name__ == "__main__":
    arquivos_pdf = listar_pdfs("download")

    todas_notas = []

    for arquivo in arquivos_pdf:
        texto = ler_pdfplumber(arquivo)
        if "DANFSev1.0" in texto:
            leitura_danfse(arquivo)
        elif "Exigibilidade ISSQN" in texto:
        #     # leitura_giss(pymupedf)
            leitura_giss(texto)
        # # elif "Prefeitura Municipal de Pontal" in pymupedf and  "Nome/Razão Social" in texto_inicio:
        # #     leitura_municipio_pontal(pdfplumber)
        # else:
        #     leitura_desconhecida(texto)