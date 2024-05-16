import streamlit as st

st.title("simple web app")
number = st.slider("pick a number", 0, 50)

st.write(f"you picked as your {number}")

apikey = st.secrets["myAPIKey"]
st.write(f"also the api key is {apikey}, though it's fake and it just tests the secrets functionality of streamlit")