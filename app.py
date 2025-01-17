# To run this file:
# python -m streamlit run .\app.py

from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import streamlit as st

# Code for Table 1
website_URL = 'https://www.salahtimes.com/india/new-delhi'
html_content = requests.get(website_URL).text
soup = BeautifulSoup(html_content, 'lxml')
table = soup.find('table', class_ = 'table-prayertimes')
t_body = table.find('tbody')
rows = t_body.find_all('tr')
data = rows[1].find_all('td')

timings = []
for datum in data:
    timings.append(datum.text)
timings.pop(0)

data = {'Event Name': ['Fajr', 'Sunrise','Zuhr', 'Asr', 'Maghrib', 'Isha'], 'Start Time': timings}
df = pd.DataFrame(data)

st.write("Today's namaz timings:")
st.table(df)

# Code for Table 2
csv_url = "https://docs.google.com/spreadsheets/d/" + "1V3c2-kDkehR_ViJdsJsgWkpK9vAn233j6Gm7lPOVueM" + "/gviz/tq?sheet=" + "mosque_table" + "/export?format=csv"
response = requests.get(csv_url)
response.raise_for_status()

data = list(csv.reader(response.text.splitlines()))
data = data[1]
data = data[52:]
table = []
colNames = ['index', 'index_f', 'Masjid', 'area', 'latitude', 'latitude_f', 'longitude', 'longitude_f', 'Jumuah', 'Fajr', 'Zuhr', 'Asr', 'Maghrib', 'Isha']
for row in range(6):
    table_row = {}
    for col in range(len(colNames)):
        table_row[colNames[col]] = data[row*len(colNames) + col]
    table_row.pop('index')
    table_row.pop('index_f')
    table_row['Masjid'] = table_row['Masjid'][6:-2]
    table_row.pop('area')
    table_row.pop('latitude')
    table_row.pop('latitude_f')
    table_row.pop('longitude')
    table_row.pop('longitude_f')
    table_row['Jumuah'] = table_row['Jumuah'][6:-2]
    table_row['Fajr'] = table_row['Fajr'][6:-2]
    table_row['Zuhr'] = table_row['Zuhr'][6:-2]
    table_row['Asr'] = table_row['Asr'][6:-2]
    table_row['Maghrib'] = table_row['Maghrib'][6:-2]
    table_row['Isha'] = table_row['Isha'][6:-4]
    table.append(table_row)
table[-1]['Isha'] = table[-1]['Isha'][:-1]
df = pd.DataFrame(table)

st.write("Jamaat timings in nearby masajid:")
st.dataframe(df, use_container_width=True)