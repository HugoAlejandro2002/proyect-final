
from fastapi import  APIRouter, Depends, Form, UploadFile, File
from fastapi.responses import JSONResponse

from src.interactors.routine_interactor import RoutineInteractor
from src.schemas.user import UserInfoBody
from src.ia_models.orchestrator import get_orquestator
from src.services.body_type_service import BodyTypeService
from src.services.routine_service import RoutineService

router = APIRouter()

@router.post("/analyze-and-generate-routine")
async def analyze_and_generate_routine(
    user_data: UserInfoBody = Depends(UserInfoBody.as_form),
    image: UploadFile = File(...),
    orchestrator=Depends(get_orquestator)
):
   
    image_bytes = await image.read()

    body_type_service = BodyTypeService(orchestrator=orchestrator)
    routine_service = RoutineService()
    interactor = RoutineInteractor(body_type_service, routine_service)

    result = await interactor.analyze_and_generate_routine(user_data.model_dump(), image_bytes)
    return JSONResponse(content=result)