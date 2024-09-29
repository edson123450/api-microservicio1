from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

app = FastAPI()

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)


# Ruta para obtener todos los libros
@app.get("/books/", response_model=list[schemas.Book])
def obtener_todos_los_libros(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books


# Ruta para obtener libros por el nombre del autor
@app.get("/books/by_author/{author_name}", response_model=list[schemas.Book])
def obtener_libros_por_el_nombre_del_author(author_name: str, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.name == author_name).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    books = db.query(models.Book).filter(models.Book.author_id == author.id).all()
    return books