from kafka import KafkaProducer
import pandas as pd
import json
import time

# Setup Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Baca semua file dataset

customers_df = pd.read_csv('olist_customers_dataset.csv')
orders_df = pd.read_csv('olist_orders_dataset.csv')
reviews_df = pd.read_csv('olist_order_reviews_dataset.csv')
items_df = pd.read_csv('olist_order_items_dataset.csv')
products_df = pd.read_csv('olist_products_dataset.csv')
payments_df = pd.read_csv('olist_order_payments_dataset.csv')
sellers_df = pd.read_csv('olist_sellers_dataset.csv')
geolocation = pd.read_csv('olist_geolocation_dataset.csv')
category_translation_df = pd.read_csv('product_category_name_translation.csv')

# Gabungkan semua dataset
merged_df = pd.merge(customers_df, orders_df, on="customer_id", how='left')
merged_df = pd.merge(merged_df, reviews_df, on="order_id", how='left')
merged_df = pd.merge(merged_df, items_df, on="order_id", how='left')
merged_df = pd.merge(merged_df, products_df, on="product_id", how='left')
merged_df = pd.merge(merged_df, payments_df, on="order_id", how='left')
merged_df = pd.merge(merged_df, sellers_df, on='seller_id', how='left')
merged_df = pd.merge(merged_df, category_translation_df, on='product_category_name', how='left')

# Streaming seluruh data ke Kafka
for _, row in merged_df.iterrows():
    json_data = row.to_dict()  # Konversi seluruh baris DataFrame ke dictionary
    producer.send('ecommerce', json_data)  # Kirim data ke topik Kafka
    print(f"Data sent: {json_data}")  # Debug output
    time.sleep(0.0001)  # Simulasi streaming dengan jeda 2 detik per data

# Flush dan tutup producer
producer.flush()
producer.close()
