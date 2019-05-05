from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from datetime import datetime as dt


import os   

app = Flask(__name__)

#Criar GetByID: http://blog.luisrei.com/articles/flaskrest.html

def converte(old):
    return dt.strftime(dt.strptime(old,'%d/%m/%Y'),'%Y-%m-%d')
    

@app.route('/api/v1/bandeco/', methods=['GET'])
def Refeicoes():
    URL = "https://www.prefeitura.unicamp.br/apps/site/cardapio.php"
    html_doc = urlopen(URL).read()
    soup = BeautifulSoup(html_doc,"html.parser")
    data = []
    for dataBox_dia in soup.find_all("a"):
        dia = converte(dataBox_dia.text.strip())
         
        URL = "https://www.prefeitura.unicamp.br/apps/site/cardapio.php?d={}".format(dia)
        html_doc = urlopen(URL).read()
        soup = BeautifulSoup(html_doc,"html.parser")
        
        ObjCafeManha = soup.find("div", class_="fundo_cardapio")
        data.append({ 
            'Data': dia,
            'cafe': ObjCafeManha.text.strip()
        })

    
        for dataBox  in soup.find_all("table", class_="fundo_cardapio"):
            refeicao = dataBox.text.strip()
            ArrozIntegral = refeicao.count('ARROZ INTEGRAL')
            Arroz =  refeicao.count('ARROZ')
            Feijao  = refeicao.count('FEIJ\u00c3O')
            
            if refeicao.find('\n\n\n PTS')!= -1:
                PratoPrincipal = refeicao[refeicao.find('PRATO PRINCIPAL')+18:refeicao.find('\n\n\n PTS')].replace('\n\n\n',' ')
            else:
                PratoPrincipal = refeicao[refeicao.find('PRATO PRINCIPAL')+18:refeicao.find('\n\n\nSALADA')].replace('\n\n\n','')

            if refeicao.find('PTS')!= -1: 
                Pts = refeicao[refeicao.find('PTS')+4:refeicao.find('\n\n\nSALADA:')]
            else:   
                Pts = -1

            Salada = refeicao[refeicao.find('SALADA:')+7:refeicao.find('\n\n\nSOBREMESA:')]   
            Sobremesa = refeicao[refeicao.find('SOBREMESA:')+10:refeicao.find('\n\n\nSUCO')]   
            Suco = refeicao[refeicao.find('SUCO:')+5:refeicao.find('\n\n\nObserva')]

            Contem = refeicao[refeicao.find('CONTÉM')+7:refeicao.find('\r\nN\u00c3O')]
            NContem = refeicao[refeicao.find('\r\nN\u00c3O')+12:refeicao.find('.\n \r\nA')]

            data.append({
                   
                    'Arroz_integral': ArrozIntegral,
                    'Arroz': Arroz,
                    'Feijao':Feijao,
                    'Prato_Principal':PratoPrincipal,
                    'PTS': Pts,
                    'Salada': Salada,
                    'Sobremesa': Sobremesa,
                    'Suco': Suco,
                    'Contem': Contem.replace('\r','').replace('\n',''),
                    'NContem': NContem

            })

                    
            
                    
    return jsonify({'Bandejao': data})  

##########################################################################################3



@app.route('/api/v1/bandeco/<id_data>', methods=['GET'])
def Refeicao_dia(id_data):
    URL = "https://www.prefeitura.unicamp.br/apps/site/cardapio.php?d={}".format(id_data)
    html_doc = urlopen(URL).read()
    soup = BeautifulSoup(html_doc,"html.parser")
    data = []
    
    ObjCafeManha = soup.find("div", class_="fundo_cardapio")
    data.append({'cafe': ObjCafeManha.text.strip()})

  
    for dataBox  in soup.find_all("table", class_="fundo_cardapio"):
        refeicao = dataBox.text.strip()
        ArrozIntegral = refeicao.count('ARROZ INTEGRAL')
        Arroz =  refeicao.count('ARROZ')
        Feijao  = refeicao.count('FEIJ\u00c3O')
        PratoPrincipal = refeicao[refeicao.find('PRATO PRINCIPAL')+18:refeicao.find('\n\n\n PTS')]
        
        if refeicao.find('PTS')!= -1: 
            Pts = refeicao[refeicao.find('PTS')+4:refeicao.find('\n\n\nSALADA:')]
        else:   
            Pts = -1

        Salada = refeicao[refeicao.find('SALADA:')+7:refeicao.find('\n\n\nSOBREMESA:')]   
        Sobremesa = refeicao[refeicao.find('SOBREMESA:')+10:refeicao.find('\n\n\nSUCO')]   
        Suco = refeicao[refeicao.find('SUCO:')+5:refeicao.find('\n\n\nObserva')]

        Contem = refeicao[refeicao.find('CONTÉM')+7:refeicao.find('\r\nN\u00c3O')]
        NContem = refeicao[refeicao.find('\r\nN\u00c3O')+12:refeicao.find('.\n \r\nA')]

        data.append({
                'Data': id_data,
                'Arroz_integral': ArrozIntegral,
                'Arroz': Arroz,
                'Feijao':Feijao,
                'Prato_Principal':PratoPrincipal.replace('\n\n\n',' E '),
                'PTS': Pts,
                'Salada': Salada,
                'Sobremesa': Sobremesa,
                'Suco': Suco,
                'Contem': Contem.replace('\r','').replace('\n',''),
                'NContem': NContem

        })

                
    return jsonify({'Bandejao': data})  

    
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    # Tem que ser 0.0.0.0 para rodar no Heroku
    app.run(host='127.0.0.1', port=port)