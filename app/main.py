from fastapi import FastAPI, HTTPException
from app import models, schemas, crud, database
import uvicorn

app = FastAPI()

models.metadata.create_all(database.engine)

@app.on_event("startup")
async def startup():
    await database.database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.database.disconnect()

@app.get("/tasks/", response_model=list[schemas.Task])
async def read_tasks():
    return await crud.get_tasks()

@app.get("/tasks/{task_id}", response_model=schemas.Task)
async def read_task(task_id: int):
    task = await crud.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks/", response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate):
    return await crud.create_task(task)

@app.put("/tasks/{task_id}", response_model=schemas.Task)
async def update_task(task_id: int, task: schemas.TaskCreate):
    db_task = await crud.get_task(task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return await crud.update_task(task_id, task)

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    await crud.delete_task(task_id)
    return {"message": "Task deleted"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
