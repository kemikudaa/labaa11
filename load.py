import csv
from sqlmodel import Session
from books import Book, engine, create_db_and_tables

def load_books():
    with open("goodbooks-10k/books.csv", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        create_db_and_tables()
        with Session(engine) as session:
            for row in reader:
                try:
                    book = Book(
                        id=int(row["book_id"]),
                        title=row["title"],
                        authors=row["authors"],
                        publication_year=int(float(row["original_publication_year"])),
                        image_url=row["image_url"],
                    )
                    session.add(book)
                except:
                    continue
            session.commit()

if __name__ == "_main_":
    load_books()