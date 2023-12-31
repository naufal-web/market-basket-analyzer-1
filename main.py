try:
    import streamlit as st
    import pandas as pd
    import random as rd
except ModuleNotFoundError:
    print("Ketiga modul belum ada")

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
    with st.expander("Tampilan file CSV"):
        st.write(csv_readable_file)

    # tampilkan fitur deskripsi file
    with st.expander("Deskripsi file CSV"):
        st.write(f"Jumlah baris data terdiri atas {len(csv_readable_file)} baris data")
        st.write(f"Jumlah kolom data terdiri atas {len(csv_readable_file.columns)} kolom data")

    def function_input(truth_value):
        freq_item_set = 0
        min_sup_percentage = 0
        min_con_percentage = 0
        value = truth_value
        if value == 0:
            with st.expander("Tampilan input pengguna"):
                while True:
                    freq_item_set = st.text_input("Masukkan jumlah frequent itemset")
                    min_sup_percentage = st.text_input("Masukkan minimal support dalam persen (%) "
                                                       "yang akan digunakan untuk proses analisis.")
                    min_con_percentage = st.text_input("Masukkan minimal confidence dalam persen (%) "
                                                       "yang akan digunakan untuk proses analisis")
                    if freq_item_set == "  " and min_sup_percentage == "  " and min_con_percentage == "  ":
                        continue
                    elif min_sup_percentage == "  " and min_con_percentage == "  ":
                        continue
                    elif min_con_percentage == "  ":
                        continue
                    else:
                        break
        elif value == 1:
            i = 0
            while True:
                freq_item_set = rd.randint(1, 6)
                min_sup_percentage = rd.randint(1, 5)
                min_con_percentage = rd.randint(1, 5)
                i += 1
                if freq_item_set >= 3 and min_sup_percentage >= 3 and min_con_percentage >= 3:
                    break
                else:
                    pass
        else:
            pass

        return freq_item_set, min_sup_percentage, min_con_percentage


    col1, col2, col3, col4 = st.columns([2, 3, 5, 6])
    with col1:
        st.button("User", key="user")
    with col2:
        st.button("Computer", key="computer")

    freq_item_set = 0
    min_sup = 0
    min_conf = 0

    if st.session_state["user"]:
        freq_item_set, min_sup, min_conf = function_input(0)
        st.info(f"""
        Frequent itemset   : {freq_item_set} item \n
        Minimal support    : {min_sup}% \n
        Minimal confidence : {min_conf}% \n
        """)

    elif st.session_state["computer"]:
        freq_item_set, min_sup, min_conf = function_input(1)
        st.info(f"""\
Frequent itemset   : {freq_item_set} item \n
Minimal support    : {min_sup}% \n
Minimal confidence : {min_conf}% \n """)
    else:
        pass

    # deklarasikan variabel num
    # num = 0
    freq_item_set = int(freq_item_set)
    min_sup = int(min_sup)
    min_con = int(min_conf)
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

        freg_item_set = 0
        for index, row in readable_file[:number].iterrows():
            products = row["produk"].title().split(",")
            temp.append(products)

        return temp


    # deklarasikan fitur buat list produk yang sering dibeli dari list produk dengan list bersarang
    def create_one_product_frequent_list(product_list):
        product_list = product_list
        product_frequent_list = []

        for i in range(len(product_list)):
            for j in range(len(product_list[i])):
                product_frequent_list.append(product_list[i][j])

        return product_frequent_list

    def create_two_product_frequent_list(product_list):
        product_list = product_list
        product_frequent_list = []

        for i in range(len(product_list)):
            for j in range(len(product_list[i])):
                product_frequent_list.append([product_list[i][j], product_list[i][j-1]])

        return product_frequent_list

    def create_three_product_frequent_list(product_list):
        product_list = product_list
        product_frequent_list = []

        for i in range(len(product_list)):
            for j in range(len(product_list[i])-1):
                product_frequent_list.append(
                    {product_list[i][j], product_list[i][j - 1], product_list[i][j - 2]})

        return list(product_frequent_list)


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
        # num_itemset = num_itemset
        product_stock_list = []

        for product in product_distinctive_list:
            product_stock_list.append(product_frequent_list.count(product))


        return product_stock_list


    # deklarasikan fitur tampilkan produk beserta stok yang terjual berdasarkan minimal support yang ditetapkan user
    def create_stock_based_products(product_distinctive_list, product_stock_list, frequent_itemset):
        frequent_itemset = frequent_itemset
        product_distinctive_list = product_distinctive_list # list tunggal
        product_stock_list = product_stock_list # list tunggal
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

    product_frequent_list = create_one_product_frequent_list(product_list)

    st.info(f"Jumlah stok yang terjual : {len(product_frequent_list)} unit")

    product_distinctive_list = create_product_distinctive_list(product_frequent_list)

    st.info(f"Jumlah produk : {len(product_distinctive_list)} produk")

    product_stock_list = create_product_stock_list(product_distinctive_list, product_frequent_list)
    min_sup_product_list, one_itemset_list = create_stock_based_products(product_distinctive_list,
                                                                         product_stock_list,
                                                                         freq_item_set)

    # st.info(len(product_frequent_list))
    if min_sup > 0:
        with st.expander(f"Tampilan data produk dengan itemset = 1 dan minimal support sebesar "
                         f"{min_sup}% "):
            if len(one_itemset_list) > 0:
                st.info(f"Jumlah produk min-sup dengan itemset 1 : {len(one_itemset_list)}")
                for min_sup_product in min_sup_product_list:
                    st.write(min_sup_product)
            else:
                pass

    two_itemset_list = []
    three_itemset_list = []

    if len(one_itemset_list) > 1:

        two_itemset_list = []

        for index in range(len(one_itemset_list)):
            two_itemset_list.append([one_itemset_list[index], one_itemset_list[index-1]])

        frequent_two_item_list = create_two_product_frequent_list(product_list)

        # two_dist_itemset_list = []

        dist_two_itemset_list = [
            list(two_itemset_list)
            for two_itemset_list in set(frozenset(two_itemset) for two_itemset in two_itemset_list)]

        two_itemset_num = []

        dist_two_itemset_list.sort(reverse=False)
        frequent_two_item_list.sort(reverse=False)
        for dist_two_itemset in dist_two_itemset_list:
            two_itemset_num.append(frequent_two_item_list.count(dist_two_itemset))

        two_itemset_min_sup_product_list, two_itemset_list = create_stock_based_products(dist_two_itemset_list,
                                                                                         two_itemset_num, freq_item_set)

        with st.expander(f"Tampilan data produk dengan itemset = 2 dan minimal support sebesar "
                         f"{min_sup}% "):
            if len(two_itemset_min_sup_product_list) > 0:
                st.info(f"Jumlah produk min-sup dengan itemset 2 : {len(two_itemset_min_sup_product_list)}")
                for two_fixed_itemset in two_itemset_list:
                    st.write(f"{', '.join(two_fixed_itemset)}")
            else:
                pass

    if len(two_itemset_list) > 1:
        three_itemset_list = []

        frequent_three_item_list = create_three_product_frequent_list(product_list)

        for index1 in range(len(two_itemset_list)):
            for index2 in range(len(two_itemset_list[index1])):
                three_itemset_list.append({two_itemset_list[index1][index2],
                                           two_itemset_list[index1][index2-1],
                                           two_itemset_list[index1][index2-2]})

        dist_three_itemset_list = [
            list(three_itemset_list)
            for three_itemset_list in set(frozenset(three_itemset) for three_itemset in three_itemset_list)]

        three_itemset_num = []
        dist_three_itemset_list.sort(reverse=False)
        frequent_three_item_list.sort(reverse=False)
        for dist_three_itemset in dist_three_itemset_list:
            three_itemset_num.append(frequent_three_item_list.count(set(dist_three_itemset)))

        three_itemset_min_sup_product_list, three_itemset_list = create_stock_based_products(
            dist_three_itemset_list, three_itemset_num, freq_item_set)

        with st.expander(f"Tampilan data produk dengan itemset = 3 dan minimal support sebesar "
                         f"{min_sup}% "):
            if len(three_itemset_min_sup_product_list) > 0:
                st.info(f"Jumlah produk min-sup dengan itemset 3 : {len(three_itemset_min_sup_product_list)}")
                for three_fixed_itemset in three_itemset_list:
                    st.write(f"{', '.join(three_fixed_itemset)}")
            else:
                pass

    with st.expander("Simpulan dan saran"):

        st.info(f"Jumlah transaksi dengan 1 barang : {len(one_itemset_list)} transaksi")
        for index, one_itemset in enumerate(one_itemset_list):
            st.write(f" {index+1}. {one_itemset} ")

        st.info(f"Jumlah transaksi dengan 2 barang : {len(two_itemset_list)} transaksi")
        for index, two_itemset in enumerate(two_itemset_list):
            st.write(f" {index + 1}. {two_itemset} ")

        st.info(f"Jumlah transaksi dengan 3 barang : {len(three_itemset_list)} transaksi")
        for index, three_itemset in enumerate(three_itemset_list):
            st.write(f" {index + 1}. {three_itemset} ")

except ValueError:
    st.write("Selamat mencoba")