import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
from pymongo import MongoClient
from dotenv import load_dotenv
import os
# Variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASS = os.getenv("DATABASE_PASS")
DATABASE_AUTHSRC = os.getenv("DATABASE_AUTHSRC")
DATABASE_DB = os.getenv("DATABASE_DB")
DATABASE_COLLECTION = os.getenv("DATABASE_COLLECTION")
# MONGO
cliente = MongoClient(DATABASE_URL,
                      username=DATABASE_USER,
                      password=DATABASE_PASS,
                      authSource=DATABASE_AUTHSRC
                      )
base = cliente[DATABASE_DB]
colleccion = base[DATABASE_COLLECTION]


st.set_page_config(
   page_title="Cuarto de Max",
   page_icon=":cyclone:",
   layout="wide",
   initial_sidebar_state="expanded",
)
# header
st.header("Este es el cuarto de max")


# cosnulta de datos
@st.cache_data(ttl=450)
def carga_datos():
    fecha = datetime.now() - timedelta(days=365)
    consulta = {"fecha": {"$gte": fecha}}
    mydoc = colleccion.find(filter=consulta, projection={"_id": 0})
    datos = pd.DataFrame(list(mydoc))
    datos["fecha"] = pd.to_datetime(
            datos["fecha"].
            dt.tz_localize("UTC")).dt.tz_convert('America/Bogota')
    datos["dia"] = datos["fecha"].map(lambda x: x.dayofweek)
    datos["mes"] = datos["fecha"].map(lambda x: x.month)
    datos["hora"] = datos["fecha"].map(lambda x: x.hour)
    datos["diaano"] = datos["fecha"].map(lambda x: x.day_of_year)
    datos["diasemana"] = datos["fecha"].map(lambda x: x.dayofweek)
    return datos
#cuerpo

descargados = carga_datos()
#st.write(descargados.iloc[-10:])
#metricas
col_1, col_2 = st.columns(2)
with col_1:
    temp_actual = descargados["temperatura"].iloc[-1]
    temp_ante = descargados["temperatura"].iloc[-2]
    cambio = (temp_actual - temp_ante)*100/temp_ante
    st.metric(label="Temperatura actual", value=temp_actual,delta=f"{cambio:.2f}%")
    hace_un_dia = datetime.now() - timedelta(days=1)
    datos_hace_un_dia = descargados[(descargados["fecha"] > hace_un_dia.astimezone())]
    figura = px.scatter(datos_hace_un_dia, x="fecha", y="temperatura", color="humedad",title="Temperatura hoy")
    st.plotly_chart(figura, use_container_width=True)

with col_2:
    humd_actual = descargados["humedad"].iloc[-1]
    humd_ante = descargados["humedad"].iloc[-2]
    cambio_hume = (humd_actual - humd_ante)*100/humd_ante
    st.metric(label="Humedad actual", value=humd_actual,delta=f"{cambio_hume:.2f}")
    hace_un_dia = datetime.now() - timedelta(days=1)
    datos_hace_un_dia = descargados[(descargados["fecha"] > hace_un_dia.astimezone())]
    figura = px.scatter(datos_hace_un_dia, x="fecha", y="humedad", color="temperatura",title="Humedad hoy")
    st.plotly_chart(figura, use_container_width=True)


# graficos
hace_semana = datetime.now() - timedelta(days=7)
datos_hace_semana = descargados[(descargados["fecha"] > hace_semana.astimezone())]
figura= px.scatter(datos_hace_semana,
                   x="fecha",
                   y="temperatura",
                   color="humedad",
                   title="Temperatura la ultima semana")
st.plotly_chart(figura, use_container_width=True)
# texto
st.header("DATOS CALIENTES")
mes_dicionario = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre",
                  "Octubre","Noviembre","Diciembre"]
dia_caliente = descargados[(descargados["temperatura"] == descargados["temperatura"].max())]["fecha"].dt.day
mes_caliente = descargados[(descargados["temperatura"] == descargados["temperatura"].max())]["fecha"].dt.month
hora_caliente = descargados[(descargados["temperatura"] == descargados["temperatura"].max())]["fecha"].dt.hour.values[0]
st.subheader(f"El momento mas caliente fue el {dia_caliente.values[0]} de {mes_dicionario[mes_caliente.values[0]-1]} a las {hora_caliente} horas")
# dia mas caliente
dia_calientito = descargados.groupby("diaano")["temperatura"].mean()[(descargados.groupby("diaano")["temperatura"].mean() == descargados.groupby("diaano")["temperatura"].mean().max())].index[0]
fecha_dia_calientito = descargados[(descargados["diaano"] == dia_calientito)]["fecha"].dt.day.values[0]
mes_dia_calientito = descargados[(descargados["diaano"] == dia_calientito)]["fecha"].dt.month.values[0]
st.subheader(f"El dia mas calientito fue el {fecha_dia_calientito} de {mes_dicionario[mes_dia_calientito-1]}")
# mes calientito
mes_calientito = descargados.groupby("mes")["temperatura"].median()[(descargados.groupby("mes")["temperatura"].median() == descargados.groupby("mes")["temperatura"].median().max())].index[0]
st.subheader(f"El mes mas calientito fue {mes_dicionario[mes_calientito-1]}")
#
st.header("DATOS FRIOS")
#momento mas frio
dia_frio = descargados[(descargados["temperatura"] == descargados["temperatura"].min())]["fecha"].dt.day
mes_frio = descargados[(descargados["temperatura"] == descargados["temperatura"].min())]["fecha"].dt.month
hora_frio = descargados[(descargados["temperatura"] == descargados["temperatura"].min())]["fecha"].dt.hour.values[0]
st.subheader(f"El momento mas frio fue el {dia_frio.values[0]} del {mes_dicionario[mes_frio.values[0]-1]} a las {hora_frio} horas")
# dia mas frio
dia_friito = descargados.groupby("diaano")["temperatura"].mean()[(descargados.groupby("diaano")["temperatura"].mean() == descargados.groupby("diaano")["temperatura"].mean().min())].index[0]
fecha_dia_friito = descargados[(descargados["diaano"] == dia_friito)]["fecha"].dt.day.values[0]
mes_dia_friito= descargados[(descargados["diaano"] == dia_friito)]["fecha"].dt.month.values[0]
st.subheader(f"El dia mas frio fue el {fecha_dia_friito} de {mes_dicionario[mes_dia_friito-1]}")
#mes mas frio
mes_masfrio = descargados.groupby("mes")["temperatura"].median()[(descargados.groupby("mes")["temperatura"].median() == descargados.groupby("mes")["temperatura"].median().min())].index[0]
st.subheader(f"El mes mas frio fue {mes_dicionario[mes_masfrio-1]}")
# final de la pagina
diferencia = int((datetime.now() - datetime.fromtimestamp(descargados["fecha"].iloc[-1].timestamp())).seconds / 60)
# temperatura mensal
pivote = pd.pivot_table(descargados,index=["diasemana"],columns=["hora"],aggfunc="median",values=["temperatura"])
grafico_mensual = px.imshow(pivote.values.tolist(),
                            y=["lunes","martes","Miercoles","jueves","viernes","sabado","domingo"],
                            title="Temperatura segun el dia y la hora",
                            labels=dict(x="Hora militar",y="dia de la semana")
)
grafico_mensual.update_xaxes(side="top")
st.plotly_chart(grafico_mensual, use_container_width=True)

#

if diferencia > 30:
    st.write("deberias recargar la pagina")

st.metric(label="Hace 	:hourglass_flowing_sand:", value=f"{diferencia} minutos",help="si este valor es mayor a 15 se debe recargar la pagina")
