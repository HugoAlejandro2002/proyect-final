
# Proyecto de Clasificación de Cuerpo y Generación de Rutina con FastAPI y CrewAI

## Descripción del Proyecto
Este proyecto implementa un sistema para la clasificación de tipo de cuerpo y la generación de rutinas personalizadas de entrenamiento y dieta. Utiliza FastAPI como framework web y CrewAI para el manejo de agentes, con modelos de clasificación basados en YOLO y Random Forest.

## Requisitos
- Python 3.10 o superior
- FastAPI
- CrewAI
- Dependencias adicionales especificadas en `pyproject.toml`

## Configuración del Entorno

1. **Instalación de Dependencias:**
   Instala las dependencias necesarias con el gestor de paquetes **uv**. Primero, instala **uv** si no lo tienes:

   ```bash
   pip install uv
   ```

   Luego, instala las dependencias con:

   ```bash
   uv sync 
   ```

2. **Variables de Entorno:**
   Configura las variables de entorno en un archivo `.env` en la raíz del proyecto:

   ```plaintext
   OPENAI_API_KEY=<tu_api_key_de_openai>
   ```

3. **Archivos de Configuración:**
   Asegúrate de que los archivos de configuración `agents.yaml` y `tasks.yaml` estén en el directorio `src/agents/config` para configurar los agentes y tareas en CrewAI.

## Estructura del Proyecto
- **src/**
  - **agents/**: Implementación del agente para CrewAI y configuración en YAML.
  - **api/**: Contiene las rutas y controladores de FastAPI.
  - **core/**: Configuraciones principales de la aplicación, como `settings.py`.
  - **ia_models/**: Modelos de IA para clasificación de cuerpo y procesamiento de imágenes.
  - **interactors/**: Clase `RoutineInteractor` que coordina los servicios de clasificación de cuerpo y generación de rutina.
  - **schemas/**: Esquemas de datos de entrada y salida.
  - **services/**: Servicios para clasificación de cuerpo (`BodyTypeService`) y generación de rutina (`RoutineService`).
  - **utils/**: Utilidades auxiliares como filtros de imagen y herramientas de registro.

## Ejecución del Proyecto
Para ejecutar el proyecto, usa el siguiente comando con **uvicorn**:

```bash
uvicorn src.main:app --reload
```

Este comando inicia el servidor en modo de recarga automática para desarrollo.

## Endpoint Principal
El proyecto expone un único endpoint para analizar el tipo de cuerpo y generar una rutina personalizada:

- **POST /analyze-and-generate-routine**: Recibe los datos del usuario y una imagen para analizar el tipo de cuerpo y generar una rutina personalizada de entrenamiento y dieta.
