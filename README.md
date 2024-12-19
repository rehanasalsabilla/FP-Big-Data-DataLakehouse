# 🚀 FP-Big-Data-DataLakehouse

## Kelompok 3 - Big Data (B)
Anggota : 
| Nama           | NRP           |
|----------------|---------------|
| Mutiara Nurhaliza  | 5027221010    |
| Rehana Putri Salsabilla   | 5027221015   |
| Etha Felisya Br Purba  | 5027221017 |
| Salsabila Amalia Harjanto  | 5027221023  |

## 📝 Project Overview
Proyek ini bertujuan untuk melakukan **klasterisasi pelanggan** menggunakan data streaming real-time. Solusi ini menggabungkan berbagai teknologi modern seperti **Kafka**, **MinIO**, **PySpark ML**, dan **Streamlit** untuk menghasilkan klaster pelanggan secara efisien. 💡

---

## 🏗️ Architecture Diagram
![Architecture Diagram](https://github.com/user-attachments/assets/af435289-8dc1-4b35-a4c1-fb1fe4f74a58)

---

## 🔧 Komponen Utama:
1. 📂 **Dataset**: Data awal dalam format CSV atau JSON.
2. 📡 **Kafka Broker**: Untuk streaming data real-time.
3. ☁️ **MinIO**: Penyimpanan data mentah dan versi delta.
4. 🔍 **PySpark ML**: Untuk proses klasterisasi.
5. 📊 **Streamlit**: UI interaktif untuk klasterisasi.
6. 📅 **Deepnote**: Untuk penjadwalan rutin harian (Deepnote Scheduler).
7. 🎯 **Output**: Hasil berupa klaster pelanggan.

---

## 📋 Requirements

### 📦 Software Dependencies:
1. 🐳 **Docker** *(Opsional untuk Kafka dan MinIO setup)*.
2. 🖥️ **Apache Kafka**.
3. ☁️ **MinIO**.
4. 🔥 **Apache Spark** (PySpark).
5. 🐍 **Python Libraries**:
   - `pandas` 📄
   - `kafka-python` 📡
   - `boto3` 🛠️
   - `pyspark` 🔍

---

## ⚡ Project Setup

### ⚙️ Step 1: Setup Kafka Broker
1. **Pastikan Docker terinstal** 🐳.
2. Buat docker-compose.ymlfile. Berikut adalah contoh `docker-compose.yml` file untuk menyiapkan broker Kafka dengan Zookeeper (Kafka memerlukan Zookeeper untuk menjalankannya):

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

### ⚙️ Step 2: Setup MinIO
1. Install MinIO:
```
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
./minio server ./data
```
2. Akses MinIO di 🌐 [http://localhost:9000](http://localhost:9000).

### ⚙️ Step 3: Klasterisasi dengan PySpark ML
1. Setup PySpark
```
pip install pyspark
```
2. Load Data dari MinIO ke PySpark:
```
Code Pyspark Machine Learning ada pada folder diatas
```

### ⚙️ Step 4: Setup Streamlit
1. Instal Streamlit 
```
pip install streamlit
```
2. Membuat aplikasi Streamlit untuk analisis data e-commerce dan klasifikasi pelanggan berdasarkan model pembelajaran mesin (machine learning). Aplikasi ini dibagi menjadi tiga mode utama di sidebar: Exploratory Data Analysis (EDA), Classification, dan Clustering.
```
Code ada di folder diatas = 'Brazillian_E-commerce_Project.py
```

## 🏃‍♂️ Running the Project
### 1. **Jalankan Kafka, zookeper dan buat topik**  
Jalankan kafka dan zookeeper menggunakan docker ```docker compose up -d```<br>
notes : pastikan kafka, zookeeper sudah running
#### Docker-compose-up ✅ 
![Docker-compose-up](https://github.com/user-attachments/assets/e322cda9-2d82-4b21-994c-942da171f8a8)

#### Running Docker
![Running Docker](https://github.com/user-attachments/assets/373a449c-6341-43ce-b92f-8d48ddc1e7b7)


### 2. **Streaming Data ke Kafka**
Melakukan streaming dengan menjalankan ```producer.py``` untuk load dataset dan setelah itu jalankan ```consumer.py``` untuk membuat batch untuk menyimpan dataset yang akan langsung disimpan di minio

#### start producer py
![start producer py](https://github.com/user-attachments/assets/9c93495e-7315-46d4-aeb0-29b8ad8fce01)

#### Producer Running 🔄  
![Running producer py](https://github.com/user-attachments/assets/c3e7051d-4615-4456-8c16-84f40ab92ac5)

#### start+result consumer py
![start+result consumer py](https://github.com/user-attachments/assets/230fa7d6-4387-43c1-bf76-7438bb3e3e95)


### 3. **Jalankan MinIO sebagai object storage.**
Jalankan minio di terminal dengan command ```minio server start``` dan buka halaman web minio pada ```http://localhost:9000```<br>
Pada halaman web minio akan otomatis ada hasil dari streaming tadi yaitu berbentuk batch

#### Start Minio Server
![Start Minio Server](https://github.com/user-attachments/assets/bd15afea-e2d4-497b-a3a1-02c16ac2fd7f)

#### Localhost-minio-server
[Localhost-minio-server](https://github.com/user-attachments/assets/8b44b565-9e05-4660-9c5f-1df92db1d429)


### 4. **Proses data dengan PySpark ML.**
Membuat code Machine learning ( ex: use Kaggle ) yang akan secara langsung terhubung dengan minio dan bisa membaca data yang ada di minio.<br>
Notes : untuk menghubungkan bisa menggunakan ```ngrok http 9000``` atau langsung dari localhost minio

Hasil running pyspark ML :<br>
Notebook big_data2.ipynb digunakan untuk melakukan eksplorasi data, preprocessing, melatih model, dan menghasilkan file seperti:<br>
- Brazilian_Ecommerce_Classification.bkl (model klasifikasi).
- Brazilian_Ecommerce_Clustering.bkl (model clustering). <br>
File-file ini akan digunakan sebagai input untuk aplikasi Streamlit.


### 5. **Melakukan pengaturan scheduling (Deepnote Scheduler) untuk mengolah datanya realtime**

#### Deepnote Running ⏰ 
![daily_running](https://github.com/user-attachments/assets/49e29ebf-4b88-41d3-8726-e84b89c2d948)

#### pengaturan_daily_running
![pengaturan_daily_running](https://github.com/user-attachments/assets/0c95fba6-162f-4a91-89fd-48dee9a28d00)


### 6. **Jalankan kode python menggunakan streamlit untuk mengarahkan ke UI untuk operasi EDA, Clustering dan Classification.** 

```
python3 streamlit Brazilian_Ecommerce_Project.py
```
Notes : pada folder yang sama juga harus terdapat file Brazilian_Ecommerce_Clustering dan Brazilian_Ecommerce_Classification

#### start streamlit
![start streamlit](https://github.com/user-attachments/assets/716a4abd-0f88-4597-b629-849355454eca)




## 🌟 Output (Streamlit UI)

## 🛠️ **Page EDA** 
### 📊 Grafik Analisis

#### 1
![ui eda-1](https://github.com/user-attachments/assets/d1406872-c33a-42a4-a556-a26cbff88c97)

#### 2
![ui eda-2](https://github.com/user-attachments/assets/47aea65e-4978-4331-beb3-146b447cd3df)

#### 3
![ui eda-3](https://github.com/user-attachments/assets/ca7bd877-a9f2-41d8-8bc1-4083fd347b4f)

#### 4
![ui eda-4](https://github.com/user-attachments/assets/ce4db1e3-5814-41de-a017-207777bba48f)

#### 5
![ui eda-5](https://github.com/user-attachments/assets/a60fb18a-cdfe-4d33-b367-4d4001e204fd)

#### 6
![ui eda-6](https://github.com/user-attachments/assets/e84e9675-3cbe-4d32-93d1-01d96c58451c)

#### 7
![ui eda-7](https://github.com/user-attachments/assets/8d9ec190-0fe6-4da7-8951-f6b3b54b5e2f)

#### 8
![ui eda-8](https://github.com/user-attachments/assets/ab526ddd-2046-4700-842e-c212c1ba3a29)

#### 9
![ui eda-9](https://github.com/user-attachments/assets/d2808f38-9f7f-4970-8645-592967797412)



## 📚 **Page Classification**
### 🚦 Klasifikasi Pelanggan

#### 1
![UI classification-1](https://github.com/user-attachments/assets/d07470b2-70dc-4b3c-ab88-b6e7bd4d4e7b)
#### 2
![UI classification-2](https://github.com/user-attachments/assets/60f4f103-979b-458c-8ece-1182c429096c)


## 🌀 Page Clustering
### 🔍 Input Data untuk Klasterisasi

#### 1
![UI Clustering-input data-1](https://github.com/user-attachments/assets/b118972b-9492-4d18-9eca-f3987170e000)

#### 2
![UI Clustering-input data-2](https://github.com/user-attachments/assets/399589cf-7ac7-46a8-91ac-193694897979)

#### 3
![UI Clustering-input file-1](https://github.com/user-attachments/assets/f3910fc5-ac07-40b8-bdb4-d4960029450b)

#### 4
![UI Clustering-input file-2](https://github.com/user-attachments/assets/a0dee858-40b8-42e6-b70d-5a0a0ff284e2)


## 📌 **Catatan Tambahan**
Pastikan file Brazilian_Ecommerce_Clustering.bkl dan Brazilian_Ecommerce_Classification.bkl tersedia dalam folder yang sama saat menjalankan Streamlit.


