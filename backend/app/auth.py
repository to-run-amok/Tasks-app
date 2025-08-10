from firebase_admin import auth as admin_auth
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Verify Firebase ID token and return the user UID.
    Raises HTTP 401 if verification fails.
    """
    try:
        decoded_token = admin_auth.verify_id_token(token)
        return decoded_token["uid"]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
