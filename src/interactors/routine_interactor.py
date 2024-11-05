from src.services.body_type_service import BodyTypeService
from src.services.routine_service import RoutineService

class RoutineInteractor:
    def __init__(self, body_type_service: BodyTypeService, routine_service: RoutineService):
        self.body_type_service = body_type_service
        self.routine_service = routine_service

    async def analyze_and_generate_routine(self, user_data: dict, image_bytes: bytes) -> dict:
        body_type_result = self.body_type_service.process_image_and_classify(image_bytes)
        
        user_data["body_type"] = body_type_result

        routine_result = self.routine_service.generate_routine(user_data)
        return {
            "body_type": body_type_result,
            "routine": routine_result
        }