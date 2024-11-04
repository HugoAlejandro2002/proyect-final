

from pyexpat import model
from fastapi import  UploadFile, File
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from src.schemas.user import UserCreate, UserCreated


@app.post("/classify_body_type", response_model=UserCreated)
async def classify_body_type(
    user_data: UserCreate, 
    image: UploadFile = File(...)
):
    
    image_bytes = await image.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    results = model(img)
    body_type = "unknown"


    for result in results[0].keypoints:  
        puntos = np.array(result.xy)
        hombros_ancho = np.linalg.norm(puntos[5] - puntos[6])
        cintura_ancho = np.linalg.norm(puntos[11] - puntos[12])
        cadera_ancho = np.linalg.norm(puntos[13] - puntos[14])

        if cintura_ancho < hombros_ancho * 0.8:
            body_type = "slim"
        elif cadera_ancho > hombros_ancho:
            body_type = "fat"
        else:
            body_type = "fit"

    
    user_data_dict = user_data.dict()
    user_data_dict.update({
        "id": 1,  
        "body_type": body_type,
        "recommended_diet": generate_diet_plan(body_type, user_data)
    })

    return JSONResponse(content=user_data_dict)


def generate_diet_plan(body_type: str, user_data: UserCreate) -> str:
    diet_recommendation = ""

    if body_type == "slim" and user_data.objective == "muscle gain":
        diet_recommendation += "High protein, balanced carbs and fats for muscle gain. "
    elif body_type == "fat" and user_data.objective == "weight loss":
        diet_recommendation += "Low carb, high fiber diet with moderate protein for weight loss. "
    elif body_type == "fit":
        diet_recommendation += "Balanced diet to maintain fitness level. "
    
    if user_data.dietary_restrictions:
        if "vegetarian" in user_data.dietary_restrictions:
            diet_recommendation += "Ensure sufficient plant-based protein intake. "
        if "vegan" in user_data.dietary_restrictions:
            diet_recommendation += "Focus on vegan protein sources like beans, lentils, and tofu. "
        if "halal" in user_data.dietary_restrictions:
            diet_recommendation += "Ensure all sources of meat are halal-certified. "

    if user_data.flavor_preferences:
        diet_recommendation += f"Include more {', '.join(user_data.flavor_preferences)} options to suit your taste preferences. "

    return diet_recommendation
