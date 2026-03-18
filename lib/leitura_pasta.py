import os

def listar_arquivos(caminho_pasta: str) -> list:
    if not os.path.exists(caminho_pasta):
        raise FileNotFoundError("Pasta não encontrada")

    # Agora aceita .pdf e .xml
    extensoes_permitidas = (".pdf", ".xml")
    return [
        os.path.join(caminho_pasta, arquivo)
        for arquivo in os.listdir(caminho_pasta)
        if arquivo.lower().endswith(extensoes_permitidas)
    ]