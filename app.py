import streamlit as st
from apps import home,eda
from multiapp import MultiApp

app = MultiApp()

# Add all your application here
app.add_app('Home', home.app)
app.add_app('Home', eda.app)

# The main app
app.run()