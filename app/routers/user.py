from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # сессия базы данных
from app.backend.db_depends import get_db  # функция подключения к базе данных
from app.models import User, Task
from app.schemes import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete  # функции работы с записями
from slugify import slugify  # функция создания slug-строки
from typing import Annotated, Sequence

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    db.commit()
    return users


@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    else:
        db.commit()
        return user


@router.get("/user_id/tasks")
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
        db.commit()
        return tasks
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )


@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], model: CreateUser):
    db.execute(insert(User).values(
        username=model.username,
        firstname=model.firstname,
        lastname=model.lastname,
        age=model.age,
        slug=slugify(model.username)))
    db.commit()
    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Successful"
    }


@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], model: UpdateUser, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )

    db.execute(update(User).where(User.id == user_id).values(
        firstname=model.firstname,
        lastname=model.lastname,
        age=model.age
    ))
    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "User update is successful!"
    }


@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    else:
        db.execute(delete(Task).where(Task.user_id == user_id))
        db.execute(delete(User).where(User.id == user_id))
        db.commit()
        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "User was deleted"
        }
