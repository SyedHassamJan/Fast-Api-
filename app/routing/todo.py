from fastapi import APIRouter , Depends
from app.models.todo import CreateTodo, TodoResponse
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.schema.todo_schema import TodoSchema
from sqlalchemy import select
from app.dependencies import authenticate_user

router = APIRouter(prefix="/todo", dependencies=[Depends(authenticate_user)])
@router.get("/")
def index(db:Annotated[Session, Depends(get_db)]):
    stmt = select(TodoSchema.id, TodoSchema.content, TodoSchema.is_completed)

    todos=db.execute(stmt).mappings().all()
    return {"message": "This is a list of todos", "todos": todos}


@router.get("/{id}")
def show(id:int, db:Annotated[Session, Depends(get_db)]):
   todo = db.query(TodoSchema).filter(TodoSchema.id == id).first()
   return {"message": "This is a single todo", "todo": todo}

@router.post("/", response_model=TodoResponse)
def store(item: CreateTodo, db: Annotated[Session, Depends(get_db)]):
    todo = TodoSchema(content=item.content, is_completed=item.is_completed)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo 

@router.put("/{id}")
def update(id:int, item: CreateTodo, db:Annotated[Session, Depends(get_db)]):
    todo = db.query(TodoSchema).filter(TodoSchema.id == id).first()
    if not todo:
        return {"message": "Todo not found"}
    todo.content = item.content
    todo.is_completed = item.is_completed
    db.commit()
    db.refresh(todo)
    return {"message": "Todo updated successfully", "todo": todo}

@router.delete("/{id}")
def delete(id:int, db:Annotated[Session, Depends(get_db)]):
    todo = db.query(TodoSchema).filter(TodoSchema.id == id).first()
    if not todo:
        return {"message": "Todo not found"}
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}
