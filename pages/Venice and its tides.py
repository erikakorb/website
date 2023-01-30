import streamlit as st
#from streamlit_autorefresh import st_autorefresh
import plotly.express as px
import altair as alt
import requests
import pandas as pd
from datetime import datetime
from urllib.error import URLError


# streamlit configuration page and headers
st.set_page_config(page_title="Venice and its tides", page_icon=" ",layout = 'wide')
align = """
    <style>
        div[data-testid="column"]:nth-of-type(1)
        {
            text-align: center;
        } 

        div[data-testid="column"]:nth-of-type(2)
        {
            text-align: center;
        } 
    </style>
    """
st.markdown(align, unsafe_allow_html=True)

st.write('# Venice and its tides')
st.write(""" ###### I built this dashboard to have **snapshot of the situation of tides and winds across the Venetian lagoon.** A detailed description of what you are looking at is available [here](https://github.com/erikakorb/AcquaAlta), among with the python script adopted to extract **real-time-data** from the [weather stations](https://www.comune.venezia.it/content/dati-dalle-stazioni-rilevamento). Unfortunately, the documentation is still in italian. An english version will be available soon; in the mean time you may consider the wonders of Google translate.""")
st.write(""" ###### What are you waiting for? **Dive into the physics of the tides** and discover the correlations between the water level in the cities, the water level at harbour entrances, and the wind properties! Eventually, you will be able to **predict the rising of the water within the next hour!**""")
st.write(""" ###### Have fun! :) """)
#st_autorefresh(interval=5 * 60 * 1000)   # autorefresh the  page every 5 mins



##### functions ############

def GetJson(url_json,NomiStazioni,StationNames):
    df_json = pd.read_json(url_json)
    df_json = df_json[['stazione','valore']]
    df_json = df_json.loc[df_json.stazione.isin(NomiStazioni)]
    df_json.stazione = StationNames
    df_json = df_json.set_index('stazione')
    df_json = df_json.rename({df_json.columns[0]:'Water Level'}, axis=1) 
    return df_json


def GetData(StationNames,urls):
    dflist=[]
    for station, url in zip(StationNames,urls):
        html = requests.get(url).content
        df=pd.read_html(html)[0]

        df['Date'] = df['Data'].apply(lambda x: datetime.strptime(x,"%Y-%m-%d %H:%M:%S")) # datetime conversion
        df['Date'] = df['Date'].dt.tz_localize('CET')  # fix bug for altair visualization, that assumes dates are in UTC
        df['Day'] = df['Date'].dt.date
        df['Hour'] = df['Date'].dt.strftime('%H:%M')
        df = df.rename({df.columns[1]:'Water'}, axis=1) 
        df['Water'] = df['Water']*100                           # water hight in cm
        if (station == 'San Nicolò') | (station=='Pellestrina'):
            df = df.rename({df.columns[3]:'WindVel'}, axis=1)     
            df['WindVel'] = df['WindVel']*3.6                         # average wind velocity in km/h
            if station == 'San Nicolò':
                df = df.rename({df.columns[4]:'WindDir'}, axis=1) 
            elif station == 'Pellestrina':
                df = df.rename({df.columns[2]:'WindDir'}, axis=1) 

        df['Station'] = station  # add station name
        dflist.append(df)        
    return dflist


def PlotMultiLine(waterwind):
    if waterwind == 'Water':
                StationNames=['Venice','San Nicolò','Alberoni','Pellestrina','Chioggia']
                colors = ['black','#17becf','#b2df8a','#b15928','grey']
                ylabel = 'Water level [cm]'
    elif (waterwind == 'WindVel') | (waterwind == 'WindDir') :
                StationNames=['San Nicolò','Pellestrina']
                colors = ['#17becf','#b15928']
                if waterwind == 'WindVel':
                        ylabel = 'Wind velocity [km/h]'
                else:
                        ylabel = 'Wind direction [degrees]'
                        
    highlight = alt.selection(type='single', on='mouseover', fields=['Station'], nearest=True)

    base = alt.Chart(data).encode(
        x=alt.X('Date:T', title='Time', axis=alt.Axis(labelAngle=0,format="%H:%M")),
        y=alt.Y(f'{waterwind}:Q', title=ylabel)
        )

    points = base.mark_circle().encode( opacity=alt.value(0) ).add_selection( highlight ).properties(
        #width=600  # recall that max width page=1200
        )

    lines = base.mark_line().encode(
        size=alt.condition(~highlight, alt.value(1), alt.value(3)),
        color=alt.Color('Station:N', scale=alt.Scale(domain=StationNames, range=colors) , legend=alt.Legend(
        orient='none',
        legendX=10, legendY=-10,
        direction='horizontal',
        titleAnchor='middle',
        title=' ') )
        )

    if waterwind == 'Water':
                hor_line = alt.Chart(pd.DataFrame({'y': [100]})).mark_rule(color='black').encode(y='y')
                text = text = alt.Chart(pd.DataFrame({'x':text_time_water, 'y': [105], 'note': 'City walking level'})).mark_text(color='black').encode(x='x:T',y='y:Q',text='note:N')
                hor_line_sanmarco = alt.Chart(pd.DataFrame({'y': [80]})).mark_rule(strokeDash=[5, 5], color='black').encode(y='y')
                text_sanmarco = alt.Chart(pd.DataFrame({'x':text_time_water, 'y': [85], 'note': 'San Marco square'})).mark_text(color='black').encode(x='x:T',y='y:Q',text='note:N')
                phantom_line = alt.Chart(pd.DataFrame({'y': [119]})).mark_rule(strokeDash=[5, 5], color='white').encode(y='y')
                chart = points + lines + hor_line + text + hor_line_sanmarco + text_sanmarco + phantom_line
    elif waterwind == 'WindVel': 
                chart = points + lines
    elif waterwind == 'WindDir':
        hor_line = alt.Chart(pd.DataFrame({'y': [60,135]})).mark_rule(strokeDash=[5, 5], color='black').encode(y='y')
        text = text = alt.Chart(pd.DataFrame({'x':[text_time_bora,text_time_scirocco], 'y': [65,140], 'note': ['Bora','Scirocco']})).mark_text(color='black').encode(x='x:T',y='y:Q',text='note:N')
        phantom_line = alt.Chart(pd.DataFrame({'y': [159]})).mark_rule(strokeDash=[5, 5], color='white').encode(y='y')
        chart = points + lines + hor_line + text + phantom_line


    return chart.configure_axis(gridColor='#969696',gridDash=[2, 2],gridOpacity=0.5)


def highlight_water(value):
    if (value >= 90) & (value < 110):
        color = 'yellow'
    elif (value >= 110) & (value < 140):
        color = 'orange'
    elif value >= 140:
        color = 'red'
    else:
        color = 'white'
    return 'background-color: %s' % color





#### extract data ####
StationNames=['Venice','San Nicolò','Alberoni','Pellestrina','Chioggia']
NomiStazioni = ['Punta Salute Canal Grande','Diga sud Lido','Diga nord Malamocco','Diga sud Chioggia','Chioggia Vigo']
urls_json = ['https://dati.venezia.it/sites/default/files/dataset/opendata/livello.json',
             'https://dati.venezia.it/sites/default/files/dataset/opendata/vento.json']

urls=['https://www.comune.venezia.it/sites/default/files/publicCPSM2/stazioni/temporeale/Punta_Salute.html',
      'https://www.comune.venezia.it/sites/default/files/publicCPSM2/stazioni/temporeale/Diga_Sud_Lido.html',
      'https://www.comune.venezia.it/sites/default/files/publicCPSM2/stazioni/temporeale/Diga_Nord_Malamocco.html',
      'https://www.comune.venezia.it/sites/default/files/publicCPSM2/stazioni/temporeale/Diga_Sud_Chioggia.html',
      'https://www.comune.venezia.it/sites/default/files/publicCPSM2/stazioni/temporeale/Chioggia_Citta.html']


dflist = GetData(StationNames,urls)
data = pd.concat(dflist)

first_data = data.groupby('Station').head(1).set_index('Station')
first_time = first_data['Date'][0]
text_time_water = data.groupby('Station').head(66).set_index('Station').tail(1)['Date'][0]  # 46
text_time_scirocco = data.groupby('Station').head(28).set_index('Station').tail(1)['Date'][0]
text_time_bora = data.groupby('Station').head(20).set_index('Station').tail(1)['Date'][0]

last_data = data.groupby('Station').tail(1).set_index('Station')
last_time = last_data['Date'][0]
last_water = last_data[['Water']].astype(int)
last_water.columns = ['Water level [cm]']
styler_water = last_water.T.style.applymap(highlight_water)

last_wind = last_data[['WindVel','WindDir']]
last_wind.columns = ['Wind velocity [km/h]','Wind direction [degrees]']
last_wind = last_wind.T[['San Nicolò','Pellestrina']].astype(int)


#### plot ####
col1, col2 = st.columns(2)
with col1:
    st.altair_chart(PlotMultiLine('Water'), use_container_width=True)

with col2:
    st.write('### Live Data')
    st.dataframe(styler_water,width=500, height=40)
    st.dataframe(last_wind,width=340, height=108)


col3, col4= st.columns(2)
with col3:
    st.altair_chart(PlotMultiLine('WindVel'), use_container_width=True)

with col4:
    #st.altair_chart(PlotMultiLine('WindDir'), use_container_width=True)
    df = data.loc[data['Station'] == 'Pellestrina']
    fig = px.scatter_polar(df, r="Water", theta="WindDir",
                       color="WindVel", color_discrete_sequence=px.colors.sequential.Plasma_r)

    st.plotly_chart(fig, theme="streamlit")
