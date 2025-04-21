from fastapi import APIRouter, HTTPException, Response, Request, Depends, Cookie
from services.auth_service import AuthService
from models.authModel import SignupRequest, LoginRequest, UserResponse, TokenResponse
from datetime import datetime, timedelta

router = APIRouter()
auth_service = AuthService()

@router.post("/signup", response_model=UserResponse)  
async def signup(user: SignupRequest):
    """
    Signup Endpoint: Creates a new user in Firebase Authentication.
    """
    return await auth_service.signup(user)

@router.post("/login", response_model=TokenResponse)
async def login(user: LoginRequest, response: Response):
    result = await auth_service.login(user)
    
    # Set cookie
    response.set_cookie(
        key="session_token",
        value=result.id_token,
        httponly=True,
        # secure=True,
        secure=False,
        samesite="None"
    )
    response.set_cookie(
        key="local_id",
        value=result.local_id,
        httponly=False,
        # secure=True,
        secure=True,
        samesite="Lax"
    )
    print("-> login result: ")
    print(result)
    return result

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("session_token")
    return {"message": "Logged out successfully"}

@router.get("/protected", response_model=UserResponse)
async def protected_route(session_token: str = Cookie(None)):
    print("-> /protected session token:")
    print(session_token)
    # if not session_token:
    #     raise HTTPException(status_code=401, detail="Not authenticated")

    return await auth_service.verify_token(session_token)
