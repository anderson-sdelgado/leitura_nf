import os

def listar_pdfs(caminho_pasta: str) -> list:
    if not os.path.exists(caminho_pasta):
        raise FileNotFoundError("Pasta não encontrada")

    return [
        os.path.join(caminho_pasta, arquivo)
        for arquivo in os.listdir(caminho_pasta)
        if arquivo.lower().endswith(".pdf")
    ]