import streamlit as st
import pandas as pd
import numpy as np

import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

df = pd.read_csv("crime-rate.csv")

st.title('Crime in US')

st.header('Data overview')

st.write(df)
st.write(df.describe())
st.write(df.columns)

st.header("We will analyse small and medium towns with population less than 100000")

df = df[df['population'] <= 100000]

st.header('General statistics about town')

state_checkbox = st.selectbox("Choose state", df['state'].unique())
town_checkbox = st.selectbox("Choose community", df[df['state'] == state_checkbox]['communityName'].unique())

df_graph_2 = df[df['communityName'] == town_checkbox]
st.write(df_graph_2)

st.header('Rape per pop rate depending on population in small cities')

borders = st.slider('population', 0, 100000, (25000, 75000), key=1)

st.write(borders)

l_pop = borders[0]
r_pop = borders[1]

df_graph_1 = df[['communityName', 'population', 'rapesPerPop', 'state']]
df_graph_1 = df_graph_1[l_pop <= df_graph_1['population']]
df_graph_1 = df_graph_1[r_pop >= df_graph_1['population']]

fig = go.Figure()
fig.update_layout(legend_orientation="h",
                  margin=dict(l=0, r=0, t=100, b=0),
                  legend=dict(x=.5, xanchor="center"),
                  title="dependence of rapes per pop number on total population",
                  width=1000,
                  height=800,
                  xaxis_title="population",
                  yaxis_title="rape per pop")

for state in df_graph_1['state'].unique():
    df_graph_1_t = df_graph_1[df_graph_1['state'] == state]
    fig.add_trace(go.Scatter(x=df_graph_1_t['population'], y=df_graph_1_t['rapesPerPop'], visible='legendonly',
                             mode="markers", name=state))

st.write(fig)

st.header("Race influence on crime level")
race_radio = st.radio("Choose race", ('White', 'Black', 'Asian', 'Hispanic'), key=2)
race = race_radio
race_column = 'racePct' + race
if race == "Black":
    race_column = 'racepctblack'
if race == "Hispanic":
    race_column = 'racePctHisp'

df3 = df[['state', 'communityName', race_column, 'autoTheftPerPop', 'larcPerPop', 'arsonsPerPop', 'assaultPerPop']]

fig = make_subplots(rows=2, cols=2, subplot_titles=["AutoThefts", "Larcenies", "Arsons", "Assaults"])


fig.add_trace(go.Scatter(x=df3[race_column], y=df3['autoTheftPerPop'], hovertext=df3['communityName'], mode="markers", legendgroup=1, name="autotheft"), 1, 1)
fig.add_trace(go.Scatter(x=df3[race_column], y=df3['larcPerPop'], hovertext=df3['communityName'], mode="markers", legendgroup=2, name="larcenies"), 1, 2)
fig.add_trace(go.Scatter(x=df3[race_column], y=df3['arsonsPerPop'], hovertext=df3['communityName'], mode="markers", legendgroup=3, name="arsons"), 2, 1)
fig.add_trace(go.Scatter(x=df3[race_column], y=df3['assaultPerPop'], hovertext=df3['communityName'], mode="markers", legendgroup=4, name="assaults"), 2, 2)
fig.update_layout(margin=dict(l=0, r=0, t=100, b=0),
                  legend=dict(x=.5, xanchor="center"),
                  title="crimes by race",
                  width=1000,
                  height=800,
                  legend_orientation="h",
                  xaxis1_title=race + "Pct",
                  xaxis2_title=race + "Pct",
                  xaxis3_title=race + "Pct",
                  xaxis4_title=race + "Pct",
                  yaxis1_title="autoTheftPerPop",
                  yaxis2_title="larcPerPop",
                  yaxis3_title="arsonsPerPop",
                  yaxis4_title="assaultPerPop")
st.write(fig)

st.header("Unemployment influence on crime level")

unemployment_radio = st.radio("Choose job status", ('employed', 'unemployed'), key=100)


column = ""
if unemployment_radio == "employed":
    column = "PctEmploy"
else:
    column = "PctUnemployed"

df4 = df[['state', 'communityName', column, 'autoTheftPerPop', 'larcPerPop', 'arsonsPerPop', 'assaultPerPop']]

fig = make_subplots(rows=2, cols=2, subplot_titles=["AutoThefts", "Larcenies", "Arsons", "Assaults"])

fig.add_trace(go.Scatter(x=df4[column], y=df4['autoTheftPerPop'], hovertext=df4['communityName'], mode="markers", legendgroup=1, name="autotheft"), 1, 1)
fig.add_trace(go.Scatter(x=df4[column], y=df4['larcPerPop'], hovertext=df4['communityName'], mode="markers", legendgroup=2, name="larcenies"), 1, 2)
fig.add_trace(go.Scatter(x=df4[column], y=df4['arsonsPerPop'], hovertext=df4['communityName'], mode="markers", legendgroup=3, name="arsons"), 2, 1)
fig.add_trace(go.Scatter(x=df4[column], y=df4['assaultPerPop'], hovertext=df4['communityName'], mode="markers", legendgroup=4, name="assaults"), 2, 2)
fig.update_layout(margin=dict(l=0, r=0, t=100, b=0),
                  legend=dict(x=.5, xanchor="center"),
                  title="crimes by job status",
                  width=1000,
                  height=800,
                  legend_orientation="h",
                  xaxis1_title=column,
                  xaxis2_title=column,
                  xaxis3_title=column,
                  xaxis4_title=column,
                  yaxis1_title="autoTheftPerPop",
                  yaxis2_title="larcPerPop",
                  yaxis3_title="arsonsPerPop",
                  yaxis4_title="assaultPerPop",
                  hovermode="x unified")
st.write(fig)