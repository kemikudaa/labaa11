from fastapi import FastAPI, HTTPException, Query
from typing import List
from sqlmodel import SQLModel, Field, create_engine, Session, select

class Book(SQLModel, table=True):
    book_id: int = Field(primary_key=True)
    title: str
    authors: str
    original_publication_year: int
    image_url: str

DATABASE_URL = "sqlite:///books.db"
engine = create_engine(DATABASE_URL, echo=False)

# Инициализация таблицы
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
# Создание FastAPI-приложения
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# TODO: Исправьте код для получения данных книги по ID
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Книга не найдена")
        return book


# TODO: Исправьте код для получения списка книг по страницам
@app.get("/books/", response_model=List[Book])
def list_books(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    with Session(engine) as session:
        books = session.exec(
            select(Book).offset(offset).limit(limit)
        ).all()
        return books
