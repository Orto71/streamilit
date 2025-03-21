import streamlit as st

st.header('st.button')

if st.button('Say hello'):
     st.write('Why hello there')
else:
     st.write('Goodbye')

press=st.button('Ciao')
if press:st.write("Ciao")
