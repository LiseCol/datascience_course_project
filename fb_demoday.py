#Import common modules
import streamlit as st
import pandas as pd
pd.options.mode.chained_assignment = None
from PIL import Image

import numpy as np
import plotly.express as px

##############################################################################################
# PAGE STYLING
##############################################################################################
st.set_page_config(page_title="Best facebook reporting ever ", 
                   page_icon=":star:",
                   layout='wide')
                   
st.title("Welcome to my dashboard! : :star:")
"""
MY TEXT MY TEXT
"""
# Page styling

st.markdown("Let's make some test: ***'hello' ***")

st.header("**Overall information about my dashboard**")
"""
Bla bla bla information about facebook bla bla bla"""

# Data loading and first checks
df = pd.read_csv('data_clean_2.csv', index_col=0)
color_list = ['DarkCyan', 'GreenYellow', 'Orchid']

st.title('KPIs evolutions')
# Static plots in two columns
col1, col2 = st.columns(2)

with col1:
    # View per country
    st.subheader('Per country')
    df_behaviour_countries = df.groupby(['country','date']).agg(
                                        {'spend $': np.sum,
                                         'revenue $': np.sum,
                                        'purchase': np.sum}
                                        ).reset_index()

    all_countries = df_behaviour_countries['country'].unique().tolist()
    options = st.selectbox('Which country are you interested in diving in?', all_countries)

    # Filter the information for this port specifically
    ind_country = df_behaviour_countries[df_behaviour_countries['country']== options]

    fig1 = px.bar(ind_country, 
                 x = "date", 
                 y = ["spend $","revenue $"])
    fig1.update_yaxes(visible=False, fixedrange=True)

    fig1.update_layout(barmode='group')
    st.plotly_chart(fig1)

with col2:    
    st.subheader('Per target type')
    df_behaviour_target = df.groupby(['target type','date']).agg(
                                        {'spend $': np.sum,
                                         'revenue $': np.sum,
                                        'purchase': np.sum}
                                        ).reset_index()

    all_target = df_behaviour_target['target type'].unique().tolist()
    options = st.selectbox('Which target type are you interested in diving in?', all_target)

    # Filter the information for this port specifically
    ind_target = df_behaviour_target[df_behaviour_target['target type']== options]

    fig2 = px.bar(ind_target, 
                 x = "date", 
                 y = ["spend $","revenue $"])
    fig2.update_yaxes(visible=False, fixedrange=True)

    fig2.update_layout(barmode='group')
    st.plotly_chart(fig2)
    