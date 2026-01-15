from fastapi import APIRouter
from src.scraping import scraping

router = APIRouter(prefix="/api/v1/scraping", tags=["Scraping"])

@router.post("/trigger")
async def trigger_scraping():
    return {"message": scraping.scrape_books()}
