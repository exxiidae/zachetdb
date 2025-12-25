from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from app.database import engine
from app import models
from app.routers import authors, posts

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="zachet", version="1.0.0")

# Подключаем роутеры
app.include_router(authors.router, prefix="/api/v1", tags=["authors"])
app.include_router(posts.router, prefix="/api/v1", tags=["posts"])

# Настраиваем статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Корневой маршрут для отображения HTML
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Дополнительный маршрут для проверки здоровья
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}
