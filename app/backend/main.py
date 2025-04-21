from fastapi import FastAPI
from api.routes.itinerary import router as itinerary_router
from api.routes.auth import router as auth_router
from api.routes.user_routes import router as user_router
from api.routes.trip_routes import router as trip_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Travel Go: AI Agentic Travel Planner", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://172.17.48.231:3000"],  # frontend port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(itinerary_router)
app.include_router(user_router)
app.include_router(trip_router)



@app.get("/")
async def root():
    return {"message": "Welcome to TravelGo"}
