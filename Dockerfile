# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /programas/api-microservicio1

# Copia el archivo de requisitos si lo tienes, o simplemente instala las dependencias necesarias directamente
# Aquí instalamos mysql-connector-python y FastAPI

RUN pip3 install fastapi[all] mysql-connector-python

# Copia el contenido del proyecto actual al contenedor
COPY . .

# Exponer el puerto en el que correrá la aplicación dentro del contenedor (8001)
EXPOSE 8001

# Comando para correr la aplicación cuando el contenedor inicie
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
