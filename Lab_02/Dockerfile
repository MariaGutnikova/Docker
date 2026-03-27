FROM python:3.9-slim

WORKDIR /app

# Копируем зависимости отдельно для кэширования слоев
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Безопасность: не работаем под root
RUN useradd -u 1000 -m appuser
USER appuser

# Копируем код
COPY app.py .

# Переменные пути по умолчанию
ENV DATA_PATH=/data/hr_data.csv
ENV OUTPUT_PATH=/output/chart.png

CMD ["python", "app.py"]
