import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Настройка генератора
np.random.seed(42)
N = 500

# Генерация данных
start_date = datetime(2022, 1, 1)
data = {
    "employee_id": range(1, N + 1),
    "age": np.random.randint(20, 60, N),
    "experience_years": np.random.randint(0, 20, N),
    "salary_usd": np.random.uniform(3000, 12000, N).round(2),
    "satisfaction_level": np.random.uniform(0.1, 1.0, N).round(2),
    "left_company": np.random.choice([0, 1], N, p=[0.8, 0.2]),
    # Генерируем даты приема на работу за последние 24 месяца
    "hire_date": [start_date + timedelta(days=np.random.randint(0, 730)) for _ in range(N)]
}

df = pd.DataFrame(data)
df = df.sort_values("hire_date")

# Создаем папку для данных
os.makedirs("data", exist_ok=True)
output_path = os.path.join("data", "hr_data.csv")
df.to_csv(output_path, index=False)

print(f"[✓] Датасет HR сгенерирован: {output_path} ({N} строк)")
print(df.head(3).to_string(index=False))
