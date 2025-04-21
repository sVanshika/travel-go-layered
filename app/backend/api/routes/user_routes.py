from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from services.user_service import UserService
from models.userModel import UserProfileUpdate, UserProfileResponse
from services.auth_service import AuthService
from typing import Optional

router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService()
auth_service = AuthService()

async def get_current_user(token: str = Depends(auth_service.verify_token)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return token

@router.put("/profile", response_model=UserProfileResponse)
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: dict = Depends(auth_service.get_current_user)
):
    """
    Update the current user's profile
    """
    try:
        return await user_service.update_profile(current_user["uid"], profile_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/profile/image", response_model=dict)
async def upload_profile_image(
    image: UploadFile = File(...),
    current_user: dict = Depends(auth_service.get_current_user)
):
    """
    Upload a profile image for the current user
    """
    try:
        image_url = await user_service.upload_profile_image(current_user["uid"], image)
        return {"imageUrl": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profile", response_model=UserProfileResponse)
async def get_profile(
    current_user: dict = Depends(auth_service.get_current_user)
):
    """
    Get the current user's profile
    """
    try:
        return await user_service.get_profile(current_user["uid"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 