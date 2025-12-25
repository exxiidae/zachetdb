from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

import sys
from pathlib import Path

# Решаем проблему импорта
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Создание app с кастомизацией
app = FastAPI(
    title="ZachetDB API",
    description="Документация API для блога",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/docs", include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=app.title + " - Swagger UI",
        swagger_ui_parameters={
            "docExpansion": "none",
            "filter": True,
            "tryItOutEnabled": True,
        }
    )

@app.get("/openapi.json", include_in_schema=False)
async def openapi():
    return app.openapi()

# Настройки CORS
origins = ["http://localhost", "http://localhost:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Импорт роутеров (пробуем разные варианты)
try:
    from routers import authors, posts
except ImportError:
    try:
        from .routers import authors, posts
    except ImportError:
        from app.routers import authors, posts

app.include_router(authors.router, prefix="/api/v1", tags=["authors"])
app.include_router(posts.router, prefix="/api/v1", tags=["posts"])

# Статика и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
