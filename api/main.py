from fastapi import FastAPI, Request
from webscrap import *
from typing import List
from pydantic import BaseModel

print(__file__)


class Meal(BaseModel):
    """Classe para salvar uma refeição"""
    id: int
    date: str
    veg: int
    main_dish: str
    side: str
    salad: str
    dessert: str
    lunch: int


today = []
week = []

app = FastAPI()
app.type = "00"

@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}

@app.get("/", response_model=List[Meal])
async def get_week():
    global week
    return week


@app.get("/today", response_model=List[Meal])
async def read_today():
    global today
    return today


@app.get("/{day}", response_model=List[Meal])
async def read_someday(day: datetime.date):
    day = get_menu(day.strftime("%Y-%M-%D"))
    return day


@app.post('/load_week', status_code=201)
async def load_Week():
    global week
    week = []

    aux = getWeek()
    for meal in aux:
        meal['id'] = len(week)
        week.append(meal)
    return week


@app.post('/load_today', status_code=201)
async def load_TodayMeals():
    global today
    today = []
    aux = get_menu()

    for meal in aux:
        meal['id'] = len(today)
        today.append(meal)
    return today
