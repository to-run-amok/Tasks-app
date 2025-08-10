from app.config import db

def create_todo_for_user(uid: str, title: str):
    doc_ref = db.collection("todos").document()
    todo_data = {
        "id": doc_ref.id,
        "title": title,
        "completed": False,
        "user_id": uid
    }
    doc_ref.set(todo_data)
    return todo_data

def get_todos_for_user(uid: str):
    todos = db.collection("todos").where("user_id", "==", uid).stream()
    return [t.to_dict() for t in todos]

def update_todo_for_user(uid: str, todo_id: str, update_data: dict):
    doc_ref = db.collection("todos").document(todo_id)
    doc = doc_ref.get()
    if not doc.exists or doc.to_dict().get("user_id") != uid:
        return None
    doc_ref.update(update_data)
    return doc_ref.get().to_dict()

def delete_todo_for_user(uid: str, todo_id: str):
    doc_ref = db.collection("todos").document(todo_id)
    doc = doc_ref.get()
    if not doc.exists or doc.to_dict().get("user_id") != uid:
        return False
    doc_ref.delete()
    return True
