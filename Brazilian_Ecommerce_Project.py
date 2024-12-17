
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from ydata_profiling import ProfileReport
from sklearn.preprocessing import LabelEncoder
from streamlit_pandas_profiling import st_profile_report

# Load models
try:
    model_classification = joblib.load('Brazilian_Ecommerce_Classification.bkl')
    model_clustering = joblib.load('Brazilian_Ecommerce_Clustering.bkl')
except Exception as e:
    st.error(f"Error loading models: {e}")

# Sidebar to navigate between EDA, Classification, and Clustering
sidebar = st.sidebar
mode = sidebar.radio('Mode', ['EDA', 'Classification', 'Clustering'])
st.markdown("<h1 style='text-align: center; color: #ff0000;'></h1>", unsafe_allow_html=True)

if mode == "EDA":
    def main():
        # Header of Customer Satisfaction Prediction
        html_temp = """<div style="background-color:#F5F5F5">
                    <h1 style="color:#31333F;text-align:center;"> Prediksi Kepuasan Pelanggan </h1>
                    </div>"""
        
        # Sidebar to upload CSV files
        with st.sidebar.header('Unggah File CSV Anda'):
            uploaded_file = st.sidebar.file_uploader('Unggah file CSV input Anda')

        if uploaded_file is not None:
            # Read file and Put headers
            EDA_sample = pd.read_csv(uploaded_file, index_col=0)
            pr = ProfileReport(EDA_sample, explorative=True)
            st.header('*Input DataFrame*')
            st.write(EDA_sample)
            st.write('---')
            st.header('*Pandas Profiling Report*')
            st_profile_report(pr)
        
        else:
            st.info('Menunggu file CSV diunggah.')

    if __name__ == '__main__':
        main()

if mode == "Classification":

    # Define function to predict classification based on assigned features
    def predict_satisfaction(freight_value, product_description_lenght, product_photos_qty, payment_type, payment_installments, payment_value, 
    estimated_days, arrival_days, arrival_status, seller_to_carrier_status, estimated_delivery_rate, arrival_delivery_rate, shipping_delivery_rate):

        prediction_classification = model_classification.predict(pd.DataFrame({'freight_value' :[freight_value], 'product_description_lenght' :[product_description_lenght], 'product_photos_qty' :[product_photos_qty], 'payment_type' :[payment_type], 'payment_installments' :[payment_installments], 'payment_value' :[payment_value], 'estimated_days' :[estimated_days], 'arrival_days' :[arrival_days], 'arrival_status' :[arrival_status], 'seller_to_carrier_status' :[seller_to_carrier_status], 'estimated_delivery_rate' :[estimated_delivery_rate], 'arrival_delivery_rate' :[arrival_delivery_rate], 'shipping_delivery_rate' :[shipping_delivery_rate]}))
        return prediction_classification

    def main():
        # Header of Customer Satisfaction Prediction
        html_temp = """<div style="background-color:#F5F5F5">
                    <h1 style="color:#31333F;text-align:center;"> Prediksi Kepuasan Pelanggan </h1>
                    </div>"""
        st.markdown(html_temp,unsafe_allow_html=True)
        
        # Assign all features with desired data input method
        sidebar.title('Numerical Features')
        product_description_lenght = sidebar.slider('Panjang Deskripsi Produk (Panjang deskripsi produk dalam karakter. Deskripsi yang lebih detail dapat mempengaruhi kepuasan pelanggan.)', 4, 3990, 100)
        product_photos_qty = sidebar.slider('Jumlah Foto Produk (Jumlah foto yang tersedia untuk produk. Lebih banyak foto dapat meningkatkan kepercayaan pelanggan.)', 1, 20, 1)
        payment_installments = sidebar.slider('Jumlah Cicilan (Jumlah pembayaran cicilan yang dipilih pelanggan.)', 1, 24, 1)
        estimated_days = sidebar.slider('Perkiraan Hari Pengiriman (Jumlah hari yang diperkirakan untuk pengiriman produk.)', 3, 60, 1)
        arrival_days = sidebar.slider('Hari Aktual Kedatangan (Jumlah hari aktual yang dibutuhkan produk untuk sampai.)', 0, 60, 1)
        payment_type = st.selectbox('Jenis Pembayaran', ['credit_card', 'boleto', 'voucher', 'debit_card']) 
        st.caption('Metode pembayaran yang dipilih pelanggan.')
        arrival_status = st.selectbox('Status Kedatangan', ['OnTime/Early', 'Late'])
        st.caption('Apakah produk tiba tepat waktu atau terlambat.')
        seller_to_carrier_status = st.selectbox('Status Pengiriman Pnejual', ['OnTime/Early', 'Late'])
        st.caption('Apakah penjual mengirim produk tepat waktu.')
        estimated_delivery_rate = st.selectbox('Tingkat Perkiraan Pengiriman', ['Very Slow', 'Slow', 'Neutral', 'Fast', 'Very Fast'])
        st.caption('Kecepatan pengiriman dibandingkan dengan perkiraan awal.')
        arrival_delivery_rate = st.selectbox('Tingkat Kedatangan Barang', ['Very Slow', 'Slow', 'Neutral', 'Fast', 'Very Fast'])
        st.caption('Kecepatan aktual pengiriman produk.')
        shipping_delivery_rate = st.selectbox('Tingkat Pengiriman', ['Very Slow', 'Slow', 'Neutral', 'Fast', 'Very Fast'])
        st.caption('Kualitas keseluruhan proses pengiriman.')
        payment_value = st.text_input('Nilai Pembayaran', '')
        st.caption('Total nilai pembayaran yang dilakukan pelanggan.')
        freight_value = st.text_input('Biaya Pengiriman', '')
        st.caption('Biaya pengiriman untuk pesanan.')
        result = ''

        # Predict Customer Satisfaction
        if st.button('Predict_Satisfaction'):
            result = predict_satisfaction(freight_value, product_description_lenght, product_photos_qty, payment_type, payment_installments, payment_value, 
                                        estimated_days, arrival_days, arrival_status, seller_to_carrier_status, estimated_delivery_rate, arrival_delivery_rate, shipping_delivery_rate)
                                      

            if result == 0:
                result = 'Tidak Puas'
                st.success(f'Pelanggan {result}')
            else:
                result = 'Puas'
                st.success(f'Pelanggan {result}')

    if __name__ == '__main__':
        main()

if mode == "Clustering":

    # Define function to predict clustering based on features
    def predict_clustering(freight_value, price, payment_value, payment_installments, payment_sequential):
        prediction_clustering = model_clustering.predict(pd.DataFrame({'freight_value': [freight_value], 'price': [price], 'payment_installments': [payment_installments], 'payment_value': [payment_value], 'payment_sequential': [payment_sequential]}))
        return prediction_clustering

    def main():
        # Header of Customer Segmentation
        html_temp = """<div style="background-color:#F5F5F5">
                        <h1 style="color:#31333F;text-align:center;"> Customer Segmentation </h1>
                        </div>"""
        st.markdown(html_temp, unsafe_allow_html=True)

        # Sidebar to choose the clustering input mode (data or file)
        # Sidebar to choose the clustering input mode (data or file)
        selected_clustering_mode = sidebar.radio(
            'Select Clustering Mode',
            ['Input Data', 'Input File'],
            key=f'clustering_mode_{mode}'
        )


        # Mode 3: Clustering - Input Data
        if selected_clustering_mode == 'Input Data':
            payment_installments = st.slider('Jumlah Cicilan', 1, 24, 1)
            st.caption('Berapa kali pelanggan memilih untuk membagi pembayaran.')
            payment_sequential = st.slider('Urutan Pembayaran', 1, 24, 1)
            st.caption('Urutan pembayaran dalam serangkaian cicilan.')
            freight_value = st.text_input('Biaya Pengiriman', '')
            st.caption('Total biaya pengiriman untuk pesanan.')
            price = st.text_input('Harga Produk', '')
            st.caption('Harga produk yang dibeli pelanggan.')
            payment_value = st.text_input('Nilai Pembayaran', '')
            st.caption('Total jumlah yang dibayarkan pelanggan.')
            result_cluster = ''

            if st.button('Prediksi Cluster'):
                result_cluster = predict_clustering(freight_value, price, payment_value, payment_installments, payment_sequential)
                st.success(f'Customer Cluster is {result_cluster}')

                # Display the description based on the predicted cluster
                if result_cluster == 0:
                    st.write("*Cluster 0:*")
                    st.write("Cluster ini berisi pelanggan dengan daya beli moderat hingga tinggi.")
                    st.write("*Rekomendasi:* Tawarkan produk premium dan promosi pengiriman gratis.")
                    
                elif result_cluster == 1:
                    st.write("*Cluster 1:*")
                    st.write("Pelanggan di cluster ini sering membeli produk mahal dan lebih memilih cicilan.")
                    st.write("*Rekomendasi:* Berikan opsi cicilan fleksibel dan fokus pada produk premium.")
                    
                elif result_cluster == 2:
                    st.write("*Cluster 2:*")
                    st.write("Cluster ini terdiri dari pelanggan yang sensitif terhadap harga.")
                    st.write("*Rekomendasi:* Tawarkan produk terjangkau dan promosi pengiriman dengan biaya rendah.")

        # Mode 4: Clustering by File
        elif selected_clustering_mode == 'Input File':
            # Upload CSV file
            with st.sidebar.header('Unggah File CSV Anda'):
                uploaded_file = st.sidebar.file_uploader('Unggah File CSV Input Anda')

            if uploaded_file is not None:
                # Read dataset
                sample = pd.read_csv(uploaded_file, index_col=0)

                # Define sidebar for clustering algorithm
                selected_algorithm = sidebar.selectbox('Pilih Algoritma Clustering', ['K-Means', 'Agglomerative'])

                # Define sidebar for number of clusters
                selected_clusters = 3

                # Define sidebar for PCA
                use_pca = sidebar.radio('Use PCA', ['No', 'Yes'])

                # Drop freight values with zeros
                sample.drop(sample[sample.freight_value == 0].index, inplace=True)
                sample.reset_index(inplace=True, drop=True)

                # Handle Skewness in sample data
                for i in ['freight_value', 'price', 'payment_value', 'payment_installments', 'payment_sequential']:
                    sample[i] = np.log10(sample[i])

                if 'category_column' in sample.columns:
                    le = LabelEncoder()
                    sample['category_column'] = le.fit_transform(sample['category_column'])

                # One-hot encoding for categorical columns without order
                sample = pd.get_dummies(sample, drop_first=True)

                sample_numeric = sample.select_dtypes(include=[np.number])

                # Check if there are any non-numeric columns in the data
                if sample_numeric.empty:
                    st.error("No numeric data available for scaling.")
                else:
                    # Apply standard scaler to numeric data
                    sc = StandardScaler(with_mean=False)
                    data_scaled = sc.fit_transform(sample_numeric)

                # Drop rows with any NaN values
                sample_cleaned = sample.dropna()

                # Proceed with scaling and clustering
                sample_numeric = sample_cleaned.select_dtypes(include=[np.number])
                sc = StandardScaler(with_mean=False)
                data_scaled = sc.fit_transform(sample_numeric)

                # Select number of clusters
                if selected_algorithm == 'Agglomerative':
                    hc = AgglomerativeClustering(n_clusters=selected_clusters)
                    y_pred_hc = hc.fit_predict(data_scaled)

                else:
                    kmean = KMeans(n_clusters=selected_clusters)
                    y_pred_kmean = kmean.fit_predict(data_scaled)

                # Apply PCA
                pca = PCA(n_components=2)
                data_pca = pca.fit_transform(data_scaled)

                # Select number of clusters for PCA
                kmean_pca = KMeans(n_clusters=selected_clusters)
                y_pred_pca = kmean_pca.fit_predict(data_pca)

                def plot_cluster(data, y_pred, num_clusters):
                    # Plot Clusters
                    fig, ax = plt.subplots()
                    Colors = ['red', 'green', 'blue', 'purple', 'orange', 'royalblue', 'brown', 'grey', 'chocolate', 'fuchsia']
                    for i in range(num_clusters):
                        ax.scatter(data[y_pred == i, 0], data[y_pred == i, 1], c=Colors[i], label='Cluster ' + str(i + 1))

                    ax.set_title('Customers Clusters')
                    ax.legend(loc='upper left', prop={'size': 5})
                    ax.axis('off')
                    st.pyplot(fig)

                # Plot clusters based on selected algorithm and PCA
                if use_pca == 'No' and selected_algorithm == 'K-Means':
                    plot_cluster(data_scaled, y_pred_kmean, selected_clusters)

                elif use_pca == 'No' and selected_algorithm == 'Agglomerative':
                    plot_cluster(data_scaled, y_pred_hc, selected_clusters)

                else:
                    plot_cluster(data_pca, y_pred_pca, selected_clusters)

                # Cluster Descriptions and Recommendations as Table
                st.write("### Cluster Descriptions and Recommendations")

                # Define a list of descriptions and recommendations
                cluster_descriptions = [
                    {"Cluster": "Cluster 0", 
                     "Description": "Cluster ini berisi pelanggan dengan daya beli yang moderat hingga tinggi, cenderung membeli produk dengan harga menengah hingga tinggi dan lebih jarang memilih pembayaran cicilan.", 
                     "Recommendation": "Fokus pada produk dengan harga terjangkau dan tawarkan pilihan cicilan untuk memudahkan pelanggan melakukan pembelian."},
                    
                    {"Cluster": "Cluster 1", 
                     "Description": "Cluster 1 berisi pelanggan dengan daya beli yang moderat hingga tinggi dan lebih sering memilih pembayaran cicilan.", 
                     "Recommendation": "Tawarkan produk premium dengan opsi cicilan menarik dan promosi pengiriman gratis untuk meningkatkan loyalitas pelanggan."},
                    
                    {"Cluster": "Cluster 2", 
                     "Description": "Cluster ini berisi pelanggan yang cenderung membeli produk dengan harga tinggi dan memilih pembayaran cicilan, dengan pengeluaran untuk pengiriman yang lebih tinggi.", 
                     "Recommendation": "Tawarkan produk premium dengan opsi cicilan, serta promosi pengiriman gratis untuk meningkatkan pengalaman belanja mereka."},
                ]

                # Convert the list to a pandas DataFrame
                df_cluster_info = pd.DataFrame(cluster_descriptions)

                # Display the DataFrame as a table
                st.table(df_cluster_info)

            else:
                st.info('Awaiting for CSV file to be uploaded.')

    if __name__ == '__main__':
        main()
