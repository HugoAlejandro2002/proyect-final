
from fastapi import  APIRouter, Form, UploadFile, File
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from src.schemas.user import UserCreate, UserCreated

router = APIRouter()

@router.post("/generate-routine", response_model=UserCreated)
async def classify_body_type(
    user_data = Form(...), 
    image: UploadFile = File(...)
):
    
    
    return JSONResponse(content={"a":"aaa"})


# def generate_diet_plan(body_type: str, user_data: UserCreate) -> str:
#     diet_recommendation = ""

#     if body_type == "slim" and user_data.objective == "muscle gain":
#         diet_recommendation += "High protein, balanced carbs and fats for muscle gain. "
#     elif body_type == "fat" and user_data.objective == "weight loss":
#         diet_recommendation += "Low carb, high fiber diet with moderate protein for weight loss. "
#     elif body_type == "fit":
#         diet_recommendation += "Balanced diet to maintain fitness level. "
    
#     if user_data.dietary_restrictions:
#         if "vegetarian" in user_data.dietary_restrictions:
#             diet_recommendation += "Ensure sufficient plant-based protein intake. "
#         if "vegan" in user_data.dietary_restrictions:
#             diet_recommendation += "Focus on vegan protein sources like beans, lentils, and tofu. "
#         if "halal" in user_data.dietary_restrictions:
#             diet_recommendation += "Ensure all sources of meat are halal-certified. "

#     if user_data.flavor_preferences:
#         diet_recommendation += f"Include more {', '.join(user_data.flavor_preferences)} options to suit your taste preferences. "

#     return diet_recommendation
