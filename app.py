import streamlit as st
from apps import home,eda,forecast
from multiapp import MultiApp

app = MultiApp()

# Add all your application here
app.add_app('Intro', home.app)
app.add_app('Explore Data', eda.app)
app.add_app('Forecast', forecast.app)

# The main app
app.run()