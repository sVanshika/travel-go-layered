from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    name: str
    email: EmailStr
    uid: str

class TokenResponse(BaseModel):
    id_token: str
    message: str = "Login successful"
    local_id: str
