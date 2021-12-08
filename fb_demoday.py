#Import common modules
import streamlit as st
import pandas as pd
pd.options.mode.chained_assignment = None
from PIL import Image

import numpy as np
import plotly.express as px

def get_percentages(df,name_column):
    percentage = df[name_column].value_counts(normalize=True)*100
    percentage = percentage.reset_index()
    percentage.columns = [name_column,'percentage']
    percentage = percentage.sort_values(by=name_column)
    return percentage

##############################################################################################
# PAGE STYLING
##############################################################################################
st.set_page_config(page_title="Titanic Dashboard ", 
                   page_icon=":ship:",
                   layout='wide')
                   
st.title("Welcome to the ***Titanic*** dashboard! : :star:")
"""
MY TEXT MY TEXT
"""
# Page styling

st.markdown("Let's ask the following question: ***'Can we use Python to retrive information from the titanic?' ***")

st.header("**Overall information from Titanic**")
"""
Bla bla bla information from Titanic bla bla bla"""


# Data loading and first checks
df = pd.read_csv('data_clean_2.csv', index_col=0)
color_list = ['DarkCyan', 'GreenYellow', 'Orchid']
