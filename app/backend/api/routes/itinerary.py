from fastapi import APIRouter, HTTPException, Depends
from models.itineraryModel import ItineraryRequest, ItineraryResponse, ItineraryHotel, ItinerarySaveRequest
from services.itinerary_service import generate_itinerary, generate_hotels, save_itinerary_to_db, fetch_user_trips_from_db
# from services.database_service import save_itinerary_to_db

router = APIRouter()

@router.get("/")
async def get_itinerary():
    return {"message": "This is the default itinerary"}

@router.post("/itinerary/generate")
async def generate_new_itinerary(request: ItineraryRequest):
    try:
        print("/itenerary/generate invoked")
        itinerary_generated = await generate_itinerary(request.destination, request.days)
        return itinerary_generated
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/itinerary/gethotels")
async def generate_new_itinerary(request: ItineraryHotel):
    try:
        print("/itenerary/gethotels invoked")
        hotels_generated = await generate_hotels(request.destination)
        return hotels_generated
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/itinerary/save")
async def save_itinerary(itinerary_request: ItinerarySaveRequest):
    try:
        print("/itinerary/save invoked")
        result = await save_itinerary_to_db(itinerary_request.user_id, itinerary_request.itinerary)
        print("-----------")
        print(result)
        return {"message": "Itinerary saved successfully", "status": 200}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/itinerary/saved")
async def get_saved_trips(user_id: str):
    """
    Fetch saved trips for a user.
    """
    try:
        # Fetch trips from Firestore or your database
        trips = await fetch_user_trips_from_db(user_id)
        return trips
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
