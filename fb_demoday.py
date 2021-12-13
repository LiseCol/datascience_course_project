#Import common modules
import streamlit as st
import pandas as pd
pd.options.mode.chained_assignment = None
from PIL import Image
import numpy as np
import plotly.express as px
import datetime

## Page config ##
st.set_page_config(page_title="Facebook ad Report", 
                   page_icon=":bar_chart:",
                   layout='wide')
# Define functions
@st.cache
def load_data():
    df = pd.read_csv('data_clean_3.csv', index_col=0)
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
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
    df['CPA'] = round(df['spend $']/df['purchase'],2)
    df['CPM'] = round(df['spend $']/(df['impressions']/1000),2)
    df['CPC'] = round(df['spend $']/df['link click'],2) 
    df['CTR'] = round((df['link click']/df['impressions']),5)
    df['ROAS'] = round(df['revenue $']/df['spend $'],2)
    df['currency'] = 'USD'
    
def df_clean(df):
    df.rename(columns = {'spend $':'spend','revenue $':'revenue','link click':'clicks'},inplace=True)
    df.drop(['currency'],axis=1,inplace=True)
    df['CTR'] = df['CTR'].apply(lambda x: '{:.2%}'.format(x))
        
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
    st.sidebar.subheader("FILTERS")
    
    # Selectbox : View of the dataframe
    status = st.sidebar.selectbox('Select your favorite KPI view:',["Per country",
                                                            "Per target type",
                                                            "Per day"])
    # Reporting per country
    if status == "Per country":
        status2 = st.sidebar.radio("Select the prefered currency :",("Local currency","USD"))    
        # In local currency
        if status2 == "Local currency":
            st.subheader("Per country - Local currency")
            st.dataframe((groupby_all('country','local').set_index('country')).style.format(subset=[
                                                        'spend', 'revenue', 'CPA','CPM','CPC', 'ROAS'],
                                                        formatter="{:,.2f}"))   
        # In USD
        elif status2 == "USD":  
            st.subheader("Per country - USD")
            st.dataframe((groupby_all('country','us').set_index('country')).style.format(subset=[
                                                        'spend', 'revenue', 'CPA','CPM','CPC', 'ROAS'],
                                                        formatter="{:,.2f}"))
        # Metrics highlight
        st.write("## Here's a single figure")
        metric("Metric 0", 0)

        st.write("## ... and here's a row of them")
        metric_row(
        {
        ("Metric 1": 100, "1.2 °F"),
        ("Metric 2": 200, "-8%"),
        ("Metric 3": 300,"4%")
        },
        )
        
        #col1, col2, col3 = st.columns(3)
        #col1.metric("Top spender", "70 °F", "1.2 °F")
        #col2.metric("Top CPA", "9 mph", "-8%")
        #col3.metric("Top ROAS", "86%", "4%")
        
        # Country per day
        st.subheader('Which country are you interested in diving in?')
        
        df_behaviour_countries = load_data().groupby(['country','date']).agg(
                                        {'spend $': np.sum,
                                         'revenue $': np.sum,
                                        'purchase': np.sum}
                                        ).reset_index()

        all_countries = df_behaviour_countries['country'].unique().tolist()
        options = st.selectbox('Select', all_countries)
        ind_country = df_behaviour_countries[df_behaviour_countries['country']== options]

        fig1 = px.bar(ind_country, 
                      x = "date", 
                      y = ["spend $","revenue $"])
        fig1.update_yaxes(visible=False, fixedrange=True)
        fig1.update_layout(barmode='group')
        st.plotly_chart(fig1)

    # Reporting per country
    elif status == "Per target type": 
        # In USD
        st.subheader("Per target type - USD")
        st.dataframe((groupby_all('target type','usd').set_index('target type')).style.format(subset=[
                                                        'spend', 'revenue', 'CPA','CPM','CPC', 'ROAS'],
                                                        formatter="{:,.2f}"))
        # Metrics highlight
        
        # Target type per day
        st.subheader('Which target type are you interested in diving in?')
        df_behaviour_target = load_data().groupby(['target type','date']).agg(
                                        {'spend $': np.sum,
                                         'revenue $': np.sum,
                                        'purchase': np.sum}
                                        ).reset_index()

        all_target = df_behaviour_target['target type'].unique().tolist()
        options = st.selectbox('Select', all_target)
        ind_target = df_behaviour_target[df_behaviour_target['target type']== options]

        fig2 = px.bar(ind_target, 
                      x = "date", 
                      y = ["spend $","revenue $"])
        fig2.update_yaxes(visible=False, fixedrange=True)
        fig2.update_layout(barmode='group')
        st.plotly_chart(fig2)    
    
    # Reporting per day
    elif status == "Per day":
        # In USD
        st.subheader("Per day - USD")
        # Add date selector
        start_date, end_date = st.date_input('Choose your date range  :',[datetime.date(2021,11,1),datetime.date(2021,11,18)])
        df_daily = groupby_all('date','usd')
        mask = (df_daily['date'] >= (start_date).strftime('%Y-%m-%d')) & (df_daily['date'] <= (end_date).strftime('%Y-%m-%d'))
        
        # Display DF
        st.dataframe(df_daily[mask].set_index('date').style.format(subset=[
                                                        'spend', 'revenue', 'CPA','CPM','CPC', 'ROAS'],
                                                        formatter="{:,.2f}"))
 
main()  