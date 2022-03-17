# Bandapp
Simple FastAPI witch gives what the menu is for the week at Bandejao  UNICAMP

Aplicativo levanta as refeições do bandejão de campinas <https://www.prefeitura.unicamp.br/cardapio/>
#-----------------------------------------------------------------------------------------------------


endpoints:
/ -> get weekly menu
/today -> get today's menu
/{day} -> get {day's} menu


/load_week and /load_today are endpoints that are to be activated with cron so that the api is up to date;



@startup

docker build .
docker run -p 8000:8002 -it --net=host <dockerHash>
  
  
  Documemntação da API em:
  
  http://127.0.0.1:8000/docs
  http://127.0.0.1:8000/redoc


SCHEMA
  
  Meal{
description:	
Classe para salvar uma refeição

id*	integer
title: Id
date*	string
title: Date
veg*	integer
title: Veg
main_dish*	string
title: Main Dish
side*	string
title: Side
salad*	string
title: Salad
dessert*	string
title: Dessert
lunch*	integer
title: Lunch
 
}
