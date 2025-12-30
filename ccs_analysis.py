import pandas as pd

# Load data dari data/ccs
transactions = pd.read_csv('data/ccs/sample.csv')  # Ini transaction_1k, rename jika perlu
customers = pd.read_csv('data/ccs/customers.csv')
gas_stations = pd.read_csv('data/ccs/gasstations.csv')
products = pd.read_csv('data/ccs/products.csv')

# Konversi Date dan Hour
transactions['Date'] = pd.to_datetime(transactions['Date'], format='%Y-%m-%d')
transactions['Hour'] = pd.to_datetime(transactions['Time'], format='%H:%M:%S').dt.hour

# 1. Top 5 Customers
top_customers = transactions.groupby('CustomerID')['Price'].sum().nlargest(5).reset_index(name='Total_Price')
top_customers = top_customers.merge(customers, on='CustomerID', how='left')
print("1. Top 5 Customers berdasarkan nilai transaksi paling banyak:")
print(top_customers.to_string(index=False))

# 2. Top 5 Gas Stations
top_stations = transactions.groupby('GasStationID')['Price'].sum().nlargest(5).reset_index(name='Total_Price')
top_stations = top_stations.merge(gas_stations, left_on='GasStationID', right_on='SiteID', how='left')
print("\n2. Top 5 Gas Stations berdasarkan nilai transaksi paling banyak:")
print(top_stations.to_string(index=False))

# 3. Top 5 Jenis Produk
top_products = transactions.groupby('ProductID')['Price'].sum().nlargest(5).reset_index(name='Total_Price')
top_products = top_products.merge(products, on='ProductID', how='left')
print("\n3. Top 5 Jenis Produk berdasarkan nilai transaksi paling banyak:")
print(top_products.to_string(index=False))

# 4. Deskripsi statistik untuk masing-masing hari (23,24,25,26)
print("\n4. Deskripsi statistik untuk masing-masing hari pada dataset transaction_1k:")
for day in [23, 24, 25, 26]:
    daily = transactions[transactions['Date'].dt.day == day]['Price']
    print(f"\nHari {day}:")
    print(daily.describe())

# 5. Waktu terbaik (hari dan jam) dengan paling banyak transaksi
transactions['Day'] = transactions['Date'].dt.day
best_time = transactions.groupby(['Day', 'Hour']).size().nlargest(10).reset_index(name='Jumlah_Transaksi')
print("\n5. Waktu terbaik dimana paling banyak user melakukan transaksi:")
print(best_time.to_string(index=False))

# 6. Tujuan utama dari analisis data customer (business understanding)
print("\n6. Dari segi bisnis understanding, tujuan utama dari analisis data customer ini adalah:")
print("Tujuan utama adalah memahami perilaku customer di jaringan SPBU untuk mendukung keputusan bisnis, seperti identifikasi customer loyal (top spender), stasiun dan produk paling menguntungkan, pola statistik per hari, dan waktu ramai untuk optimasi stok, staffing, promo targeted, serta peningkatan revenue dan retensi customer.")