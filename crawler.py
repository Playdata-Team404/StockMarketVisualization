from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from elasticsearch import Elasticsearch
import warnings

class Crawling():
    def crawl_stock_one():
        # 여기다가 es에서 받은 code 냅두기
        stock=[]
        for stock_num in ['005930']:
            driver = webdriver.Chrome('C:/driver/chromedriver')
            main_url = "https://m.stock.naver.com/index.html#/domestic/stock/"+ stock_num +"/price"
            driver.get(main_url)

            html = driver.page_source
            soup=BeautifulSoup(html, 'html.parser')
            
            for i in soup.select_one('tbody'):
                company=[]
                company.append(driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[1]/span[1]').text[:6])
                company.append(driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[1]/span[2]').text)

            for i in soup.select('#content > div:nth-child(4) > div:nth-child(3) > div:nth-child(2) > div > div.VTablePrice_article__DfdmT > table > tbody > tr:nth-child(1)'):
                company.append(i.select('.VTablePrice_td__PZi0o')[0].text)
                company.append(int(i.select('.VTablePrice_td__PZi0o')[1].text.replace(',','')))
                company.append(int(i.select('.VTablePrice_td__PZi0o')[4].text.replace(',','')))
                company.append(int(i.select('.VTablePrice_td__PZi0o')[5].text.replace(',','')))
                company.append(int(i.select('.VTablePrice_td__PZi0o')[6].text.replace(',','')))
                company.append(int(i.select('.VTablePrice_td__PZi0o')[7].text.replace(',','')))

            stock.append(company)

            time.sleep(1)


        col=['code','name','date','close','open','high','low','volume']
        df = pd.DataFrame(stock,columns=col)
        df.to_csv("C:/ELKStack/0.dataset/stock.csv", mode='a',header=False,index=False)  

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
        df.to_csv("C:/ELKStack/0.dataset/stock.csv",header=False,index=False)
  
    def crawl_news_all():
        driver = webdriver.Chrome("C:/driver/chromedriver")
        stock=[]
        driver.get('https://m.stock.naver.com/index.html#/domestic/capitalization/KOSPI')
        for i in range(1,11):

            #각 회사 들어가기
            driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[2]/div[2]/div[1]/table/tbody/tr[{}]'.format(i)).click()
            time.sleep(1)

            #뉴스항목 들어가기
            driver.find_element_by_xpath('//*[@id="common_component_tab"]/div/ul/li[3]/a/span').click()
            time.sleep(1)
            
            # 뉴스 클릭
            for i in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            for i in range(1,61):

                time.sleep(3)
                news=[]
                
                try:
                    driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[3]/div[2]/div/div[4]/ul/li[{}]/a'.format(i)).click()
                except:
                    print("Pass")
                    continue

                time.sleep(2)

                news.append(driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[1]/span[1]').text[:6])
                news.append(driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[1]/span[2]').text)
                news.append(driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[3]/div[2]/div/div[1]/div[1]/div[1]/time').text[:10])
                news.append(driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[3]/div[2]/div/div[1]/div[1]/strong').text)
                news.append(driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[3]/div[2]/div/div[1]/div[2]/div[1]').text)

                time.sleep(2)
                driver.back()
                time.sleep(2)
                stock.append(news)
                
            driver.back()
            time.sleep(2)
            driver.back()
            time.sleep(2)

        col=['code','name','date','subject','content']
        df = pd.DataFrame(stock,columns=col)
        df.to_csv("news.csv", mode='a',header=False,index=False)

if __name__ == '__main__':
    # Crawling.crawl_stock_all()
    # Crawling.crawl_stock_one()
    Crawling.crawl_news_all()
