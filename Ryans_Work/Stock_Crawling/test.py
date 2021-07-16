from os import SEEK_CUR
from flask import Flask, render_template, request, jsonify
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import warnings
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from datetime import datetime
from IPython.display import display

warnings.filterwarnings('ignore')

main_url = "https://m.stock.naver.com/index.html#/domestic/stock/035420/price"
driver = webdriver.Chrome("C:/driver/chromedriver")
driver.get(main_url)
time.sleep(2)  
driver.implicitly_wait(1) 
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
driver.implicitly_wait(1) 
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

driver.find_element_by_xpath('/html/body/div/div[1]/div[4]/div[3]/div[2]/div/div[3]/a').click()

data = []
first = ['날짜','종가','전일대비','등락률','시가','고가','저가','거래량']
soup = BeautifulSoup(driver.page_source, "lxml")
items = soup.select('#content > div:nth-child(4) > div:nth-child(3) > div:nth-child(2) > div > div.VTablePrice_article__DfdmT > table > tbody')[0]
driver.close()

can = []
cann = []
for i in items.select('tr>td'):
    can.append(i.text)

for j in range(len(items.select('tr'))):
    cann.append(can[j*8:(j+1)*8])
data = cann[::-1]
data = pd.DataFrame(data)
data = data.reset_index()
del data['index']
data.columns = first
del data['전일대비']

for i in range(len(data.columns.values)):
    if not i in [0,2]:
        data[data.columns.values[i]] = data[data.columns.values[i]].str.replace(',', '')
        data[data.columns.values[i]] = pd.to_numeric(data[data.columns.values[i]], errors='coerce')

kospi_df = data
kospi_df['MA3'] = kospi_df['종가'].rolling(3).mean()
kospi_df['MA5'] = kospi_df['종가'].rolling(5).mean()
kospi_df['MA10'] = kospi_df['종가'].rolling(10).mean()
kospi_df['MA20'] = kospi_df['종가'].rolling(20).mean()

fig, ax = plt.subplots(figsize=(10,5))
ax.set_title('KOSPI INDEX', fontsize=15)
ax.set_ylabel("KOSPI")
ax.set_xlabel("Date Time")
ax.plot(kospi_df.index, kospi_df[['종가','MA5','MA10']])
ax.legend(['종가','MA5','MA10'])
plt.show()
