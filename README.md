# FP-Big-Data-DataLakehouse

## Project Overview
Proyek ini bertujuan untuk melakukan klasterisasi pelanggan menggunakan data streaming real-time. Arsitektur solusi terdiri dari komponen utama seperti Kafka, MinIO, PySpark ML, dan Streamlit. Data akan dikirim, disimpan, dan diproses untuk menghasilkan output berupa klaster pelanggan.

## Architecture Diagram


## Komponen Utama:
1. Dataset: Data awal dalam format CSV atau JSON.
2. Kafka Broker: Untuk streaming data real-time.
3. MinIO: Penyimpanan data mentah dan versi delta.
4. PySpark ML: Digunakan untuk proses klasterisasi.
5. Streamlit : Sebagai UI untuk klasterisasi
6. Deepnote : Untuk daily routine (Deepnote Scheduler)
7. Output: Hasil berupa klaster pelanggan


## Requirements
### Software Dependencies:
1. Docker (Optional for Kafka and MinIO setup)
2. Apache Kafka
3. MinIO
4. Apache Spark (PySpark)
5. Python Libraries:
	- pandas
	- kafka-python
	- boto3
	- pyspark

## Project Setup
### Step 1: Setup Kafka Broker
Using Docker :
Syarat : 
1. Docker harus sudah terinstal di sistem
2. Buat docker-compose.ymlfile. Berikut adalah contoh docker-compose.ymlfile untuk menyiapkan broker Kafka dengan Zookeeper (Kafka memerlukan Zookeeper untuk menjalankannya):

```
version: '3.8'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper
    container_name: zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  kafka:
    image: confluentinc/cp-kafka
    container_name: kafka
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  minio:
    image: minio/minio
    container_name: minio
    ports:
      - "9000:9000"
    environment:
      MINIO_ROOT_USER: minio_user
      MINIO_ROOT_PASSWORD: minio_password
    command: server /data
    volumes:
      - minio_data:/data

volumes:
  minio_data:
```

3. Jalankan broker Kafka dan Zookeeper menggunakan Docker Compose : Jalankan perintah berikut untuk menjalankan kedua layanan:
```
docker-compose up -d
```
4. Verifikasi bahwa kontainer berjalan
```
docker ps
```
5. Membuat topic kafka 
```
docker exec -it <kafka_container_id> kafka-topics.sh --create --topic test-topic --partitions 1 --replication-factor 1 --zookeeper zookeeper:2181
```

### Step 2: Setup MinIO (Object Storage)
1. Install MinIO:
```
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
./minio server ./data
```
2. Akses MinIO di http://localhost:9000.

Step 3: Klasterisasi dengan PySpark ML
1. Setup PySpark
```
pip install pyspark
```
2. Load Data dari MinIO ke PySpark:
```
Code Pyspark Machine Learning ada pada folder diatas
```

### Step 3 
1. Instal Streamlit 
```
pip install streamlit
```
2. Membuat aplikasi Streamlit untuk analisis data e-commerce dan klasifikasi pelanggan berdasarkan model pembelajaran mesin (machine learning). Aplikasi ini dibagi menjadi tiga mode utama di sidebar: Exploratory Data Analysis (EDA), Classification, dan Clustering.
```
Code ada di folder diatas = 'Brazillian_E-commerce_Project.py
```

## Running the Project
1. Jalankan Kafka dan buat topik.
Jalankan kafka dan zookeeper menggunakan docker ```docker compose up -d```<br>
notes : pastikan kafka, zookeeper sudah running

2. Streaming data ke Kafka.
Melakukan streaming dengan menjalankan ```producer.py``` untuk load dataset dan setelah itu jalankan ```consumer.py``` untuk membuat batch untuk menyimpan dataset yang akan langsung disimpan di minio

3. Jalankan MinIO sebagai object storage.
Jalankan minio di terminal dengan command ```minio server start``` dan buka halaman web minio pada ```http://localhost:9000```<br>
Pada halaman web minio akan otomatis ada hasil dari streaming tadi yaitu berbentuk batch

4. Proses data dengan PySpark ML.
Membuat code Machine learning ( ex: use Kaggle ) yang akan secara langsung terhubung dengan minio dan bisa membaca data yang ada di minio.<br>
Notes : untuk menghubungkan bisa menggunakan ```ngrok http 9000``` atau langsung dari localhost minio

Hasil running pyspark ML :<br>
Notebook big_data2.ipynb digunakan untuk melakukan eksplorasi data, preprocessing, melatih model, dan menghasilkan file seperti:<br>
- Brazilian_Ecommerce_Classification.bkl (model klasifikasi).
- Brazilian_Ecommerce_Clustering.bkl (model clustering).
File-file ini akan digunakan sebagai input untuk aplikasi Streamlit.

5. Jalankan kode python menggunakan streamlit untuk mengarahkan ke UI untuk operasi EDA, Clustering dan Classification. 

```
python3 streamlit Brazilian_Ecommerce_Project.py
```
Notes : pada folder yang sama juga harus terdapat file Brazilian_Ecommerce_Clustering dan Brazilian_Ecommerce_Classification

6. Melakukan pengaturan scheduling (Deepnote Scheduler) untuk mengolah datanya realtime




