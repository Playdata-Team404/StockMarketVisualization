from flask import Flask, render_template, request, jsonify
import time
from crawler import Crawling
from elasticsearch import Elasticsearch
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ohlc
import matplotlib.ticker as ticker
import warnings

app = Flask(import_name=__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/', methods=['get'])
def index():
    return render_template('00.index.html')


@app.route('/fullcrawling', methods=['get'])
def full_crawling():
    Crawling.crawl_stock_all()


@app.route('/stockchart', methods=['get'])
def stock_candle(stock_name):

    warnings.filterwarnings('ignore')
    col = ['code', 'name', 'date', 'close', 'open', 'high', 'low', 'volume']
    df = pd.read_csv("C:/ELKStack/0.dataset/stock.csv",
                     names=col, header=None, index_col='date')

    df_ = df[df['name'] == stock_name]
    df_['MA3'] = df_['close'].rolling(3).mean()
    df_['MA5'] = df_['close'].rolling(5).mean()
    df_['MA10'] = df_['close'].rolling(10).mean()
    df_ = df_.sort_index(ascending=True)

    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.set_title('INDEX', fontsize=15)
    ax.set_ylabel("Inter")
    ax.set_xlabel("Date Time")
    ax.plot(df_.index, df_[['close', 'MA5', 'MA10']])
    ax.legend(['close', 'MA5', 'MA10'])

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111)
    index = df_.index.astype('str')  # 캔들스틱 x축이 str로 들어감

    # 이동평균선 그리기
    ax.plot(index, df_['MA3'], label='MA3', linewidth=0.7)
    ax.plot(index, df_['MA5'], label='MA5', linewidth=0.7)
    ax.plot(index, df_['MA10'], label='MA10', linewidth=0.7)

    # X축 티커 숫자 20개로 제한
    ax.xaxis.set_major_locator(ticker.MaxNLocator(20))

    # 그래프 title과 축 이름 지정
    ax.set_title('INDEX', fontsize=22)
    ax.set_xlabel('Date')

    # 캔들차트 그리기
    candlestick2_ohlc(ax, df_['open'], df_['high'],
                      df_['low'], df_['close'],
                      width=0.5, colorup='r', colordown='b')
    ax.legend()
    plt.grid()
    plt.savefig("static\img\candlestick.png")


if __name__ == '__main__':
    stock_candle('삼성전자')