from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated
from fastapi import FastAPI
from ultralytics import YOLO  

app = FastAPI()
model = YOLO('yolo_keypoints_model.pt')

class UserBase(BaseModel):
    first_name: Annotated[str, Field(examples=["John"], min_length=1, description="First name")]
    last_name: Annotated[str, Field(examples=["Doe"], min_length=1, description="Last name")]
    email: Annotated[str, Field(examples=["john.doe@example.com"], description="Email address")]
    age: Annotated[int, Field(ge=10, le=100, examples=[30], description="Age of the user")]
    gender: Annotated[str, Field(examples=["male", "female"], description="Gender")]
    height: Annotated[float, Field(ge=100, le=250, examples=[175], description="Height in cm")]
    physical_activity_per_week: Annotated[int, Field(ge=0, le=14, examples=[3], description="Physical activity frequency per week")]
    dietary_restrictions: Annotated[Optional[List[str]], Field(default=None, description="List of dietary restrictions, e.g., 'vegetarian', 'vegan', 'halal'")]
    flavor_preferences: Annotated[Optional[List[str]], Field(default=None, examples=[["sweet", "savory"]], description="Flavor preferences or favorite foods")]
    objective: Annotated[Optional[str], Field(default="fitness", examples=["weight loss"], description="Nutrition objective")]

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    pass

class UserCreated(UserBase):
    id: Annotated[int, Field(ge=1, examples=[1])]



