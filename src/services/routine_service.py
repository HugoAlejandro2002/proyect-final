from src.agents.routine_crew import RoutineCrew
from src.schemas.user import UserBase

class RoutineService:
    def __init__(self):
        self.crew = RoutineCrew().crew()

    def generate_routine(self, user_data: dict):
        result = self.crew.kickoff(inputs=user_data)
        return result.raw if result else "Error generating routine"
