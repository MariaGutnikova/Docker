FROM python:3.9-slim

WORKDIR /app

# Сначала копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Потом код (под root)
COPY app.py .

# Создаём пользователя
RUN useradd -u 1000 -m appuser

# Даем права
RUN chown -R appuser:appuser /app

# Переключаемся
USER appuser

# Переменные
ENV DATA_PATH=/data/hr_data.csv
ENV OUTPUT_PATH=/output/chart.png

CMD ["python", "app.py"]
