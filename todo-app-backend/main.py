from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreateSchema(BaseModel):
    title: str

tasks: list[TaskSchema] = []   

@app.get("/tasks")
def read_tasks() -> list[TaskSchema]:
    return tasks

@app.post("/tasks")
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)

    tasks.append(new_task)
    return new_task

# КНИГИ
class BookSchema(BaseModel):
    title: str

class BookCreateSchema(BaseModel):
    title: str

books: list[BookSchema] = []

@app.get("/books")
def get_books():
    return {"Любимая книга": books[-1].title}

@app.post("/books")
def add_book(payload: BookCreateSchema):
    new_book = BookSchema(title=payload.title)

    books.append(new_book)
    return {"message":f"Книга '{payload.title}' добавлена"}