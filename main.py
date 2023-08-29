try:
    import streamlit as st
    import pandas as pd
except ModuleNotFoundError:
    print("Kedua modul belum ada")

st.title("Market Basket Analyzer - Modified 1")
st.subheader("Powered by Naufal-Web")