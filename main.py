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
        st.write(f"Jumlah baris data terdiri atas {len(csv_readable_file)} baris data")
        st.write(f"Jumlah kolom data terdiri atas {len(csv_readable_file.columns)} kolom")

    # deklarasikan variabel num
    # num = 0
    freq_itemset = st.text_input("Masukkan jumlah frequent itemset")
    min_sup_percentage = st.text_input("Masukkan minimal support dalam persen (%) "
                                       "yang akan digunakan untuk proses analisis.")
    min_con_percentage = st.text_input("Masukkan minimal confidence dalam persen (%) "
                                       "yang akan digunakan untuk proses analisis")

    freq_itemset = int(freq_itemset)
    min_sup = int(min_sup_percentage)
    min_con = int(min_con_percentage)
    count_of_transaction = len(csv_readable_file)


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
    def create_stock_based_products(product_distinctive_list, product_stock_list, frequent_itemset):
        frequent_itemset = frequent_itemset
        product_distinctive_list = product_distinctive_list
        product_stock_list = product_stock_list
        min_sup_list = []
        itemset_list = []
        for product, stock in zip(product_distinctive_list, product_stock_list):
            try:
                if frequent_itemset <= stock:
                    min_sup_list.append(f"{product} {int(stock)} pcs")
                    itemset_list.append(product)
            except TypeError:
                pass
        return min_sup_list, itemset_list

    product_list = create_product_list(int(count_of_transaction), csv_readable_file)

    st.info(f"Jumlah transaksi : {len(product_list)} transaksi")

    product_frequent_list = create_product_frequent_list(product_list)

    st.info(f"Jumlah stok yang terjual : {len(product_frequent_list)} unit")

    product_distinctive_list = create_product_distinctive_list(product_frequent_list)

    st.info(f"Jumlah produk : {len(product_distinctive_list)} produk")

    product_stock_list = create_product_stock_list(product_distinctive_list, product_frequent_list)
    min_sup_product_list, one_itemset_list = create_stock_based_products(product_distinctive_list,
                                                                         product_stock_list,
                                                                         freq_itemset)

    # st.info(len(product_frequent_list))
    with st.expander(f"Tampilan data produk dengan itemset = 1 dan minimal support sebesar "
                     f"{min_sup}% "):
        if len(one_itemset_list) > 0:
            st.info(f"Jumlah produk min-sup dengan itemset 1 : {len(one_itemset_list)}")
            for min_sup_product in min_sup_product_list:
                st.write(min_sup_product)
        else:
            pass

    two_itemset_list = []

    for i in range(len(one_itemset_list)):
        for j in range(len(one_itemset_list)):
            if one_itemset_list[i] == one_itemset_list[j]:
                pass
            else:
                two_itemset_list.append([one_itemset_list[i], one_itemset_list[j]])

    two_dist_itemset_list = [list(two_itemset_list) for two_itemset_list in set(frozenset(two_itemset_list)
                                                                                for two_itemset in two_itemset_list)]
    if len(two_itemset_list) > 0:
        st.info(len(two_itemset_list))
    else:
        pass

    two_frequent_item_list = []
    count = 0
    for product in product_list:
        for index in range(len(two_itemset_list)):
            if two_itemset_list[index][0] and two_itemset_list[index][1] in product:
                if two_itemset_list[index][0] != two_itemset_list[index][1]:
                    count = count + 1
                    two_frequent_item_list.append([two_itemset_list[index][0],
                                                   two_itemset_list[index][1]])
                else:
                    pass
            else:
                pass

    if len(two_dist_itemset_list) > 0 and len(two_frequent_item_list) > 0:
        st.info(len(two_dist_itemset_list))
        st.info(len(two_frequent_item_list))
    else:
        pass

    two_itemset_num = create_product_stock_list(two_dist_itemset_list, two_frequent_item_list)
    two_itemset_min_sup_product_list, two_itemset_list = create_stock_based_products(two_dist_itemset_list,
                                                                                     two_itemset_num, freq_itemset)

    with st.expander(f"Tampilan data produk dengan itemset = 2 dan minimal support sebesar "
                     f"{round(min_sup)}% "):
        if len(two_itemset_min_sup_product_list) > 0:
            st.info(f"Jumlah produk min-sup dengan itemset 2 : {len(two_itemset_min_sup_product_list)}")
            for two_fixed_itemset in two_itemset_list:
                st.write(f"{' '.join(two_fixed_itemset)}")
        else:
            pass

    with st.expander("Simpulan dan saran"):
        for one_itemset in one_itemset_list:
            st.write(f"Restock barang ini ya : {one_itemset} ")


except ValueError:
    st.write("Selamat mencoba")