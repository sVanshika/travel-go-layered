from fastapi import APIRouter, Depends, HTTPException, Query
from services.trip_service import TripService
from models.tripModel import TripCreate, TripResponse
# from backend.services.auth_service import AuthService
from typing import List

router = APIRouter(prefix="/trip")
trip_service = TripService()
# auth_service = AuthService()

# async def get_current_user(token: str = Depends(auth_service.verify_token)):
#     if not token:
#         raise HTTPException(status_code=401, detail="Not authenticated")
#     return token

# @router.post("/", response_model=TripResponse)
# async def create_trip(
#     trip_data: TripCreate,
#     current_user: dict = Depends(get_current_user)
# ):
#     """
#     Create a new trip for the current user
#     """
#     return await trip_service.create_trip(current_user["uid"], trip_data)

# @router.get("/", response_model=List[TripResponse])
# async def get_trips(current_user: dict = Depends(get_current_user)):
#     """
#     Get all trips for the current user
#     """
#     return await trip_service.get_user_trips(current_user["uid"]) 

@router.get("/my-trips")
async def get_user_trips(user_id: str = Query(...)):
    """
    Fetch trips for a specific user.
    """
    try:
        # Fetch trips from your database or Firestore based on user_id
        print("/trip/my-trips inoked")
        trips = await trip_service.get_user_trips(user_id)
        print("------------------------------------------")
        print(trips)
        return trips
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
