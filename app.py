import streamlit as st
from apps import home
from multiapp import MultiApp

app = MultiApp()

# Add all your application here
app.add_app('Home', home.app)

# The main app
app.run()