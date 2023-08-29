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
    csv_file = st.file_uploader("Unggah file CSV", type="csv")

# deklarasikan variabel file csv
csv_readable_file = pd.read_csv(csv_file)

# tampilkan fitur display file
with st.expander("Tampilkan file CSV"):
    st.write(csv_readable_file)

# tampilkan fitur deskripsi file
with st.expander("Deskripsi file CSV"):
    st.write(f"Jumlah baris data terdiri atas {len(csv_readable_file)} baris")

# deklarasikan variabel num
# num = 0

# deklarasikan variabel num untuk menyimpan data berupa angka padahal string
num = st.text_input("Masukkan jumlah data yang akan digunakan untuk proses analisis")
num = int(num)

# atur logika variabel num
if num <= 0:
    st.write("Angka tidak valid")
else:
    st.write("Angka valid")






