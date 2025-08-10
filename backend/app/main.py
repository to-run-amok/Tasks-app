from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth_routes, todo_routes

app = FastAPI(title="ToDo List API with Firebase Auth")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_routes.router)
app.include_router(todo_routes.router)

@app.get("/")
async def root():
    return {"message": "API is running"}
