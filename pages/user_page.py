import streamlit as st
import pandas as pd
from backend.middle import top_three, fires_dict, stack
# package to format long numbers, i.e. 6,400 -> 6.4k
from millify import millify
# Cache fire data, otherwise streamlit deletes it every time you change the text_input()


@st.cache_data
def get_top_three(_top_three):
    return [fire.return_dict() for fire in _top_three]


@st.cache_data
def get_fires_df(_fires_dict):
    return pd.DataFrame(_fires_dict)


# extract variables from functions
fire1, fire2, fire3 = get_top_three(top_three)

df = get_fires_df(fires_dict)

st.markdown("# User Dashboard")

st.markdown("## Highest Priority Fires")

a, b, c = st.columns(3)
a.metric(f"{fire1["IncidentName"]}, ID: {fire1["ID"]}", f"Acres Covered: {millify(fire1["Acres"], precision=1)}",
         "Estimated Cost: ${:20,.2f}".format(fire1["Estimated Cost"]), border=True)
b.metric(f"{fire2["IncidentName"]}, ID: {fire2["ID"]}", f"Acres Covered: {millify(fire2["Acres"], precision=1)}",
         "Estimated Cost: ${:20,.2f}".format(fire2["Estimated Cost"]), border=True)
c.metric(f"{fire3["IncidentName"]}, ID: {fire3["ID"]}", f"Acres Covered: {millify(fire3["Acres"], precision=1)}",
         "Estimated Cost: ${:20,.2f}".format(fire3["Estimated Cost"]), border=True)


st.markdown("## Complete List of Fires")
st.markdown(
    "Hover over the table and click the search icon to find a specific fire by ID or any other field.")


table = st.dataframe(df, hide_index=True, column_config={
                     "CurrentDate": None, "InitialLatitude": None, "InitialLongitude": None, "FireBehaviorGeneral": None, "FireCauseSpecific": None, "IncidentShortDescription": None})


st.markdown("#### Get fire by ID")
id = st.number_input(
    "Enter the ID of the fire to get detailed information on the event", value=38144)
user_dict = stack.get_by_ID(id)

st.table(user_dict)
