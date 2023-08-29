try:
    import streamlit as st
    import pandas as pd
except ModuleNotFoundError:
    print("Kedua modul belum ada")

st.title("Market Basket Analyzer - Modified 1")
st.subheader("Powered by Naufal-Web")

with st.expander("Unggah file CSV"):
    csv_file_readable = st.file_uploader("Unggah file CSV", type="csv")
