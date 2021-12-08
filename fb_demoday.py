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

# Static plots in two columns
col1, col2 = st.columns(2)

with col1:
    df_behaviour_countries = df.groupby(['country','date']).agg(
                                        {'spend $': np.sum,
                                         'revenue $': np.sum,
                                        'purchase': np.sum}
                                        ).reset_index()
    def split_country(country):
        return df_behaviour_countries[df_behaviour_countries['country']==country]

    st.subheader('KPI behaviour according to country')
    fig = fig = px.bar(split_country('ES'), 
                 x = "date", 
                 y = ["spend $","revenue $"],title='Spain')
    fig.update_yaxes(visible=False, fixedrange=True)

    fig.update_layout(barmode='group')
    st.plotly_chart(fig)

with col2:
    st.markdown('test')