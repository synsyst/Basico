import streamlit as st

st.title("simple web app")
number = st.slider("pick a number", 0, 50)

st.write(f"you picked as your {number}")

