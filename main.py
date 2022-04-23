from typing import Optional
from unittest import result
from enum import Enum

from pydantic import BaseModel,Field

from fastapi import FastAPI, Path, Query

from fastapi import Body

app = FastAPI()

# models

class HairColor(Enum):
    #Lista de Colores de cabello con Enum Dato excentrico , de esta manera solo se puede seleccionar alguna opcion de las siguientes
    # a continuacion
    white= "white"
    black= "black"
    brown= "brown"
    blonde="blonde"
    red="red"

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str = Field (
        ...,
        min_length=1,
        max_length=50,
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50)
    age : int = Field(
        ...,
        gt=0,
        le=115,
        )
    hair_color: Optional[HairColor]= Field(default=None,)
    is_married: Optional[bool] = Field(default=None)


@app.get("/")
def home():
    return {"Message" : "Hello World"}

# Request & response body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person


# Validaciones Query parameteers

@app.get("/person/detail")
def show_person(
    name:Optional[str]= Query(
        default=None,
        min_length=1,
        max_length=50,
        title="Person name",
        description="This is the person name. Its Between 1-50 characters"
        ),
    age:str = Query(
        ...,
        title="Person Age ",
        description="This is the age of the person"
        )
    ) :  
    return {name:age}

# Validaciones Path parameteers

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int= Path(
        ...,
        gt=0,
        title="Person ID",
        description="This person exists "
        )
    ):
    return {person_id: "It exists"}

# Validaciones Request Body 
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        tittle= "Person ID",
        description="This is the person ID",
        gt=0
        ),
    person: Person = Body(...),
    location: Location = Body(...)
):

    results=person.dict()
    results.update(location.dict())

    return results