import statistics
from pydantic import BaseModel
from typing import List

class Books(BaseModel):
    titulo: str
    preço: float
    avaliação: str
    disponibilidade: str
    categoria: str
    imagem: str

def analise_dados(data: List[Books], categoria: str = None) -> dict:
    """
    Estatísticas gerais da coleção: total de livros, preço médio, distribuição de ratings
    
    Parâmetros:
    dados (dataset books.csv): Uma lista de livros para serem analisados
    
    Retorna:
    dict: Um dicionário contendo total de livros, preço médio, distribuição de ratings
    """
    
    if categoria:
        dados = [book for book in data if book["Categoria"].lower() == categoria.lower()]
    else:
        dados = data

    total_livros = len(dados)
    precos = [float(book["Preço"][1:]) for book in dados]
    preco_medio = round(statistics.mean(precos), 2) if precos else 0.0

    distribuicao_ratings = {}
    for book in dados:
        rating = book["Avaliação"]
        if rating in distribuicao_ratings:
            distribuicao_ratings[rating] += 1
        else:
            distribuicao_ratings[rating] = 1

    return {
        "total_livros": total_livros,
        "preco_medio": preco_medio,
        "distribuicao_ratings": distribuicao_ratings
    }