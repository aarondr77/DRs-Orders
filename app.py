import streamlit as st
import pandas as pd
from io import BytesIO
from mitosheet.public.v3 import *
import plotly.express as px
import requests


col1, mid, col2 = st.columns([1,3,20])
with col1:
    st.image('./icon.png', width=100)
with col2:
    st.title("DR's Orders")


st.write("As a DR, these are your DR's orders. Follow your orders everyday and send a picture to the chill fam group chat to prove it.")

st.write("""
- 50 pushups
- 1 minute plank
- 30 lunges
- pickup someting that weight over 30 lbs
""")

r = requests.get('https://docs.google.com/spreadsheet/ccc?key=1VovrfntPTD8y0g978D_pbCp2kr4Lg_7MmhnkecSKIgE&output=csv')
data = r.content

df = pd.read_csv(BytesIO(data), index_col=0)

# Reset df index
df = df.reset_index()

# Renamed columns Date
df.rename(columns={'index': 'Date'}, inplace=True)

# Unpivoted df into df_unpivoted
df_unpivoted = df.melt(id_vars=['Date'])

# Filled NaN values in 1 columns in df_unpivoted
df_unpivoted.fillna({'value': 0}, inplace=True)

# Replace x with 1 in df_unpivoted
df_unpivoted = df_unpivoted.astype(str).replace("(?i)x", "1", regex=True).astype(df_unpivoted.dtypes.to_dict())

# Pivoted df_unpivoted into df_unpivoted_pivot
df_unpivoted_pivot = pd.DataFrame(data={})

# Renamed columns Person
df_unpivoted.rename(columns={'variable': 'Person'}, inplace=True)

# Changed value to dtype float
df_unpivoted['value'] = to_float_series(df_unpivoted['value'])

# Pivoted df_unpivoted into score
tmp_df = df_unpivoted[['value', 'Person']].copy()
pivot_table = tmp_df.pivot_table(
    index=['Person'],
    values=['value'],
    aggfunc={'value': ['sum']}
)
pivot_table = pivot_table.set_axis([flatten_column_header(col) for col in pivot_table.keys()], axis=1)
score = pivot_table.reset_index()


# Construct the graph and style it. Further customize your graph by editing this code.
# See Plotly Documentation for help: https://plotly.com/python/plotly-express/
fig = px.bar(score, x='Person', y='value sum')
fig.update_layout(
        title='Scoreboard', 
        xaxis={
            "showgrid": False
        }, 
        yaxis={
            "title": 'Number of Days', 
            "showgrid": False
        }, 
        legend={
            "orientation": 'v'
        }, 
        barmode='group', 
        paper_bgcolor='#FFFFFF'
    )
st.plotly_chart(fig)
