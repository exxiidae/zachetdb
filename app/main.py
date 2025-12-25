from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi


app = FastAPI(
    title="ZachetDB API",
    description="""
    ## Документация API для проекта ZachetDB
    
    Это FullStack приложение на FastAPI, которое управляет сущностями "Авторы" и "Посты".
    
    ### Основные возможности:
    * **CRUD-операции** для авторов и постов
    * **Автоматическая документация** в формате OpenAPI
    * **Поддержка PostgreSQL** через SQLAlchemy ORM
    
    ### Маршруты API:
    * `/api/v1/authors` — управление авторами
    * `/api/v1/posts` — управление постами
    """,
    version="1.0.0",
    docs_url=None,  # Отключаем стандартный /docs
    redoc_url=None, # Отключаем стандартный /redoc
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
            "defaultModelsExpandDepth": -1,
            "filter": True,
            "displayRequestDuration": True,
            "tryItOutEnabled": True,
            "syntaxHighlight.theme": "monokai",
        }
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


from app.routers import authors, posts

app.include_router(authors.router, prefix="/api/v1", tags=["authors"])
app.include_router(posts.router, prefix="/api/v1", tags=["posts"])


from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")


from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
