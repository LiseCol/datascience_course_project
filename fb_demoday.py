#Import common modules
import streamlit as st
import pandas as pd
pd.options.mode.chained_assignment = None
from PIL import Image
import numpy as np
import plotly.express as px

## Page config ##
st.set_page_config(page_title="Facebook ad Report", 
                   page_icon=":bar_chart:",
                   layout='wide')
# Define functions
@st.cache
def load_data():
    df = pd.read_csv('data_clean_2.csv', index_col=0)
    return  df

#color_list = ['DarkCyan', 'GreenYellow', 'Orchid']

# Define functions
def custom_col(df):
    df['CPA'] = round(df['spend']/df['purchase'],2)
    df['CPM'] = round(df['spend']/(df['impressions']/1000),2)
    df['CPC'] = round(df['spend']/df['link click'],2)
    df['CTR'] = round((df['link click']/df['impressions']) ,5)
    df['ROAS'] = round(df['revenue']/df['spend'],2)

def custom_col_USD(df):
    df['CTR'] = round((df['link click']/df['impressions']),5)
    df['ROAS'] = round(df['revenue $']/df['spend $'],2)
    df['CPA $'] = round(df['spend $']/df['purchase'],2)
    df['CPM $'] = round(df['spend $']/(df['impressions']/1000),2)
    df['CPC $'] = round(df['spend $']/df['link click'],2)
    
def df_clean(df):
    df.rename(columns = {'spend $':'spend','revenue $':'revenue'},inplace=True)
    df['CTR'] = df['CTR'].apply(lambda x: '{:.2%}'.format(x))
    to_change = ['spend','revenue','CPA','CPM','CPC']
    for col in to_change:
        for value in df[df.loc[:,'currency']=='USD'].loc[:,col]: 
            df.loc[:,col].replace(value,"${:,.2f}".format(value),inplace=True)
        for value in df[df.loc[:,'currency']=='EUR'].loc[:,col]: 
            df.loc[:,col].replace(value,"€{:,.2f}".format(value),inplace=True)
    df.drop(['currency'],axis=1,inplace=True)
        
def groupby_all(variable,cur):
    # one variable only
    if cur == "local":
        df_var = load_data().groupby([variable]).agg(
                                        {'impressions':np.sum, 
                                      'link click': np.sum, 
                                      'spend': np.sum, 
                                      'purchase': np.sum, 
                                      'revenue': np.sum,
                                     'currency':pd.Series.mode}).reset_index()
        custom_col(df_var)
        df_clean(df_var)
        return df_var
    
    else:
        df_var= load_data().groupby([variable]).agg(
                                        {'impressions':np.sum,
                                         'link click': np.sum,
                                         'spend $': np.sum,
                                      'purchase': np.sum, 
                                      'revenue $': np.sum,
                                     'currency':pd.Series.mode}).reset_index()
        custom_col_USD(df_var)
        df_clean(df_var)
        return df_var

def main():

    # Page title                   
    st.title("Facebook ad Report :bar_chart:")

    # Add sth into sidebar
    text = """
    :arrow_forward: **To start**: \n
    Don't forget to select your favorite filters\n
    ---------------------\n
    `This dashboard is based on a sample of 2 months facebook historical data.`\n
    ---------------------
    """
    st.sidebar.markdown(text)


    # Selectbox : View of the dataframe
    st.sidebar.subheader("FILTERS")

    status = st.sidebar.selectbox('Select your favorite view:',["Performance per country",
                                                            "Performance per target type",
                                                            "Daily view"])

    status2 = st.sidebar.radio("Select the prefered currency :",("Local currency","USD"))

    if status == "Performance per country":
        if status2 == "Local currency":
            st.subheader("Performance per country")
            st.dataframe((groupby_all('country','local').set_index('country'))
                         #.style.format(
                          #  subset=['impressions','link click','spend','purchase','revenue','CPA','CPM','CPC','ROAS'], 
                           #  formatter="{:,}"))
            
        if status2 == "USD":  
            st.subheader("Performance per country")
            st.dataframe(groupby_all('country','usd').set_index('country'))

    elif status == "Performance per target type":
        if status2 == "Local currency":
            st.subheader("Performance per target type")
            st.dataframe(groupby_all('target type','local').set_index('target type'))
        if status2 == "USD":  
            st.subheader("Performance per target type")
            st.dataframe(groupby_all('target type','usd').set_index('target type'))
        
    elif status == "Daily view":
        if status2 == "Local currency":
            st.subheader("Daily view")
            st.dataframe(groupby_all('date','local').set_index('date'))
        if status2 == "USD":  
            st.subheader("Daily view")
            st.dataframe(groupby_all('date','usd').set_index('date'))

                                                                                  
    # Static plots in two columns
    col1, col2 = st.columns(2)

    with col1:
        # View per country
        st.subheader('Per country')
        df_behaviour_countries = load_data().groupby(['country','date']).agg(
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
        df_behaviour_target = load_data().groupby(['target type','date']).agg(
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

st.write(main())   