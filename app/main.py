from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from app import models, schemas, crud, database

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=database.engine)

@app.get("/tasks", response_model=List[schemas.Task])
async def get_tasks():
    return await crud.get_tasks()

@app.post("/tasks", response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate):
    return await crud.create_task(task)

@app.put("/tasks/{task_id}", response_model=schemas.Task)
async def update_task(task_id: int, task: schemas.TaskUpdate):
    updated_task = await crud.update_task(task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    success = await crud.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}
