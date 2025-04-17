from backend.classes import *
import streamlit as st

# pages
main_page = st.Page("./pages/main_page.py", title="Wildfires")
page_2 = st.Page("./pages/user_page.py", title="User Panel")

# Nav
pg = st.navigation([main_page, page_2])

# Set Wide Mode
st.set_page_config(layout="wide")

# Run
pg.run()
