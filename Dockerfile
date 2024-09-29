FROM python:3.10-slim
WORKDIR /programas/api-microservicio1
RUN pip install fastapi uvicorn sqlalchemy pymysql
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]