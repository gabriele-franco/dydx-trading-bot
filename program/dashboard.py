import streamlit as st 
import pandas as pd 

storico= pd.read_json('storico.json')

bot_agent=pd.read_json('bot_agents.json')

st.dataframe(storico)
st.dataframe(bot_agent)
