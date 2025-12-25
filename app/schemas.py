from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# ===== СХЕМЫ ДЛЯ АВТОРОВ =====
class AuthorBase(BaseModel):
    name: str
    email: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  


class PostBase(BaseModel):
    title: str
    content: str
    author_id: int

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    author: Optional[Author] = None  

    class Config:
        from_attributes = True
