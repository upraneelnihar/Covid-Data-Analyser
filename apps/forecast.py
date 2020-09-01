import streamlit as st
from .eda import load_state_wise_data
import datetime
import pandas as pd
import altair as alt
from fbprophet import Prophet


def app():
    st.title('Forecast')
    st.markdown('In this page we will use a `Prophet` model to forecast the virus spread.')
    st.markdown('**Inputs:**')
    st.markdown('1. `cutoff_date`: Date from which the forecast needs to be generated(all the data before this date is used as training data')
    st.markdown('2. `ndays`: no of days you want to forecast')

    cutoff_date = st.date_input('Enter the cutoff date', datetime.date(2020, 6, 1))
    ndays = st.number_input(label="Enter No of days you want to forecast:", min_value=10, max_value=100)

    compute_forecasts = st.button("Compute Forecast and Display Output")

    if compute_forecasts:
        compute_state = st.text('Computing Forecast...')
        df_daily = load_state_wise_data()
        df_input = (df_daily[df_daily['Status'] == 'Confirmed']
                    .get(['Date','TT'])
                    .rename(columns={'Date':'ds','TT':'y'}))

        # Train Prophet Model
        df_train = df_input[df_input['ds'] < pd.Timestamp(cutoff_date)]
        model = Prophet()
        model.fit(df_train)

        # Perform prediction
        df_predict = model.make_future_dataframe(periods=ndays)
        df_fcst = model.predict(df_predict)

        df_actuals = df_input[df_input['ds'] <= df_predict['ds'].max()]

        st.write(df_fcst[['ds','yhat','yhat_lower','yhat_upper']])
        compute_state.text('Computing Forecast......done!')