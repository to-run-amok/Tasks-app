from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from firebase_admin import auth as admin_auth
from app.config import firebase
from app.models import SignUpschema, Loginschema


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_data: SignUpschema):
    try:
        user = admin_auth.create_user(email=user_data.email, password=user_data.password)
        return JSONResponse(content={"message": f"User {user.uid} created successfully"}, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Signup failed: {e}")

@router.post("/login")
async def login(user_data: Loginschema):
    """
    Sign in using pyrebase (Firebase client). Requires FIREBASE_* env variables to be set.
    Returns an ID token (idToken) on success.
    """
    if firebase is None:
        raise HTTPException(status_code=500, detail="Server not configured for client auth. Set FIREBASE_API_KEY and related env vars.")
    try:
        auth_client = firebase.auth()
        user = auth_client.sign_in_with_email_and_password(user_data.email, user_data.password)
        token = user.get("idToken")
        return {"token": token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Login failed: {e}")
