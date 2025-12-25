from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL: 
    DATABASE_URL = "sqlite:///./test.db"
    print("⚠️  DATABASE_URL не найден в окружении. Используется SQLite.")
else:  
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        print("🔧  Исправлен формат URL с postgres:// на postgresql://")
    print(f"✅  Используется DATABASE_URL из окружения Render")
try:
    engine = create_engine(DATABASE_URL)
    print("✅  Движок базы данных успешно создан")
except Exception as e:
    print(f"❌  Ошибка создания движка БД: {e}")
   
    print("🔄  Переключаемся на SQLite для возможности запуска...")
    DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

print("🎯  Модуль database.py успешно инициализирован")
