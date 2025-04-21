from core.firebase import update_user_profile, upload_profile_image, get_user_profile
from models.userModel import UserProfileUpdate, UserProfileResponse
from fastapi import HTTPException, UploadFile
from typing import Optional
from datetime import datetime

class UserService:
    async def update_profile(self, user_id: str, profile_data: UserProfileUpdate) -> UserProfileResponse:
        """
        Updates a user's profile
        """
        try:
            # Convert Pydantic model to dict and exclude unset values
            update_data = profile_data.model_dump(exclude_unset=True)
            
            # Add timestamps
            update_data["updatedAt"] = datetime.now().isoformat()
            
            # Update profile in Firestore
            updated_profile = update_user_profile(user_id, update_data)
            return UserProfileResponse(**updated_profile)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def upload_profile_image(self, user_id: str, image_file: UploadFile) -> str:
        """
        Uploads a profile image and returns the URL
        """
        try:
            # Read the image file
            image_data = await image_file.read()
            content_type = image_file.content_type or "image/jpeg"
            
            # Upload to Firebase Storage
            image_url = upload_profile_image(user_id, image_data, content_type)
            
            # Update the user's profile with the new image URL
            await self.update_profile(user_id, UserProfileUpdate(profileImage=image_url))
            
            return image_url
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_profile(self, user_id: str) -> UserProfileResponse:
        """
        Gets a user's profile
        """
        try:
            profile_data = get_user_profile(user_id)
            if not profile_data:
                raise HTTPException(status_code=404, detail="Profile not found")
            return UserProfileResponse(**profile_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 