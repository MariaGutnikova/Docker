# Отчет по лабораторной работе №3
## Тема: Развертывание приложения в Kubernetes
**Студент:** [ФИО]  
**Группа:** [Группа]  
**Вариант:** 2 (PostgreSQL + Adminer)

---

### 1. Цель работы
Освоить процесс оркестрации контейнеров. Научиться разворачивать связки сервисов (аналитическое приложение + база данных/интерфейс) в кластере Kubernetes, управлять их масштабированием (Deployment) и сетевой доступностью (Service).

### 2. Задание (Вариант 2)
Развернуть базу данных **PostgreSQL** и веб-интерфейс **Adminer**. Настроить Adminer на подключение к сервису Postgres. Открыть доступ к Adminer в браузере.

---

### 3. Ход выполнения

#### 3.1. Подготовка манифестов
Для выполнения работы были созданы следующие манифесты:
1. `secrets.yaml` — для безопасного хранения пароля БД.
2. `db-deployment.yaml` — для развертывания PostgreSQL.
3. `adminer-deployment.yaml` — для развертывания веб-интерфейса Adminer.
4. `services.yaml` — для описания сетевых интерфейсов доступа.

#### 3.2. Листинг и пояснение YAML-файлов

**1. Секреты (`secrets.yaml`)**
Мы закодировали пароль `postgres` в Base64 (`cG9zdGdyZXM=`) и поместили его в секрет.
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
type: Opaque
data:
  postgres-password: cG9zdGdyZXM=
```

**2. База данных PostgreSQL (`db-deployment.yaml`)**
Мы используем официальный образ `postgres:15`. Пароль передается через переменные окружения из секрета.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres-db
  labels:
    app: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15 # Образ PostgreSQL
        ports:
        - containerPort: 5432 # Стандартный порт PostgreSQL
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: postgres-password
```

**3. Приложение Adminer (`adminer-deployment.yaml`)**
Adminer будет использоваться для управления БД через браузер.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: adminer-ui
  labels:
    app: adminer
spec:
  replicas: 1
  selector:
    matchLabels:
      app: adminer
  template:
    metadata:
      labels:
        app: adminer
    spec:
      containers:
      - name: adminer
        image: adminer:latest # Последний образ Adminer
        ports:
        - containerPort: 8080 # Внутренний порт Adminer
```

**4. Сетевые сервисы (`services.yaml`)**
- `postgres-service`: тип `ClusterIP`, обеспечивает внутреннюю доступность БД по имени `postgres-service`.
- `adminer-service`: тип `NodePort`, открывает доступ к веб-интерфейсу на порту `30080`.
```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
spec:
  selector:
    app: postgres
  ports:
    - port: 5432
      targetPort: 5432
  type: ClusterIP # Внутренний IP для доступа из Adminer
---
apiVersion: v1
kind: Service
metadata:
  name: adminer-service
spec:
  selector:
    app: adminer
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30080 # Внешний порт для доступа из браузера
  type: NodePort
```

---

### 4. Результаты (скриншоты)

#### 4.1. Проверка состояния подов
Команда `kubectl get pods` показывает, что все компоненты запущенны и работают корректно.
*(Сюда вставьте скриншот `kubectl get pods`)*
![kubectl get pods](img/pods_running.png)

#### 4.2. Проверка сервисов
Команда `kubectl get services` показывает открытые порты.
*(Сюда вставьте скриншот `kubectl get services`)*
![kubectl get services](img/services_status.png)

#### 4.3. Веб-интерфейс Adminer
После перехода по адресу `http://<IP-ВМ>:30080` мы видим страницу входа. Для подключения используем:
- **System:** PostgreSQL
- **Server:** `postgres-service` (имя нашего сервиса)
- **User:** postgres
- **Password:** postgres

*(Сюда вставьте скриншот интерфейса Adminer с успешным подключением)*
![Adminer Connect](img/adminer_connected.png)

---

### 5. Выводы
В ходе работы был освоен процесс оркестрации контейнеров с помощью Kubernetes. Были созданы и запущены Deployment для базы данных и управляющего интерфейса, что позволило гибко управлять их жизненным циклом. Использование `Service` (NodePort и ClusterIP) обеспечило как внутреннюю связь между компонентами (Adminer -> Postgres), так и внешнюю доступность для пользователя. Декларативный подход Kubernetes значительно упрощает развертывание сложных аналитических систем.
