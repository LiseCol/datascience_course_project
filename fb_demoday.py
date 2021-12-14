#Import common modules
import streamlit as st
import pandas as pd
pd.options.mode.chained_assignment = None
from PIL import Image
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import time

## Page config ##
st.set_page_config(page_title="Facebook ad Report", 
                   page_icon=":bar_chart:",
                   layout='wide',initial_sidebar_state='collapsed',)
st.markdown("""
 <!-- This example requires Tailwind CSS v2.0+ -->
<nav x-data="{ isOpen: false }" class="bg-gray-800">
  <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
    <div class="relative flex items-center justify-between h-16">
      <div class="absolute inset-y-0 left-0 flex items-center sm:hidden">
        <!-- Mobile menu button-->
        <button @click = "isOpen = !isOpen" type="button" class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white" aria-controls="mobile-menu" aria-expanded="false">
          <span class="sr-only">Open main menu</span>
          <!--
            Icon when menu is closed.

            Heroicon name: outline/menu

            Menu open: "hidden", Menu closed: "block"
          -->
          <svg x-show="!isOpen" x-bind:class=" !isOpen ? 'block' : 'hidden'" class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <!--
            Icon when menu is open.

            Heroicon name: outline/x

            Menu open: "block", Menu closed: "hidden"
          -->
          <svg x-show="isOpen" x-bind:class=" isOpen ? 'block' : 'hidden'" class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div class="flex-1 flex items-center justify-center sm:items-stretch sm:justify-start">
        <div class="flex-shrink-0 flex items-center">
          <img class="block lg:hidden h-8 w-auto" src="https://tailwindui.com/img/logos/workflow-mark-indigo-500.svg" alt="Workflow">
          <img class="hidden lg:block h-8 w-auto" src="https://tailwindui.com/img/logos/workflow-logo-indigo-500-mark-white-text.svg" alt="Workflow">
        </div>
        <div class="hidden sm:block sm:ml-6">
          <div class="flex space-x-4">
            <!-- Current: "bg-gray-900 text-white", Default: "text-gray-300 hover:bg-gray-700 hover:text-white" -->
            <a href="#" class="bg-gray-900 text-white px-3 py-2 rounded-md text-sm font-medium" aria-current="page">Dashboard</a>

            <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Team</a>

            <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Projects</a>

            <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Calendar</a>
          </div>
        </div>
      </div>
      <div class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
        <button type="button" class="bg-gray-800 p-1 rounded-full text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white">
          <span class="sr-only">View notifications</span>
          <!-- Heroicon name: outline/bell -->
          <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
        </button>
      </div>
    </div>
  </div>

  <!-- Mobile menu, show/hide based on menu state. -->
  <div x-show="isOpen" class="sm:hidden" id="mobile-menu">
    <div class="px-2 pt-2 pb-3 space-y-1">
      <!-- Current: "bg-gray-900 text-white", Default: "text-gray-300 hover:bg-gray-700 hover:text-white" -->
      <a href="#" class="bg-gray-900 text-white block px-3 py-2 rounded-md text-base font-medium" aria-current="page">Dashboard</a>

      <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium">Team</a>

      <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium">Projects</a>

      <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium">Calendar</a>
    </div>
  </div>
</nav>
""",unsafe_allow_html=True)
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
    
def ROAS_col(df):   
    df['ROAS'] = round(df['revenue $']/df['spend $'],2)

def custom_col_USD(df):
    df['CPA'] = round(df['spend $']/df['purchase'],2)
    df['CPM'] = round(df['spend $']/(df['impressions']/1000),2)
    df['CPC'] = round(df['spend $']/df['link click'],2) 
    df['CTR'] = round((df['link click']/df['impressions']),5)
    df['ROAS'] = round(df['revenue $']/df['spend $'],2)
    df['currency'] = 'USD'
    
def CPA_col(df):   
    df['CPA $'] = round(df['spend $']/df['purchase'],2)    
    
def df_clean(df):
    df.rename(columns = {'spend $':'spend','revenue $':'revenue','link click':'clicks'},inplace=True)
    df['CTR'] = df['CTR'].apply(lambda x: '{:.2%}'.format(x))
    for col in df.columns:
        if col == 'currency':
            df.drop(['currency'],axis=1,inplace=True)
        
def groupby_all(variable1,variable2,cur):
    # one variable only
    if variable2== 'None':
        df_var= load_data().groupby(variable1).agg(
                                        {'impressions':np.sum,
                                         'link click': np.sum,
                                         'spend $': np.sum,
                                      'purchase': np.sum, 
                                      'revenue $': np.sum}).reset_index()
        custom_col_USD(df_var)
        df_clean(df_var)
        return df_var
    else:
        if cur == "local":
            df_var= load_data().groupby([variable1,variable2]).agg(
                                        {'impressions':np.sum, 
                                      'link click': np.sum, 
                                      'spend': np.sum, 
                                      'purchase': np.sum, 
                                      'revenue': np.sum
                                     }).reset_index()
            custom_col(df_var)
            df_clean(df_var)
            return df_var
        else:
            df_var= load_data().groupby([variable1,variable2]).agg(
                                        {'impressions':np.sum,
                                         'link click': np.sum,
                                         'spend $': np.sum,
                                      'purchase': np.sum, 
                                      'revenue $': np.sum}).reset_index()
            custom_col_USD(df_var)
            df_clean(df_var)
            return df_var

def main():

    # Page title                   
    st.title("Facebook ad Report :bar_chart:")

    ## Sidebar
    st.sidebar.title("MENU")
    
    # Different pages
    country_report = st.sidebar.button('KPI per country')
    target_report = st.sidebar.button('KPI per target type')
    
    ## Reporting per country
    if country_report:
        status2 = st.radio("Select the prefered currency :",("Local","USD")) 
        ## In local currency
        if status2 == "Local":
            st.subheader("Grouped by country in local currency")
            with st.expander("See the data"):
                st.dataframe((groupby_all('country','currency','local').set_index('country')).style.format(subset=[
                                                        'spend', 'revenue', 'CPA','CPM','CPC', 'ROAS'],
                                                        formatter="{:,.2f}"))  
            ## Country per day
            st.subheader("Let's dive in:")
            col1, col2, col3 = st.columns(3)
            with col1: # Select date
                start_date, end_date = st.date_input('Date range:',[datetime.date(2021,11,1),datetime.date(2021,11,18)])
            
            
            with col2: # Selectbox country
                df_behaviour_country = groupby_all('country','date','local')
                all_countries = df_behaviour_country['country'].unique().tolist()
                options = st.selectbox('Country:', all_countries)
            
            with col3: # Select KPI
                KPI= ['CPA','revenue','ROAS']
                selected_KPI = st.selectbox("KPI:",KPI)
            
            ind_country = df_behaviour_country[df_behaviour_country['country']== options]
            mask = (ind_country['date'] >= (start_date).strftime('%Y-%m-%d')) & (ind_country['date'] <= (end_date).strftime('%Y-%m-%d'))
            ind_country = ind_country [mask]

            # Create plot
            fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    
            fig1.add_trace(
                    go.Bar(x=ind_country['date'],
                    y=ind_country['spend'],
                    name="Spend"),
                    secondary_y=False,
                )
        
            fig1.add_trace(
                    go.Scatter(x=ind_country['date'],
                    y=ind_country[selected_KPI], name= selected_KPI,
                    line_color='black'),
                    secondary_y=True,
                )

            fig1.update_xaxes(title_text="Days")
        
            fig1.update_yaxes(title_text="Spend", secondary_y=False)
            fig1.update_yaxes(title_text=selected_KPI, secondary_y=True)
            st.plotly_chart(fig1)

        ## In USD
        elif status2 == "USD":  
            st.subheader("Grouped by country in US dollar")
            with st.expander("See the data"):
                st.dataframe((groupby_all('country','currency','usd').set_index('country')).style.format(subset=[
                                                        'spend', 'revenue', 'CPA','CPM','CPC', 'ROAS'],
                                                        formatter="{:,.2f}"))
            # Metrics highlight

            #col1, col2, col3 = st.columns(3)
            #country = df_country_us[df_country_us['ROAS']==df_country_us['ROAS'].max()].index[0]
            #col1.metric("Top spender", '2', "1.2 °F")
            #col2.metric("Top CPA", "9 mph", "-8%")
            #col3.metric("Top ROAS", "86%", "4%")
        
            ## Country per day
            st.subheader("Daily view:")
            
            col1, col2, col3 = st.columns(3)
            with col1: # Select date
                start_date, end_date = st.date_input('Date range:',[datetime.date(2021,11,1),datetime.date(2021,11,18)])
            
            
            with col2: # Selectbox country
                df_behaviour_country = groupby_all('country','date','us')
                all_country = df_behaviour_country['country'].unique().tolist()
                options = st.selectbox('Country:', all_country)
            
            with col3: # Select KPI
                KPI= ['CPA','revenue','ROAS']
                selected_KPI = st.selectbox("KPI:",KPI)
            
            ind_country = df_behaviour_country[df_behaviour_country['country']== options]
            mask = (ind_country['date'] >= (start_date).strftime('%Y-%m-%d')) & (ind_country['date'] <= (end_date).strftime('%Y-%m-%d'))
            ind_country = ind_country[mask]

            # Create plot
            fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    
            fig2.add_trace(
                    go.Bar(x=ind_country['date'],
                    y=ind_country['spend'],
                    name="Spend"),
                    secondary_y=False,
                )
        
            fig2.add_trace(
                    go.Scatter(x=ind_country['date'],
                    y=ind_country[selected_KPI], name= selected_KPI,
                    line_color='black'),
                    secondary_y=True,
                )

            fig2.update_xaxes(title_text="Days")
        
            fig2.update_yaxes(title_text="Spend", secondary_y=False)
            fig2.update_yaxes(title_text=selected_KPI, secondary_y=True)
            
            st.plotly_chart(fig2)

    ## Reporting per target type
    elif target_report:
        st.subheader("View: Grouped by target type in local currency")
        with st.expander("See the data"):
            st.dataframe(groupby_all('target type','None','usd').set_index('target type').style.format(subset=[
                                                        'spend', 'revenue', 'CPA','CPM','CPC', 'ROAS'],
                                                        formatter="{:,.2f}"))
        # Metrics highlight
        
        ## Target type per day
        st.subheader("Daily view:")
            
        col1, col2, col3 = st.columns(3)
        with col1: # Select date
            start_date, end_date = st.date_input('Date range:',[datetime.date(2021,11,1),datetime.date(2021,11,18)])
            
            
        with col2: # Selectbox country
            df_behaviour_target = groupby_all('target type','date','local')
            all_target = df_behaviour_target['target type'].unique().tolist()
            options = st.selectbox('Target type:', all_target)
            
        with col3: # Select KPI
            KPI= ['CPA','revenue','ROAS']
            selected_KPI = st.selectbox("KPI:",KPI)
            
        ind_target = df_behaviour_target[df_behaviour_target['target type']== options]
        mask = (ind_target['date'] >= (start_date).strftime('%Y-%m-%d')) & (ind_target['date'] <= (end_date).strftime('%Y-%m-%d'))
        ind_target = ind_target[mask]

        # Create plot
        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    
        fig3.add_trace(
                    go.Bar(x=ind_target['date'],
                    y=ind_target['spend'],
                    name="Spend"),
                    secondary_y=False,
                )
        
        fig3.add_trace(
                    go.Scatter(x=ind_target['date'],
                    y=ind_target[selected_KPI], name= selected_KPI,
                    line_color='black'),
                    secondary_y=True,
                )
        
        fig3.update_xaxes(title_text="Days")
        
        fig3.update_yaxes(title_text="Spend", secondary_y=False)
        fig3.update_yaxes(title_text=selected_KPI, secondary_y=True)
        
        st.plotly_chart(fig3)
    
    else:
        st.subheader(':arrow_left: To start: Select a page on the side bar')
main()  