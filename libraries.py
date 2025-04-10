from fastapi import FastAPI, HTTPException, Query
from typing import List
from sqlmodel import SQLModel, Field, create_engine, Session, select

# Модель данных о наличии книги в филиале
class BookAvailability(SQLModel, table=True):
    id: int = Field(primary_key=True)
    book_id: int
    branch_name: str
    available_copies: int

# Настройка подключения к базе данных SQLite
DATABASE_URL = "sqlite:///library.db"
engine = create_engine(DATABASE_URL, echo=False)


# Функция для создания таблиц в базе данных
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

# Инициализация базы данных при старте приложения
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# CRUD операции


# Получение информации о наличии книги в определённом филиале
@app.get("/availability/{book_id}", response_model=List[BookAvailability])
def get_book_availability(book_id: int):
    with Session(engine) as session:
        availability = session.exec(select(BookAvailability).filter(BookAvailability.book_id == book_id)).all()
        if not availability:
            raise HTTPException(status_code=404, detail="Нет информации о наличии книги с таким ID")
        return availability


# Добавление данных о наличии книги в филиал
@app.post("/availability/", response_model=BookAvailability)
def add_book_availability(availability: BookAvailability):
    with Session(engine) as session:
        # Проверка, есть ли уже данные о наличии этой книги в указанном филиале
        existing = session.exec(
            select(BookAvailability).filter(
                BookAvailability.book_id == availability.book_id,
                BookAvailability.branch_name == availability.branch_name
            )
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Данные для этого филиала уже существуют.")
        
        session.add(availability)
        session.commit()
        session.refresh(availability)
        return availability


# Обновление количества экземпляров книги в филиале
@app.put("/availability/{book_id}/{branch_name}", response_model=BookAvailability)
def update_book_availability(book_id: int, branch_name: str, available_copies: int):
    with Session(engine) as session:
        availability = session.exec(
            select(BookAvailability).filter(
                BookAvailability.book_id == book_id,
                BookAvailability.branch_name == branch_name
            )
        ).first()
        if not availability:
            raise HTTPException(status_code=404, detail="Данные о наличии книги не найдены.")
        
        availability.available_copies = available_copies
        session.commit()
        session.refresh(availability)
        return availability
