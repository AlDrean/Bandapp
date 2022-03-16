from pydantic import BaseModel


class Meal(BaseModel):
    """Classe para salvar uma refeição"""
    date: str
    main_dish: str
    side: str
    salad: str
    dessert: str
