import pandas as pd

# URL raw yang benar (pakai %20 untuk spasi di "sample data")
transactions = pd.read_csv('https://raw.githubusercontent.com/hackathonBI/CCS/master/sample%20data/transaction_1k.csv')
customers = pd.read_csv('https://raw.githubusercontent.com/hackathonBI/CCS/master/sample%20data/customers.csv')
gas_stations = pd.read_csv('https://raw.githubusercontent.com/hackathonBI/CCS/master/sample%20data/gasstations.csv')
products = pd.read_csv('https://raw.githubusercontent.com/hackathonBI/CCS/master/sample%20data/products.csv')

# Konversi Date dan Hour
transactions['Date'] = pd.to_datetime(transactions['Date'], format='%d.%m.%Y')
transactions['Hour'] = pd.to_datetime(transactions['Time'], format='%H:%M:%S').dt.hour

# 1. Top 5 Customers
top_customers = transactions.groupby('CustomerID')['Price'].sum().nlargest(5).reset_index(name='Total_Price')
top_customers = top_customers.merge(customers, on='CustomerID', how='left')
print("1. Top 5 Customers berdasarkan nilai transaksi paling banyak:")
print(top_customers[['CustomerID', 'Total_Price', 'Segment', 'Country']])

# 2. Top 5 Gas Stations
top_stations = transactions.groupby('GasStationID')['Price'].sum().nlargest(5).reset_index(name='Total_Price')
top_stations = top_stations.merge(gas_stations, on='GasStationID', how='left')
print("\n2. Top 5 Gas Stations berdasarkan nilai transaksi paling banyak:")
print(top_stations[['GasStationID', 'Total_Price', 'Segment', 'Country']])

# 3. Top 5 Produk
top_products = transactions.groupby('ProductID')['Price'].sum().nlargest(5).reset_index(name='Total_Price')
top_products = top_products.merge(products, on='ProductID', how='left')
print("\n3. Top 5 Jenis Produk berdasarkan nilai transaksi paling banyak:")
print(top_products[['ProductID', 'Description', 'Total_Price']])

# 4. Deskripsi statistik per hari (23,24,25,26) untuk Price
print("\n4. Deskripsi statistik nilai transaksi (Price) untuk masing-masing hari:")
for day in [23, 24, 25, 26]:
    daily_data = transactions[transactions['Date'].dt.day == day]['Price']
    print(f"\nHari {day}:")
    print(daily_data.describe())

# 5. Waktu terbaik (hari + jam) dengan transaksi terbanyak
best_count = transactions.groupby([transactions['Date'].dt.day, 'Hour']).size().nlargest(10).reset_index(name='Jumlah_Transaksi')
best_count.columns = ['Hari', 'Jam', 'Jumlah_Transaksi']
print("\n5. Waktu terbaik berdasarkan jumlah transaksi terbanyak:")
print(best_count)

best_value = transactions.groupby([transactions['Date'].dt.day, 'Hour'])['Price'].sum().nlargest(10).reset_index(name='Total_Price')
best_value.columns = ['Hari', 'Jam', 'Total_Price']
print("\nWaktu terbaik berdasarkan total nilai transaksi tertinggi:")
print(best_value)

# 6. Business Understanding
print("\n6. Tujuan utama dari analisis data customer ini dari segi bisnis:")
print("Tujuan utama adalah memahami perilaku dan nilai ekonomi customer di jaringan SPBU (gas station) ")
print("untuk mendukung keputusan bisnis, seperti:")
print("- Identifikasi customer high-value untuk program loyalitas atau promo targeted")
print("- Optimasi stok produk dan staffing di stasiun atau jam ramai")
print("- Strategi pricing dan cross-selling produk non-bahan bakar yang menguntungkan")
print("- Peningkatan revenue dan retensi customer secara keseluruhan")