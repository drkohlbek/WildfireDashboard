import streamlit as st
from backend.middle import stats, figure

st.markdown("# Wildfires in the United States")
st.plotly_chart(figure, height=700, theme=None)

st.markdown("#### Totals")
string = "##### Wildfire Count: &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; {:20,.0f}".format(
    stats["total_fires"])
st.markdown(string)
st.markdown("##### Acres Covered: &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; {:20,.0f}".format(
    stats["total_acres"]))
st.markdown("##### Estimated Supression Cost: &ensp;&nbsp; ${:20,.2f}".format(
    stats["estimated_cost"]))
