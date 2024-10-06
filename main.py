from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel
from typing import List

# --- Configuración de la base de datos ---
host_name = "98.83.69.254"  # Cambiar según sea necesario
port_number = "8005"  # Cambiar según sea necesario
user_name = "root"  # Cambiar según sea necesario
password_db = "utec"  # Cambiar según sea necesario
database_name = "mysql_microservicio1"  # Cambiar según sea necesario

app = FastAPI()


# --- Rutas ---
# Obtener todos los libros
@app.get("/books/")
def obtener_todos_los_libros():
    try:
        # Conexión a la base de datos
        mydb = mysql.connector.connect(
            host=host_name,
            port=port_number,
            user=user_name,
            password=password_db,
            database=database_name
        )
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM books")
        result = cursor.fetchall()
        cursor.close()
        mydb.close()
        # Devuelve los resultados
        return {"books": result}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error: {str(err)}")


# Obtener libros por el nombre del autor
@app.get("/books/by_author/{author_name}")
def obtener_libros_por_el_nombre_del_author(author_name: str):
    try:
        # Conexión a la base de datos
        mydb = mysql.connector.connect(
            host=host_name,
            port=port_number,
            user=user_name,
            password=password_db,
            database=database_name
        )
        cursor = mydb.cursor()
        # Busca al autor por nombre
        cursor.execute("SELECT id FROM authors WHERE name = %s", (author_name,))
        author_id = cursor.fetchone()
        if not author_id:
            raise HTTPException(status_code=404, detail="Author not found")

        # Busca libros asociados al autor
        cursor.execute("SELECT * FROM books WHERE author_id = %s", (author_id[0],))
        result = cursor.fetchall()
        cursor.close()
        mydb.close()
        # Devuelve los resultados
        return {"books": result}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error: {str(err)}")


# Obtener book_id por título del libro y nombre del autor
@app.get("/books/get_book_id")
def obtener_book_id_por_title_y_author(title: str, author_name: str):
    try:
        # Conexión a la base de datos
        mydb = mysql.connector.connect(
            host=host_name,
            port=port_number,
            user=user_name,
            password=password_db,
            database=database_name
        )
        cursor = mydb.cursor()
        # Paso 1: Obtener el author_id a partir del nombre del autor
        cursor.execute("SELECT id FROM authors WHERE name = %s", (author_name,))
        author_id = cursor.fetchone()
        if not author_id:
            raise HTTPException(status_code=404, detail="Author not found")

        # Paso 2: Usar el author_id y el title del libro para obtener el book_id
        cursor.execute("SELECT id FROM books WHERE title = %s AND author_id = %s", (title, author_id[0]))
        book_id = cursor.fetchone()
        if not book_id:
            raise HTTPException(status_code=404, detail="Book not found")

        cursor.close()
        mydb.close()

        # Devolver el book_id
        return {"book_id": book_id[0]}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error: {str(err)}")


# Nueva API: Obtener title y author_name por book_id
@app.get("/books/{book_id}/details")
def obtener_detalles_por_book_id(book_id: int):
    try:
        # Conexión a la base de datos
        mydb = mysql.connector.connect(
            host=host_name,
            port=port_number,
            user=user_name,
            password=password_db,
            database=database_name
        )
        cursor = mydb.cursor()

        # Paso 1: Obtener el title y author_id del libro a partir del book_id
        cursor.execute("SELECT title, author_id FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        title = book[0]
        author_id = book[1]

        # Paso 2: Obtener el nombre del autor a partir del author_id
        cursor.execute("SELECT name FROM authors WHERE id = %s", (author_id,))
        author = cursor.fetchone()
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")

        author_name = author[0]

        cursor.close()
        mydb.close()

        # Devolver el title del libro y el name del autor
        return {"title": title, "author_name": author_name}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error: {str(err)}")

# Nueva API: Obtener author_id por name del author
@app.get("/authors/get_author_id/")
def obtener_author_id_por_name(author_name: str):
    try:
        # Conexión a la base de datos
        mydb = mysql.connector.connect(
            host=host_name,
            port=port_number,
            user=user_name,
            password=password_db,
            database=database_name
        )
        cursor = mydb.cursor()

        # Buscar el author_id basado en el nombre del autor
        cursor.execute("SELECT id FROM authors WHERE name = %s", (author_name,))
        author_id = cursor.fetchone()
        if not author_id:
            raise HTTPException(status_code=404, detail="Author not found")

        cursor.close()
        mydb.close()

        # Devolver el author_id
        return {"author_id": author_id[0]}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error: {str(err)}")


# Esquema para los libros (books)
class BookBase(BaseModel):
    title: str
    author_id: int

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


# Esquema para los autores (authors)
class AuthorBase(BaseModel):
    name: str

class Author(AuthorBase):
    id: int
    books: List[Book] = []

    class Config:
        orm_mode = True
