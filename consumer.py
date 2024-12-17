from kafka import KafkaConsumer
import json
import pandas as pd
from minio import Minio

# Konfigurasi Kafka Consumer
consumer = KafkaConsumer(
    'ecommerce',  # Nama topik Kafka
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # Deserialize JSON
    auto_offset_reset='earliest',  # Mulai membaca dari awal
    enable_auto_commit=True,  # Auto-commit
    group_id='ecomm-consumer-group'  # ID grup konsumen
)

# Konfigurasi MinIO
minio_client = Minio(
    "localhost:9000",  # Endpoint MinIO
    access_key="minioadmin",  # Ganti dengan akses kunci MinIO Anda
    secret_key="minioadmin",  # Ganti dengan kunci rahasia MinIO Anda
    secure=False  # Jika tidak menggunakan HTTPS
)

# Nama bucket dan folder di MinIO
bucket_name = "ecomm-bucket"
folder_name = "batches/"  # Folder untuk menyimpan file

# Pastikan bucket MinIO ada, buat jika belum ada
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)

print("Consumer started. Listening for messages...")

# Variabel untuk menyimpan batch data
batch_data = []
batch_size = 5000  # Ukuran batch
file_counter = 1  # Untuk penamaan file batch

# Loop membaca data dari Kafka
for message in consumer:
    # Ambil data dari Kafka
    data = message.value
    batch_data.append(data)  # Tambahkan data ke batch

    # Jika batch mencapai ukuran yang ditentukan, simpan ke MinIO
    if len(batch_data) >= batch_size:
        # Konversi batch ke DataFrame
        df = pd.DataFrame(batch_data)

        # Simpan ke CSV sementara
        file_name = f"batch_{file_counter}.csv"
        local_file_path = file_name
        df.to_csv(local_file_path, index=False)

        # Nama object di MinIO (folder_name + file_name)
        minio_object_name = f"{folder_name}{file_name}"

        # Unggah ke MinIO
        minio_client.fput_object(
            bucket_name=bucket_name,
            object_name=minio_object_name,
            file_path=local_file_path,
        )

        print(f"Uploaded batch {file_counter} to MinIO in folder '{folder_name}' as {file_name}")

        # Reset batch
        batch_data = []
        file_counter += 1

# Jika ada sisa data setelah loop selesai, simpan ke MinIO
if batch_data:
    df = pd.DataFrame(batch_data)
    file_name = f"batch_{file_counter}.csv"
    local_file_path = file_name
    df.to_csv(local_file_path, index=False)

    # Nama object di MinIO (folder_name + file_name)
    minio_object_name = f"{folder_name}{file_name}"

    # Unggah ke MinIO
    minio_client.fput_object(
        bucket_name=bucket_name,
        object_name=minio_object_name,
        file_path=local_file_path,
    )
    print(f"Uploaded final batch {file_counter} to MinIO in folder '{folder_name}' as {file_name}")
