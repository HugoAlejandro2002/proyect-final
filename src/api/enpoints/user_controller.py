
from fastapi import  APIRouter, Depends, Form, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse

from src.ia_models.orchestrator import Orchestrator
from src.schemas.user import UserCreate, UserCreated
from src.ia_models.orchestrator import get_orquestator
from src.services.body_type_service import BodyTypeService

router = APIRouter()

@router.post("/analyze-body-type", response_model=UserCreated)
async def analyze_body_type(
    user_data = Form(...), 
    image: UploadFile = File(...),
    orchestrator = Depends(get_orquestator)
):
    # Leer la imagen cargada
    body_type_service = BodyTypeService(orchestrator=orchestrator)
    image_bytes = await image.read()

    result = body_type_service.process_image_and_classify(image_bytes)

    # response_data = user_data.dict()
    # response_data["id"] = 1  # Simulación de un ID generado
    # response_data.update({"body_type_result": result})
    return JSONResponse(content={"body_type_result": result})