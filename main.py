from email import message
from email.policy import default
from typing import Optional
from unittest import result
from enum import Enum

from pydantic import BaseModel, EmailStr,Field, HttpUrl

from fastapi import Cookie, FastAPI, Form, Header, Path, Query,status

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
    
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    state: str= Field(
        ...,
        min_length=1,
        max_length=50,
        )
    country: str =Field(
        ...,
        min_length=1,
        max_length=50,
        )

class PersonBase(BaseModel):
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
    email: Optional[EmailStr]
    website: Optional[HttpUrl]



class Person(PersonBase):
    password: str = Field(
                        ...,
                        min_length=8
                        )

    class Config:
        schema_extra={
            "example":{
                "first_name":"Facundo",
                "last_name":"Garcia Martoni",
                "age":"21",
                "hair_color":"blonde",
                "is_married":"false",
                "email":"facundo@example.com",
                "website":"https://github.com/ian333",
                "password":"Hola soy miguel"
            }
        }

class PersonOut(PersonBase):
    pass
        
class LoginOut(BaseModel):
    username:str = Field(
                    ...,
                    max_length=20,
                    example="Ianvaz")
    message: str = Field(default="Login Succesfully!")
@app.get(
    "/",
    status_code=status.HTTP_200_OK)
def home():
    return {"Message" : "Hello World"}

# Request & response body

@app.post(
    "/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED)
def create_person(person: Person = Body(...)):
    return person

# Validaciones Query parameteers

@app.get(
    "/person/detail",
    status_code=status.HTTP_200_OK)
def show_person(
    name:Optional[str]= Query(
        default=None,
        min_length=1,
        max_length=50,
        title="Person name",
        description="This is the person name. Its Between 1-50 characters",
        example="Ian"
        ),
    age:str = Query(
        ...,
        title="Person Age ",
        description="This is the age of the person",
        example="25"
        )
    ) :  
    return {name:age}

# Validaciones Path parameteers

@app.get(
    "/person/detail/{person_id}",
    status_code=status.HTTP_302_FOUND)
def show_person(
    person_id: int= Path(
        ...,
        gt=0,
        title="Person ID",
        description="This person exists ",
        example=22
        )
    ):
    return {person_id: "It exists"}

# Validaciones Request Body 
@app.put(
    "/person/{person_id}",
    status_code=status.HTTP_205_RESET_CONTENT)
def update_person(

    person_id: int = Path(
        ...,
        tittle= "Person ID",
        description="This is the person ID",
        gt=0,
        example=22
        ),
    person: Person = Body(...),
    location: Location = Body(...)
):

    results=person.dict()
    results.update(location.dict())

    return person

# forms

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
    )
def login(
    username:str=Form(...),
    password:str=Form(...)):
    
    return LoginOut(username=username)


# Cookies & Headers Parameters

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
            )
def contact(
    first_name:str= Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    last_name:str= Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    email:EmailStr=Form(...),
    message:str=Form(...,min_length=20),
    user_agent: Optional[str ]=Header(default=None),
    ads:Optional[str]=Cookie(default=None)
):
    return user_agent