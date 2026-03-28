# Лабораторная работа №2. Создание Docker-образа для HR-аналитики

**Вариант 2** — HR & Retention (Тема 2)  
**Стек технологий** — Python (Pandas + Matplotlib) + Docker  
**Задание** — Скрипт генерирует временной ряд удовлетворенности сотрудников, строит линейный график и сохраняет его как `chart.png`.

---

## 1. Описание задачи
**Предметная область:** HR-менеджмент и удержание персонала.  
**Бизнес-метрика:** Анализ динамики уровня удовлетворенности сотрудников в зависимости от даты их приема на работу. Это позволяет выявить периоды найма "наименее вовлеченных" сотрудников и скорректировать процессы адаптации.

**Используемые данные:** 500 синтетических записей.
- `employee_id`: ID сотрудника.
- `age`: Возраст (20–60 лет).
- `salary_usd`: Зарплата.
- `satisfaction_level`: Уровень удовлетворенности (0.0–1.0).
- `hire_date`: Дата найма (за последние 2 года).

---

Структура проекта

docker2/
├── app/
│   ├── Dockerfile            # Многоэтапная сборка (styled)
│   ├── .dockerignore         # Исключения сборки
│   ├── requirements.txt
│   └── app.py     
├── data/
│   └── hr_data.csv      # Сгенерированные данные
├── .env                      # Переменные окружения
├── docker-compose.yml        # Оркестрация сервиса
└── generate_data.py          # Генератор данных (Python)


## 2. Листинг кода

### 2.1 Генератор данных (`generate_data.py`)
Скрипт создает CSV-файл с детальной информацией о сотрудниках. Использование `numpy.random` обеспечивает реалистичное распределение.

### 2.2 Аналитический скрипт (`app/app.py`)
Скрипт читает CSV, преобразует даты, рассчитывает скользящее среднее (resample по месяцам) и строит визуализацию.

### 2.3 Dockerfile
```dockerfile
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
]
```
---

## 3. Сборка и запуск

### Шаг 1: Генерация данных
```bash
python generate_data.py
```
<img width="1479" height="176" alt="image" src="https://github.com/user-attachments/assets/7afac4e0-4aca-436a-b985-368c7feeee02" />

### Шаг 2: Сборка образа
```bash
docker compose build
```
<img width="1348" height="878" alt="image" src="https://github.com/user-attachments/assets/ee81b5ad-8698-4c9e-a6f4-2b061abac4ef" />

### Шаг 3: Запуск и получение результата
```bash
docker compose up
```
<img width="1286" height="877" alt="image" src="https://github.com/user-attachments/assets/7345c85d-6391-48d8-a854-4785a2b31549" />

<img width="1284" height="878" alt="image" src="https://github.com/user-attachments/assets/bb2d0561-3bf0-4973-a69c-2570c60cf189" />


---

## 5. Вывод
В ходе работы был разработан контейнеризированный инструмент для анализа HR-метрик. Использование Docker позволило упаковать зависимости и обеспечить повторяемость результатов независимо от окружения хоста. Файл-график успешно сохраняется на хост-машину через volume (монтируемую папку).
