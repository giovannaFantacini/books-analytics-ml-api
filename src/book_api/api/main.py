from fastapi import FastAPI

from src.book_api.api .routers import auth, books, categories, health, stats, scraping, ml

app = FastAPI(
    title="Tech Challenge Fiap",
    description=(
        "API do Tech Challenge: realiza scraping no 'Books to Scrape' e expõe endpoints "
        "de consulta, estatísticas e predição de avaliação."
    ),
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(categories.router)
app.include_router(health.router)
app.include_router(stats.router)
app.include_router(scraping.router)
app.include_router(ml.router)
