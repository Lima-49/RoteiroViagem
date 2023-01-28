import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime 

## Functions ##
def get_api_response():

    url = "https://awesomeapi-exchange.p.rapidapi.com/json/list/EUR/10"

    headers = {
        "X-RapidAPI-Key": "3ec7e94af8msha93851d69707896p10e2d0jsn05ef113b8aa4",
        "X-RapidAPI-Host": "awesomeapi-exchange.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers).json()

    return response 

## Main ##
st.title("Cotação de moedas externas")

result =  get_api_response()

#Transformando o resultado da API em um dataframe
df = pd.DataFrame(result)

#Criando um novo dataframe com duas colunas, menor valor da moeda e a data do dia 
df = pd.DataFrame({"Valor":list(map(lambda val: round(float(val),2), df['low'])), 
                    "Data":list(map(lambda timestamp: datetime.fromtimestamp(int(timestamp)).strftime('%d-%m-%y'), df['timestamp']))})

#Invertendo os valores para pegar da data anterior até a data atual
df.sort_values(by=['Data'], ascending=True, inplace=True)

#Criando um plot com o stilo da biblioteca disponibilizada no github
plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')
fig,ax = plt.subplots()

#definindo os valores de cada eixo do gráfico
x = df['Valor']
y = df['Data']

#Plotando um gráfico de barras 
line, = ax.plot(y,x)

#Manipulando as linhsa atrás do gráfico, nesse caso, apagando as linhas da vertical e mantendo as linhas da horizontal
ax.grid(visible=False, axis='x')
ax.grid(which="major", axis='y', color='#DAD8D7', alpha=0.5, zorder=1)

ax.set_xticklabels('') # No need for an axis label

st.pyplot(fig)

st.bar_chart(df, x='Data', y='Valor')