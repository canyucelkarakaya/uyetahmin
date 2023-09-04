import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


# Excel dosyasını okuma
file_path = 'All_Users.xlsx'
df = pd.read_excel(file_path)

# Tarih sütunlarını datetime nesnelerine dönüştürme
df['Register Date'] = pd.to_datetime(df['Register Date'])
df['Suspended Date'] = pd.to_datetime(df['Suspended Date'])

# Yıl ve ay sütunlarını oluşturma
df['Year'] = df['Register Date'].dt.year
df['Month'] = df['Register Date'].dt.month

# Yıl ve ay bazında kayıt sayılarını hesaplama
year_month_counts = df.groupby(['Year', 'Month']).size().reset_index(name='Count')

# Streamlit uygulamasını oluşturma
st.title("Üye Değişim Grafiği")

# Üye değişim grafiğini görmek için yıl seçimi
selected_year = st.selectbox("Üye değişim grafiğini görmek için yıl seçin:", [2019, 2020, 2021, 2022, "2023"])

# Yıla göre veriyi filtreleme
if selected_year == 2019:
    filtered_data = year_month_counts[(year_month_counts['Year'] == 2019) & (year_month_counts['Month'] >= 7)]
elif selected_year == 2020:
    filtered_data = year_month_counts[(year_month_counts['Year'] == 2020)]
elif selected_year == 2021:
    filtered_data = year_month_counts[(year_month_counts['Year'] == 2021)]
elif selected_year == 2022:
    filtered_data = year_month_counts[(year_month_counts['Year'] == 2022)]
else:  # 2023 seçildiğinde
    filtered_data = year_month_counts[(year_month_counts['Year'] == 2023) & (year_month_counts['Month'] <= 6)]

# Grafik oluşturma
plt.figure(figsize=(12, 8))

# Seçilen yılın değişimini gösteren grafik
plt.plot(filtered_data['Month'], filtered_data['Count'], label=f'Üye Sayısı ({selected_year})', color='blue', marker='o')

plt.xlabel('Ay')
plt.ylabel('Üye Sayısı')
plt.title(f'{selected_year} Yılının Üye Sayısı Zaman Grafiği')
plt.legend()
plt.grid(True)

# Streamlit üzerinde gösterme
st.pyplot(plt)

# Excel dosyasını okuma
file_path = 'All_Users.xlsx'
df = pd.read_excel(file_path)

# Tarih sütunlarını datetime nesnelerine dönüştürme
df['Register Date'] = pd.to_datetime(df['Register Date'])
df['Suspended Date'] = pd.to_datetime(df['Suspended Date'])

# Yıl ve ay sütunlarını oluşturma
df['Year'] = df['Register Date'].dt.year
df['Month'] = df['Register Date'].dt.month

# Yıl ve ay bazında kayıt sayılarını hesaplama
year_month_counts = df.groupby(['Year', 'Month']).size().reset_index(name='Count')

# Tahmin için kullanılacak özellikler ve hedef
X = year_month_counts[['Year', 'Month']]
y = year_month_counts['Count']

# Modeli oluşturma ve eğitme
model = LinearRegression()
model.fit(X, y)

# Streamlit uygulamasını oluşturma
st.title("Üye Tahmin Uygulaması")

# Tahmin yapılacak ayı seçme
selected_month = st.selectbox("Tahmin yapmak istediğiniz ayı seçin:", [7, 8, 9, 10, 11, 12])

# Sadece 2023 yılının ilk 6 ayını filtreleme
year_month_counts_2023 = year_month_counts[(year_month_counts['Year'] == 2023) & (year_month_counts['Month'] <= 6)]

# Grafik oluşturma
plt.figure(figsize=(12, 8))

# 2023 yılının ilk 6 ayının değişimini gösteren grafik
plt.plot(year_month_counts_2023['Month'], year_month_counts_2023['Count'], label='Üye Sayısı (2023)', color='blue', marker='o')

# Seçilen ayın tahminini mavi nokta ile gösterme
predicted_count = model.predict([[2023, selected_month]])
plt.scatter(selected_month, predicted_count, color='red', marker='o', s=100, label=f'{selected_month}. Ay Tahmini: {int(predicted_count[0])}')

# Her noktanın yanına üye sayısını yazdırma
for x, y in zip(year_month_counts_2023['Month'], year_month_counts_2023['Count']):
    plt.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

plt.xlabel('Ay')
plt.ylabel('Üye Sayısı')
plt.title('2023 Yılının İlk 6 Ayının Üye Sayısı Zaman Grafiği ve Tahmin')
plt.legend()
plt.grid(True)

# Tahmini kayıt sayısını metin olarak gösterme
st.text(f"2023 yılının {selected_month}. ayında tahmini kayıt sayısı: {int(predicted_count[0])}")

# Streamlit üzerinde gösterme
st.pyplot(plt)