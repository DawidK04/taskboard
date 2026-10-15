from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

TASKS: dict[int,dict] = {
    1: {"id": 1, "title": "Przygotować środowisko", "status": "done", "priority": "high"},
    2: {"id": 2, "title": "Przeczytać RFC 9110", "status": "open", "priority": "medium"},
}

NEXT_ID = 3

class TaskIn(BaseModel):
    title: str
    status: str = "open"
    priority: str = "medium"

app = FastAPI(title="TaskBoard")

@app.get("/")
def root():
    return {"message": "Hello Web"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def list_tasks():
    return {"items": list(TASKS.values()), "total": len(TASKS)}

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = TASKS.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Zadanie nie istnieje")
    return task

@app.get("/tasks")
def list_tasks(status: str | None = None, limit: int = 20):
    items = list(TASKS.values())
    if status is not None:
        items = [t for t in items if t["status"] == status]
    return {"items": items[:limit], "total": len(items)}

@app.post("/tasks", status_code=201)
def create_task(payload: TaskIn, response: Response):
    response.headers["Location"] = f"/tasks/{NEXT_ID}"
    task = ""
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Zadanie nie istnieje")
    del TASKS[task_id]
