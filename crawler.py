from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
# from pandas_datareader import data  
from datetime import datetime
from IPython.display import display
import warnings

class Crawling():
    def crawl_stock_all():

        warnings.filterwarnings('ignore')

        driver = webdriver.Chrome("C:/driver/chromedriver")
        driver.get('https://m.stock.naver.com/index.html#/domestic/capitalization/KOSPI')
        stock=[]
        for i in range(1,11):

            driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[2]/div[2]/div[1]/table/tbody/tr[{}]/td[1]/span[1]'.format(i)).click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="common_component_tab"]/div/ul/li[4]/a').click()
            for i in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            time.sleep(1)
            html = driver.page_source
            soup=BeautifulSoup(html, 'html.parser')

            for i in soup.select_one('tbody'):
                company=[]
                company.append(driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[1]/span[1]').text[:6])
                company.append(driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[1]/span[2]').text)
                company.append(i.select('.VTablePrice_td__PZi0o')[0].text)
                company.append(int(i.select('.VTablePrice_td__PZi0o')[1].text.replace(',','')))
                company.append(int(i.select('.VTablePrice_td__PZi0o')[4].text.replace(',','')))
                company.append(int(i.select('.VTablePrice_td__PZi0o')[5].text.replace(',','')))
                company.append(int(i.select('.VTablePrice_td__PZi0o')[6].text.replace(',','')))
                company.append(int(i.select('.VTablePrice_td__PZi0o')[7].text.replace(',','')))
                
                stock.append(company)
            driver.back()

            driver.back()
            time.sleep(1)

        col=['code','name','date','close','open','high','low','volume']
        df = pd.DataFrame(stock,columns=col)
        df
        df.to_csv("C:/ELKStack/0.dataset/stock.csv", mode='a',header=False,index=False)
  
if __name__ == '__main__':
    Crawling.crawl_stock_all()