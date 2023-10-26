import streamlit as st
#from streamlit_autorefresh import st_autorefresh
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly"
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
            text-align: left;
        } 

        div[data-testid="column"]:nth-of-type(2)
        {
            text-align: left;
        }
        div[data-testid="column"]:nth-of-type(3)
        {
            text-align: left;
        }
        div[data-testid="column"]:nth-of-type(4)
        {
            text-align: left;
        }
        div[data-testid="column"]:nth-of-type(5)
        {
            text-align: left;
        }
        div[data-testid="column"]:nth-of-type(6)
        {
            text-align: left;
        }
        [data-testid="stMetricValue"] {
            font-size: 20px;
            text-align: left;
        }
    </style>
    """
st.markdown(align, unsafe_allow_html=True)


################################ profile pic
import io
from PIL import Image
import base64

file = open("Korb_Erika_pic.jpg", "rb")
contents = file.read()
img_str = base64.b64encode(contents).decode("utf-8")
buffer = io.BytesIO()
file.close()
img_data = base64.b64decode(img_str)
img = Image.open(io.BytesIO(img_data))
resized_img = img.resize((150, 150))  # x, y
resized_img.save(buffer, format="PNG")
img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url('data:image/png;base64,{img_b64}');
                background-repeat: no-repeat;
                padding-top: 50px;
                background-position: 90px 50px;
            }}
            [data-testid="stSidebarNav"]::before {{
                content: " ";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 50px;
                position: relative;
                top: 200px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

###############################



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

    points = base.mark_circle().encode( opacity=alt.value(0)).add_selection( highlight ).properties(
        #width=600  # recall that max width page=1200
        )

    lines = base.mark_line().encode(
        size=alt.condition(~highlight, alt.value(1), alt.value(3)),
        color=alt.Color('Station:N', scale=alt.Scale(domain=StationNames, range=colors, nice={'interval': 'hour', 'step': 2}) ,
                        legend=alt.Legend(
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
                phantom_line = alt.Chart(pd.DataFrame({'y': [119]})).mark_rule(strokeDash=[5, 5], color='white',opacity=0.3).encode(y='y')
                chart = points + lines + hor_line + text + hor_line_sanmarco + text_sanmarco + phantom_line
    elif waterwind == 'WindVel': 
                chart = points + lines
    elif waterwind == 'WindDir':
        hor_line = alt.Chart(pd.DataFrame({'y': [60,135]})).mark_rule(strokeDash=[5, 5], color='black').encode(y='y')
        text = text = alt.Chart(pd.DataFrame({'x':[text_time_bora,text_time_scirocco], 'y': [65,140], 'note': ['Bora','Scirocco']})).mark_text(color='black').encode(x='x:T',y='y:Q',text='note:N')
        phantom_line = alt.Chart(pd.DataFrame({'y': [159]})).mark_rule(strokeDash=[5, 5], color='white',opacity=0.3).encode(y='y')
        chart = points + lines + hor_line + text + phantom_line


    return chart.configure_axis(gridColor='#969696',gridDash=[2, 2],gridOpacity=0.5)

def PolarPlot(NameStation):
    df = data.loc[data['Station'] == NameStation]
    df = WindConvert(df,'WindDir')
    df['newcol'] = df.index
    df = df.rename({'WindVel':'km/h'}, axis=1) 
    fig = px.scatter_polar(df, r="newcol", theta="WindDir",
                       color="km/h", hover_data=[df.Data, df.WindDir, df['km/h']])
    fig.update_layout(title = NameStation, showlegend = False,    polar = dict(
        radialaxis = dict(tickvals = [72,144,216], ticktext = ['-18h','-12h','-6h']) ,
        angularaxis = dict(tickvals = [0,45,90,135,180,225,270,315], ticktext = ['N','NE','E','SE','S','SW','W','NW'])    )   )
    fig.update_traces(hovertemplate='%{customdata[0]} <br> Direction = %{customdata[1]}° <br> Velocity = %{customdata[2]:.2f} km/h')
    return fig

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

def WindConvert(df,colname):
    df.loc[(((df[colname] > 348.75) & (df[colname] <= 360)) | ((df[colname] >= 0) & (df[colname] <= 11.25))), 'Direction'] = 'N'
    df.loc[((df[colname] > 11.25) & (df[colname] <= 33.75)), 'Direction'] = 'NNE'
    df.loc[((df[colname] > 33.75) & (df[colname] <= 56.25)), 'Direction'] = 'NE'
    df.loc[((df[colname] > 56.25) & (df[colname] <= 78.75)), 'Direction'] = 'ENE'
    df.loc[((df[colname] > 78.75) & (df[colname] <= 101.25)), 'Direction'] = 'E'
    df.loc[((df[colname] > 101.25) & (df[colname] <= 123.75)), 'Direction'] = 'ESE'
    df.loc[((df[colname] > 123.75) & (df[colname] <= 146.25)), 'Direction'] = 'SE'
    df.loc[((df[colname] > 146.25) & (df[colname] <= 168.75)), 'Direction'] = 'SSE'
    df.loc[((df[colname] > 168.75) & (df[colname] <= 191.25)), 'Direction'] = 'S'
    df.loc[((df[colname] > 191.25) & (df[colname] <= 213.75)), 'Direction'] = 'SSW'
    df.loc[((df[colname] > 213.75) & (df[colname] <= 236.25)), 'Direction'] = 'SW'
    df.loc[((df[colname] > 236.25) & (df[colname] <= 258.75)), 'Direction'] = 'WSW'
    df.loc[((df[colname] > 258.75) & (df[colname] <= 281.25)), 'Direction'] = 'W'
    df.loc[((df[colname] > 281.25) & (df[colname] <= 303.75)), 'Direction'] = 'WNW'
    df.loc[((df[colname] > 303.75) & (df[colname] <= 326.25)), 'Direction'] = 'NW'
    df.loc[((df[colname] > 326.25) & (df[colname] <= 348.75)), 'Direction'] = 'NNW'
    return df




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
copylastwind = last_wind.copy()
last_wind.columns = ['Wind velocity [km/h]','Wind direction [degrees]']
last_wind = last_wind.T[['San Nicolò','Pellestrina']].astype(int)
last_wind_direction = WindConvert(copylastwind,'WindDir')['Direction']


#### plot ####
col1, colempty, col2, col3,col4,col5 = st.columns([4,0.5,1,1,1,1])
with col1:
    st.altair_chart(PlotMultiLine('Water'), use_container_width=True)
with col2:
    st.write('#### Venice')
    #st.dataframe(styler_water,width=500, height=40)
    #st.dataframe(last_wind,width=340, height=108)
    st.metric(label="Water level", value=str(last_water.T['Venice'][0]) + ' cm', delta=str(last_water.T['Venice'][0]-100) + ' cm', delta_color='inverse')
with col3:
    st.write('#### Chioggia')
    st.metric(label="Water level", value=str(last_water.T['Chioggia'][0]) + ' cm',delta=str(last_water.T['Chioggia'][0]-100) + ' cm', delta_color='inverse')
with col4:
    st.write('#### San Nicolò')
    st.metric(label="Water level", value=str(last_water.T['San Nicolò'][0]) + ' cm',delta=str(last_water.T['San Nicolò'][0]-100) + ' cm', delta_color='inverse')
    st.metric(label="Wind velocity", value=str(last_wind['San Nicolò'][0]) + ' km/h')
    st.metric(label="Wind direction", value=str(last_wind_direction['San Nicolò']))
with col5:
    st.write('#### Pellestrina')
    st.metric(label="Water level", value=str(last_water.T['Pellestrina'][0]) + ' cm',delta=str(last_water.T['Pellestrina'][0]-100) + ' cm', delta_color='inverse')
    st.metric(label="Wind velocity", value=str(last_wind['Pellestrina'][0]) + ' km/h')
    st.metric(label="Wind direction", value=str(last_wind_direction['Pellestrina']))


colW1,  colW2, colW3 = st.columns([1,1,1])
with colW1:
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.altair_chart(PlotMultiLine('WindVel'), use_container_width=True)
with colW2:
    st.plotly_chart(PolarPlot('San Nicolò'), theme=None, use_container_width=True)
with colW3:
    #st.altair_chart(PlotMultiLine('WindDir'), use_container_width=True)    
    st.plotly_chart(PolarPlot('Pellestrina'), theme=None, use_container_width=True)
