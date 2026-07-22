import streamlit as st
st.title('Executive Overview')
cols=st.columns(4)
cols[0].metric('Backlog Value','$405K')
cols[1].metric('Open Lines','97')
cols[2].metric('Late Lines','26')
cols[3].metric('Average Age','10 Days')
