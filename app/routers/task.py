from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # сессия базы данных
from app.backend.db_depends import get_db  # функция подключения к базе данных
from app.models import Task, User
from app.schemes import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete  # функции работы с записями
from slugify import slugify  # функция создания slug-строки
from typing import Annotated, Sequence

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    db.commit()
    return tasks


@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    else:
        db.commit()
        return task


@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], model: CreateTask, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        db.execute(insert(Task).values(
            title=model.title,
            content=model.content,
            priority=model.priority,
            user_id=user_id,
            slug=slugify(model.title)))
        db.commit()
        return {
            "status_code": status.HTTP_201_CREATED,
            "transaction": "Successful"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )


@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], model: UpdateTask, task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )

    db.execute(update(Task).where(Task.id == task_id).values(
        title=model.title,
        content=model.content,
        priority=model.priority
    ))
    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Task update is successful!"
    }


@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    user = db.scalar(select(Task).where(Task.id == task_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    else:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "Task was deleted"
        }
