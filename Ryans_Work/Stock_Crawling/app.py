from bs4 import BeautifulSoup 
import urllib.request as req
from selenium import webdriver
from flask import Flask, json, request, render_template, jsonify
import time

app = Flask(__name__)


@app.route('/', methods=['get'])
def get():
    return render_template('index.html') 

@app.route('/getdata', methods=['post'])
def getdata():
    driver = webdriver.Chrome("C:/driver/chromedriver")
    driver.get('https://kr.investing.com/equities/south-korea')
    time.sleep(3) 
    # print(driver.page_source)
    # driver.implicitly_wait(10) # seconds
    soup = BeautifulSoup(driver.page_source,'lxml')

    boxitems = soup.select('table#cross_rate_markets_stocks_1>tbody > tr>td')
    print('--'*30)
    print(boxitems[0])

    ss = []
    for i in boxitems:
        ss.append(i.text)
    
    companies = []
    for j in range(50):
        companies.append(ss[10*j:10*(j+1)][1])
    
    result = []
    for j in range(50):
        datas = ss[10*j:10*(j+1)][1:-1]
        company = datas[0]
        current = datas[1]
        high = datas[2]
        low = datas[3]
        move = datas[4]
        move_per = datas[5]
        amount = datas[6]
        date = datas[7]
        result.append({'company':company, 'current':current,'high':high,'low':low,\
        'move':move,'move_per':move_per,'amount':amount,'date':date})
    
    sele = []
    for st in result:
        if request.form.get('stock') == st['comapny']:
            sele.append(st)

    driver.close()
    return jsonify(sele)
            


# @app.route('/stocks', methods=['POST'])
# def stocks():
#     driver = webdriver.Chrome("C:/driver/chromedriver")
#     driver.get('https://kr.investing.com/equities/south-korea')
#     time.sleep(3) 
#     soup = BeautifulSoup(driver.page_source, "lxml" )
#     stocks = soup.select('table#cross_rate_markets_stocks_1>tbody > tr>td')
#     # driver.close()
#     ss = []
#     for i in stocks:
#         ss.append(i.text)
    
#     companies = []
#     for j in range(50):
#         companies.append(ss[10*j:10*(j+1)][1])
    
#     result = []
#     for j in range(50):
#         datas = ss[10*j:10*(j+1)][1:-1]
#         company = datas[0]
#         current = datas[1]
#         high = datas[2]
#         low = datas[3]
#         move = datas[4]
#         move_per = datas[5]
#         amount = datas[6]
#         date = datas[7]
#         result.append({'company':company, 'current':current,'high':high,'low':low,\
#         'move':move,'move_per':move_per,'amount':amount,'date':date})

    # print('*'*100)
    # for st in result:
    #     if request.form.get('stock_name') == st['comapny']:
    #         return jsonify(st)

'''
    

    ['company','current','high','low','move','move_per','amount','date']
    result = []
    for j in range(50):
        datas = ss[10*j:10*(j+1)][1:-1]
        company = datas[0]
        current = datas[1]
        high = datas[2]
        low = datas[3]
        move = datas[4]
        move_per = datas[5]
        amount = datas[6]
        date = datas[7]
        result.append({'company':company, 'current':current,'high':high,'low':low,\
        'move':move,'move_per':move_per,'amount':amount,'date':date})
'''
    
# request.form.get('stock_name')

    # for film in films:
    #     title = film.find('strong').text
    #     price = film.find('span').text
    #     photo = film.find('img')['src']
    #     items.append({'title':title, 'price':price, 'photo':photo})
    # return jsonify(items)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port="5000")
    # stocks()


