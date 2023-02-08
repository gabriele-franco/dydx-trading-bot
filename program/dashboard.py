import streamlit as st 
import pandas as pd 

storico= pd.read_json('/home/ubuntu/storico.json')
bot_agent=pd.read_json('/home/ubuntu/bot_agents.json')
storico['profit']=storico['base_tot']+storico['quote_tot']

total_profit=storico['profit'].sum()
open_positions=len(bot_agent['pair_status'])*2

st.title('total profit is {total_profit}')
st.title('the number of live orders is {open_positions}')
st.write('this is the storico ordini')
st.dataframe(storico)

st.write('these should be the live orders')
st.title('bot_agent')

st.dataframe(bot_agent)
