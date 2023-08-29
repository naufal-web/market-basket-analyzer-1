try:
    import streamlit as st
    import pandas as pd
except ModuleNotFoundError:
    print("Kedua modul belum ada")

# tampilkan judul program
st.title("Market Basket Analyzer - Modified 1")
# tampilkan subheader
st.subheader("Powered by Naufal-Web")

# tampilkan fitur unggah file
with st.expander("Unggah file CSV"):
    csv_file_readable = st.file_uploader("Unggah file CSV", type="csv")

# tampilkan fitur display file
with st.expander("Tampilkan file CSV"):
    st.write(pd.read_csv(csv_file_readable))
