from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_current_user
from app.config import db
from app.models import ToDoCreate, ToDoUpdate
from typing import List
import firestore
router = APIRouter(prefix="/tasks", tags=["ToDo"])

@router.get("/", response_model=List[dict])
async def get_tasks(uid: str = Depends(get_current_user)):
    todos_ref = db.collection("users").document(uid).collection("tasks")
    docs = todos_ref.stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_data: ToDoCreate, uid: str = Depends(get_current_user)):
    new_todo_ref = db.collection("users").document(uid).collection("tasks").document()
    new_todo_ref.set({
        "task": todo_data.task,
        "completed": todo_data.completed,
        "timestamp": getattr(todo_data, "timestamp", None) or firestore.SERVER_TIMESTAMP
    })
    return {"message": "To-Do created successfully", "id": new_todo_ref.id}


@router.delete("/{task_id}")
async def delete_task(task_id: str, uid: str = Depends(get_current_user)):
    task_ref = db.collection("users").document(uid).collection("tasks").document(task_id)
    if not task_ref.get().exists:
        raise HTTPException(status_code=404, detail="Task not found")
    task_ref.delete()
    return {"message": "Task deleted"}

@router.patch("/{task_id}")
async def update_task(task_id: str, todo: ToDoUpdate, uid: str = Depends(get_current_user)):
    task_ref = db.collection("users").document(uid).collection("tasks").document(task_id)
    if not task_ref.get().exists:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = {k: v for k, v in todo.dict().items() if v is not None}
    task_ref.update(update_data)
    return {"id": task_id, **update_data}
