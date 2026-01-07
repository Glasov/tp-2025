FROM python:3.9-slim

WORKDIR /app

# Устанавливаем зависимости
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY backend/ .

# Создаем пользователя для безопасности
RUN useradd -m -u 1000 studentuser
USER studentuser

# Запускаем приложение
EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]