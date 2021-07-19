from flask import Flask, render_template, request, jsonify
from pandas.core.accessor import register_index_accessor
from crawler import Crawling
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ohlc
import matplotlib.ticker as ticker
from matplotlib import font_manager, rc
import warnings
import platform

app = Flask(import_name=__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/', methods=['get'])
def index():
    return render_template('index.html')


@app.route('/getstock', methods=['get'])
def stock_crawling():
    Crawling.crawl_stock_all()

@app.route('/getnews', methods=['get'])
def news_crawling():
    Crawling.crawl_news_all()

@app.route('/stockchart', methods=['get', 'post'])
def stock_candle():
    if platform.system() == 'Windows':
        path = 'c:/Windows/Fonts/malgun.ttf'
        font_name = font_manager.FontProperties(fname = path).get_name()
        rc('font', family = font_name)
    elif platform.system() == 'Darwin':
        rc('font', family = 'AppleGothic')
    else:
        print('Check your OS system')

    stock_name = request.form.get("stock_name")

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
    index = df_.index.astype('str')

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
    plt.savefig("static/img/candlestick{}.png".format(stock_name))
    return "static/img/candlestick{}.png".format(stock_name)

@app.route('/wordcloud', methods=['get', 'post'])
def wordcloud():
    stock_name = request.form.get("stock_name")

    data = pd.read_csv('news.csv',encoding='utf-8')
    noun_extractor = LRNounExtractor_v2(verbose=True)
    nouns = noun_extractor.train_extract(data[data['name']==stock_name]['content'])
    
    count=[]
    for word, score in sorted(nouns.items()):
        info=[]
        word=word.replace('"','').replace('“','').replace('‘','').replace("'",'')
        if len(word)>1:
            info.append(word)
            info.append(score[0])

            count.append(info)
    
    icon = Image.open('dollar.png')
    mask = Image.new("RGB", icon.size, (255,255,255))
    mask.paste(icon,icon)
    mask = np.array(mask)

    wordcloud = WordCloud(font_path='NanumGothic.ttf',width=1500,height=1000,background_color='black',mask=mask,max_font_size=300)
    wordcloud.generate_from_frequencies(dict(count))
    plt.imshow(wordcloud)
    wordcloud.to_file('static/img/word{}.png'.format(stock_name))
    return 'static/img/word{}.png'.format(stock_name)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)
