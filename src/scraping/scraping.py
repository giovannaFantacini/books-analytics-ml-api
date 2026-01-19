import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_web_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        return html_content
    else:
        print(f"Falha ao obter a página. Código de status: {response.status_code}")
        return ConnectionRefusedError

def scrape_books():
    url = 'https://books.toscrape.com/'
    response = requests.get(url)

    books = []
    categories = []
    html_content = get_web_page(url)
    soup = BeautifulSoup(html_content, 'html.parser')

    for side_category in soup.select("div.side_categories ul li a"):
        category = side_category.get_text().strip()
        link = url + side_category['href']
        if category != 'Books':
            categories.append({
                "Categoria": category,
                "Link": link
            })

    for category in categories:
        html_content = get_web_page(category["Link"])
        soup = BeautifulSoup(html_content, 'html.parser')
        for book in soup.select('article.product_pod'):
            titulo = book.h3.a["title"]
            preco = book.select('p.price_color')[0].get_text()[1:]
            rating = book.select('p.star-rating')[0]['class'][1]
            disponibilidade = book.select('p.instock.availability')[0].get_text().strip()
            categoria = category["Categoria"]
            imagem = book.select('div.image_container a img')[0]['src']
            imagem = url + imagem.replace('../', '')
            books.append({
                "Título": titulo,
                "Preço": preco,
                "Avaliação": rating,
                "Disponibilidade": disponibilidade,
                "Categoria": categoria,
                "Imagem": imagem
            })

    books_to_df = pd.DataFrame(books)   
    books_to_df.to_csv('data/books.csv', index=False)
    return "Scraping concluído e dados salvos em 'data/books.csv'"