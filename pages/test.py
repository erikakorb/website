import plotly.express as px
#import matplotlib.pyplot as plt
import streamlit as st
##df = px.data.wind()
##fig = px.scatter_polar(df, r="frequency", theta="direction",
##                       color="strength", symbol="strength", size="frequency",
##                       color_discrete_sequence=px.colors.sequential.Plasma_r)
##st.pyplot(fig)

#create your figure and get the figure object returned
df = px.data.wind()
fig = px.scatter_polar(df, r="frequency", theta="direction",
                       color="strength", symbol="strength", size="frequency",
                       color_discrete_sequence=px.colors.sequential.Plasma_r)
st.plotly_chart(fig, theme="streamlit")
