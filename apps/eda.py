import streamlit as st
import altair as alt
import pandas as pd

@st.cache()
def load_city_codes():
    df = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
    df_codes = df[['State', 'State_code']].drop_duplicates()
    df_codes['State']= df_codes['State'].replace({"Total": 'India'})
    state_codes = {row['State'] : row['State_code'] 
                        for _,row in df_codes.iterrows()}
    return state_codes

def plot_altair_chart(df, x_name, y_name):
    chart = alt.Chart(df).mark_line().encode(
                x=x_name,
                y=y_name
            )
    st.altair_chart(chart, use_container_width=True)

@st.cache
def load_state_wise_data():
    df_daily = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise_daily.csv')
    df_daily['Date'] = pd.to_datetime(df_daily['Date'], format='%d-%b-%y')
    return df_daily

def app():
    st.title('Exploration Data Analysis')
    st.markdown('In this page we will visualize the covid numbers for `Confirmed`, `Deceased`, `Recovered` at `All India` and `State` level.')

    df_daily = load_state_wise_data()
    state_codes = load_city_codes()
    
    city = st.sidebar.selectbox('Choose a city', options=list(state_codes.keys()))

    if city:
        df_confirmed = df_daily[df_daily['Status'] == 'Confirmed'][['Date', state_codes[city]]]
        df_recovered = df_daily[df_daily['Status'] == 'Recovered'][['Date', state_codes[city]]]
        df_deceased = df_daily[df_daily['Status'] == 'Deceased'][['Date', state_codes[city]]]

        x_name='Date'
        y_name=state_codes[city]

        st.markdown('## Confirmed Cases')
        plot_altair_chart(df_confirmed,x_name,y_name)

        st.markdown('## Recovered Cases')
        plot_altair_chart(df_recovered,x_name,y_name)

        st.markdown('## Deaths Cases')
        plot_altair_chart(df_deceased,x_name,y_name)