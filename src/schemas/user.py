from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated
from enum import Enum
from fastapi import Form

class GenderEnum(str, Enum):
    male = "male"
    female = "female"


class UserBase(BaseModel):
    first_name: Annotated[
        str, Field(..., examples=["John"], min_length=1, description="First name")
    ]
    last_name: Annotated[
        str, Field(..., examples=["Doe"], min_length=1, description="Last name")
    ]
    email: Annotated[
        str, Field(..., examples=["john.doe@example.com"], description="Email address")
    ]
    age: Annotated[
        int, Field(..., ge=10, le=100, examples=[30], description="Age of the user")
    ]
    gender: Annotated[
        GenderEnum, Field(..., examples=["male"], description="Gender")
    ]
    height: Annotated[
        float, Field(..., ge=100, le=250, examples=[175], description="Height in cm")
    ]
    physical_activity_per_week: Annotated[
        int,
        Field(
            ..., ge=0, le=14, examples=[3],
            description="Physical activity frequency per week",
        ),
    ]
    dietary_restrictions: Annotated[
        Optional[List[str]],
        Field(
            default=None,
            description="List of dietary restrictions, e.g., 'vegetarian', 'vegan', 'halal'",
        ),
    ]
    flavor_preferences: Annotated[
        Optional[List[str]],
        Field(
            default=None,
            examples=[["sweet", "savory"]],
            description="Flavor preferences or favorite foods",
        ),
    ]
    objective: Annotated[
        Optional[str],
        Field(
            default="fitness",
            examples=["weight loss"],
            description="Nutrition objective",
        ),
    ]

    model_config = ConfigDict(from_attributes=True)

class UserInfoBody(UserBase):
    @classmethod
    def as_form(
        cls,
        first_name: str = Form(..., description="First name"),
        last_name: str = Form(..., description="Last name"),
        email: str = Form(..., description="Email address"),
        age: int = Form(..., ge=10, le=100, description="Age of the user"),
        gender: GenderEnum = Form(..., description="Gender"),
        height: float = Form(..., ge=100, le=250, description="Height in cm"),
        physical_activity_per_week: int = Form(..., ge=0, le=14, description="Physical activity frequency per week"),
        dietary_restrictions: Optional[List[str]] = Form(None, description="Dietary restrictions"),
        flavor_preferences: Optional[List[str]] = Form(None, description="Flavor preferences"),
        objective: Optional[str] = Form(..., description="User's fitness objective"),
    ) -> "UserInfoBody":
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            age=age,
            gender=gender,
            height=height,
            physical_activity_per_week=physical_activity_per_week,
            dietary_restrictions=dietary_restrictions,
            flavor_preferences=flavor_preferences,
            objective=objective,
        )

