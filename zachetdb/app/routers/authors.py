from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/authors", response_model=schemas.AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    # Проверка на существующего автора с таким email
    db_author = db.query(models.Author).filter(models.Author.email == author.email).first()
    if db_author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author with this email already exists"
        )
    
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author
