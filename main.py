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
