from src.services.routine_service import RoutineService
from src.schemas.user import UserCreate

def run():
    # Define los inputs del usuario
    inputs = {
        'first_name': "John",
        'last_name': "Doe",
        'email': "john.doe@example.com",
        'age': 30,
        'gender': "male",
        'height': 175,
        'physical_activity_per_week': 3,
        'dietary_restrictions': ["vegetarian"],
        'flavor_preferences': ["savory"],
        'objective': "lose weight"
    }

    # Instancia el servicio de rutina
    service = RoutineService()

    # Ejecuta el método generate_routine con los inputs del usuario
    result = service.generate_routine(inputs)
    
    # Imprime el resultado
    print("Generated Routine:\n", result)

if __name__ == "__main__":
    run()
