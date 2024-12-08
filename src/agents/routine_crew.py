from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field
from crewai_tools import PDFSearchTool

class RoutinePlanOutput(BaseModel):
    """Modelo de salida para la rutina y dieta personalizada"""
    training_plan: str = Field(..., description="Plan de entrenamiento detallado")
    diet_plan: str = Field(..., description="Plan de dieta detallado")


@CrewBase
class RoutineCrew:
    """Clase principal que define los agentes y tareas para la creación de rutinas personalizadas"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def routine_agent(self) -> Agent:
        """Define el agente que generará las rutinas"""
        return Agent(
            config=self.agents_config['routine_agent'],
            tools=[PDFSearchTool(file_path="get-fit-life.pdf")],
            verbose=True,
        )

    @task
    def create_routine_task(self) -> Task:
        """Crea la tarea que generará la rutina y dieta usando el PDF y la información del usuario"""
        return Task(
            config=self.tasks_config['routine_task'],
            agent=self.routine_agent(),
            output_json=RoutinePlanOutput,
        )

    @crew
    def crew(self) -> Crew:
        """Crea y configura la tripulación con las tareas y agentes definidos"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
