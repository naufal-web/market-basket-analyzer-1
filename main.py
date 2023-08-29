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
    csv_file = st.file_uploader("Unggah file", type="csv", label_visibility="hidden")
try:
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

    num = 0
    min_sup = 0

    col1, col2, col3 = st.columns([0.3, 0.3, 0.4])

    with col1:
        st.button("Masukkan dengan angka bilangan bulat", key="integer")
    with col2:
        st.button("Masukkan dengan angka desimal", key="float")

    if st.session_state["float"]:
        pass
    else:
        # deklarasikan variabel num untuk menyimpan data berupa angka padahal string
        num = st.text_input("Masukkan jumlah data yang akan digunakan untuk proses analisis")
        try:
            num = int(num)
        except ValueError:
            st.write("Angka belum diinput oleh Anda")

        # atur logika variabel num
        try:
            if num <= 0:
                st.write("Angka tidak valid")
            else:
                st.write("Angka valid")
        except TypeError:
            pass

        min_sup = st.text_input("Masukkan nilai minimal support")
        try:
            min_sup = int(min_sup)
        except ValueError:
            st.write("Angka belum diinput oleh Anda")

        try:
            if min_sup <= 0:
                st.write("Angka tidak valid")
            else:
                st.write("Angka valid")
        except TypeError:
            pass


    # deklarasikan fitur tampilan data berdasarkan angka yang diinput oleh user
    def display_partial_data(number, file):
        # ambil data number ke dalam variabel number
        # ambil data file ke dalam variabel file
        number = number
        file = file
        # readable_file = pd.read_csv(file)
        try:
            first_transaction = file[:number]
            st.write(first_transaction)
        except TypeError:
            pass


    # deklarasikan fitur buat list product berdasarkan angka yang diinput oleh user serta hasilkan list tersebut
    def create_product_list(number, file):
        # ambil data number ke dalam variabel number
        # ambil data file ke dalam variabel file
        number = number
        readable_file = file

        temp = []

        for index, row in readable_file[:number].iterrows():
            products = row["produk"].title().split(",")
            temp.append(products)

        return temp


    # deklarasikan fitur buat list produk yang sering dibeli dari list produk dengan list bersarang
    def create_product_frequent_list(product_list):
        product_list = product_list
        product_frequent_list = []

        for i in range(len(product_list)):
            for j in range(len(product_list[i])):
                product_frequent_list.append(product_list[i][j])

        return product_frequent_list


    # deklarasikan fitur buat list produk dari list produk yang sering dibeli serta hasilkan list tersebut
    def create_product_distinctive_list(product_frequent_list):
        product_frequent_list = product_frequent_list
        product_distinctive_list = []

        for product in product_frequent_list:
            if product not in product_distinctive_list:
                product_distinctive_list.append(product)

        return product_distinctive_list


    # deklarasikan fitur buat list stok keluar produk dari list produk dan list produk yang sering dibeli serta hasilkan
    # list tersebut
    def create_product_stock_list(product_distinctive_list, product_frequent_list):
        product_distinctive_list = product_distinctive_list
        product_frequent_list = product_frequent_list
        product_distinctive_list.sort(reverse=False)
        product_stock_list = []

        for product in product_distinctive_list:
            product_stock_list.append(product_frequent_list.count(product))

        return product_stock_list


    # deklarasikan fitur tampilkan produk beserta stok yang terjual berdasarkan minimal support yang ditetapkan user
    def display_products_and_stocks(product_distinctive_list, product_stock_list, minimal_support):
        product_distinctive_list = product_distinctive_list
        product_stock_list = product_stock_list
        minimal_support = minimal_support

        for product, stock in zip(product_distinctive_list, product_stock_list):
            try:
                if minimal_support <= stock:
                    st.write(f"{product} {stock} pcs")
                else:
                    pass
            except TypeError:
                st.write("Angka minimal support belum dimasukkan")


    with st.expander(f"Tampilkan file CSV dengan {num} transaksi"):
        display_partial_data(num, csv_readable_file)

    product_list = create_product_list(int(num), csv_readable_file)
    product_frequent_list = create_product_frequent_list(product_list)
    product_distinctive_list = create_product_distinctive_list(product_frequent_list)
    product_stock_list = create_product_stock_list(product_distinctive_list, product_frequent_list)

    with st.expander(f"Tampilkan daftar produk berserta stok yang terjual dengan minimal support sebesar {min_sup} pcs"):
        display_products_and_stocks(product_distinctive_list, product_stock_list, min_sup)
except ValueError:
    pass