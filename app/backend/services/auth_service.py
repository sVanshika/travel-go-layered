from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.firebase import create_user, verify_firebase_token
from models.authModel import SignupRequest, LoginRequest, UserResponse, TokenResponse
import requests
import os

security = HTTPBearer()

class AuthService:
    def __init__(self):
        self.firebase_api_key = os.getenv("FIREBASE_API_KEY")

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials
        user = verify_firebase_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    async def register_user(self, name: str, email: str, password: str):
        try:
            return create_user(name, email, password)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def signup(self, request: SignupRequest) -> UserResponse:
        """
        Service layer method to handle user signup
        """
        try:
            user_data = create_user(request.name, request.email, request.password)
            return UserResponse(
                name=user_data["name"],
                email=user_data["email"],
                uid=user_data["uid"]
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def login(self, request: LoginRequest) -> TokenResponse:
        """
        Service layer method to handle user login
        """
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.firebase_api_key}"
        payload = {
            "email": request.email,
            "password": request.password,
            "returnSecureToken": True
        }
        
        try:
            res = requests.post(url, json=payload)
            data = res.json()

            print("aut_service - data")
            print(data)

            if "idToken" not in data:
                raise HTTPException(status_code=400, detail="Invalid credentials")

            return TokenResponse(id_token=data["idToken"], local_id=data["localId"])
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def verify_token(self, token: str) -> UserResponse:
        """
        Service layer method to verify Firebase token
        """
        try:
            user_data = verify_firebase_token(token)
            if not user_data:
                raise HTTPException(status_code=401, detail="Invalid token")
            
            return UserResponse(
                name=user_data["name"],
                email=user_data["email"],
                uid=user_data["uid"]
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
