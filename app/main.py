from fastapi import FastAPI
from app.routers import task, user

app = FastAPI()


@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}

# позволяет подключать дополнительные внешние роуты, и легко масштабировать приложение
app.include_router(task.router)
app.include_router(user.router)