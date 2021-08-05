import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
resp_jateng = requests.get('https://data.covid19.go.id/public/api/prov_detail_JAWA_TENGAH.json')
cov_jateng_raw = resp_jateng.json()
cov_jateng = pd.DataFrame(cov_jateng_raw['list_perkembangan'])
print('Info cov_jateng:\n', cov_jateng.info())
print('\nLima data teratas cov_jateng:\n', cov_jateng.head())
print('\nLima data terakhir cov_jateng:\n', cov_jateng.tail())

cov_jateng_tidy = (cov_jateng.drop(columns=[item for item in cov_jateng.columns 
                                               if item.startswith('AKUMULASI') 
                                                  or item.startswith('DIRAWAT')])
                           .rename(columns=str.lower)
                           .rename(columns={'kasus': 'kasus_baru'})
                  )
cov_jateng_tidy['tanggal'] = pd.to_datetime(cov_jateng_tidy['tanggal']*1e6, unit='ns')
print('Lima data teratas:\n', cov_jateng_tidy.head())

plt.clf()
fig, ax = plt.subplots(figsize=(10,10))
ax.bar(data=cov_jateng_tidy, x='tanggal', height='kasus_baru', color='salmon')
ax.set_title('Kasus Harian Positif COVID-19 di Jawa Tengah',
             fontsize=30, pad=40)
ax.set_xlabel('')
ax.set_ylabel('Jumlah kasus', fontsize=15)
ax.text(1, -0.3, 'Sumber data: covid.19.go.id', color='blue',
ha='right', transform=ax.transAxes, fontsize=15)
ax.set_xticklabels(ax.get_xticks(), rotation=90)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.grid(axis='y')
plt.tight_layout()
plt.show()

plt.clf()
fig, ax = plt.subplots(figsize=(10,10))
ax.bar(data=cov_jateng_tidy, x='tanggal', height='sembuh', color='olivedrab')
ax.set_title('Kasus Harian Sembuh Dari COVID-19 di Jawa Tengah',
             fontsize=30, pad=40)
ax.set_xlabel('')
ax.set_ylabel('Jumlah kasus', fontsize=15)
ax.text(1, -0.3, 'Sumber data: covid.19.go.id', color='blue',
        ha='right', transform=ax.transAxes, fontsize=15)
ax.set_xticklabels(ax.get_xticks(), rotation=90)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.grid(axis='y')
plt.tight_layout()
plt.show()

plt.clf()
fig, ax = plt.subplots(figsize=(10, 10))
ax.bar(data=cov_jateng_tidy, x='tanggal', height='meninggal', color='slategrey')
ax.set_title('Kasus Harian Meninggal Dari Covid-19 di Jawa Jateng',
             fontsize=30, pad=40)
ax.set_xlabel('')
ax.set_ylabel('Jumlah kasus', fontsize=15)
ax.text(1, -0.3, 'Sumber data: covid.19.go.id', color='blue',
        ha='right', transform=ax.transAxes, fontsize=15)
ax.set_xticklabels(ax.get_xticks(), rotation=90)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.grid(axis='y')
plt.tight_layout()
plt.show()

cov_jateng_akumulasi = cov_jateng_tidy[['tanggal']].copy()
cov_jateng_akumulasi['akumulasi_aktif'] = (cov_jateng_tidy['kasus_baru'] - cov_jateng_tidy['sembuh'] - cov_jateng_tidy['meninggal']).cumsum()
cov_jateng_akumulasi['akumulasi_sembuh'] = cov_jateng_tidy['sembuh'].cumsum()
cov_jateng_akumulasi['akumulasi_meninggal'] = cov_jateng_tidy['meninggal'].cumsum()
print(cov_jateng_akumulasi.tail())

plt.clf()
fig, ax = plt.subplots(figsize=(15,10))
ax.plot('tanggal','akumulasi_aktif', data=cov_jateng_akumulasi, lw=2)

ax.set_title('Akumulasi aktif COVID-19 di Jawa Tengah',
             fontsize=30, pad=40)
ax.set_xlabel('')
ax.set_ylabel('Akumulasi aktif')
ax.text(1, -0.3, 'Sumber data: covid.19.go.id', color='blue',
        ha='right', transform=ax.transAxes)
ax.set_xticklabels(ax.get_xticks(), rotation=90)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.grid()
plt.tight_layout()
plt.show()

plt.clf()
fig, ax = plt.subplots(figsize=(10, 10))
cov_jateng_akumulasi_ts = cov_jateng_akumulasi.set_index('tanggal')
cov_jateng_akumulasi_ts.plot(kind='line', ax=ax, lw=3, color=['salmon', 'slategrey', 'olivedrab'])

ax.set_title('Dinamika Kasus COVID-19 di Jawa Tengah', fontsize=30, pad=40)
ax.set_xlabel('')
ax.set_ylabel('Akumulasi aktif', fontsize=15)
ax.text(1, -0.3, 'Sumber data: covid.19.go.id', color='blue', ha='right', transform=ax.transAxes, fontsize=15)


plt.grid()
plt.tight_layout()
plt.show()
