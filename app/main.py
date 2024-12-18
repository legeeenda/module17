from fastapi import FastAPI
from app.routers import task, user

app = FastAPI()

# ЗАПУСК ФАЙЛА
# вариант 1: $ fastapi dev app/main.py
# вариант 2: $ uvicorn app.main:app --reload
# unicorn <путь к файлу>:<ссылка на объект FastAPI> --reload - опция автоматического перезапуска сервера при изменении кода

# ПОДГОТОВКА МИГРАЦИИ
# 1. $ alembic init app/migrations  - создание папки миграции
# 2. в файле alembic.ini прописать: sqlalchemy.url = sqlite:///taskmanager.db
# 3. в файле env.py прописать:  from app.backend.db import Base
#                               from app.models.task import Task
#                               from app.models.user import User
#                               target_metadata = Base.metadata
# 4. $ alembic revision --autogenerate -m "Initial migration"  - генерация базы данных
# 5. $ alembic upgrade head  - применение последней миграции и создание таблиц User, Task и запись текущей версии миграции

@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}

# позволяет подключать дополнительные внешние роуты, и легко масштабировать приложение
app.include_router(task.router)
app.include_router(user.router)