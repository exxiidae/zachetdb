from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="ZachetDB Blog API",
    description="""
    ## 📖 Полная документация API для блога ZachetDB

    Это полнофункциональное бэкенд-приложение на **FastAPI**, реализующее блог с авторами и постами.

    ### 🚀 Основные возможности
    *   **CRUD для авторов** — создание, чтение, обновление, удаление авторов
    *   **CRUD для постов** — создание, чтение, обновление, удаление постов
    *   **Связь один-ко-многим** — каждый пост принадлежит одному автору
    *   **Автогенерация документации** — эта страница создана автоматически

    ### 🔗 Эндпоинты API
    Все эндпоинты имеют префикс **`/api/v1`**.
    """,
    version="1.0.0",
    docs_url=None,  # Отключаем стандартный /docs
    redoc_url=None, # Отключаем стандартный /redoc
)

# ============ Кастомная OpenAPI схема и UI ============
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title + " - OpenAPI",
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=app.title + " - Swagger UI",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "docExpansion": "none",
            "filter": True,
            "displayRequestDuration": True,
            "tryItOutEnabled": True,
        }
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=app.title + " - ReDoc"
    )

@app.get("/openapi.json", include_in_schema=False)
async def openapi():
    return app.openapi()


origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from .routers import authors, posts  # Используем относительный импорт

app.include_router(authors.router, prefix="/api/v1", tags=["authors"])
app.include_router(posts.router, prefix="/api/v1", tags=["posts"])

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root():
    return {"message": "Добро пожаловать в ZachetDB Blog API! Перейдите на /docs для документации."}
