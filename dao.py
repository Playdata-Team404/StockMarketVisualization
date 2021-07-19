from datetime import datetime
from elasticsearch import Elasticsearch


class es_dao():
    def save_news(news_data):
        es = Elasticsearch()
        if not es.indices.exists(index="stock_news"):
            body = {"settings":{"number_of_shards":2,"number_of_replicas":1,"index":{"analysis":{"analyzer":{"nori_analyzer":{"type":"custom","tokenizer":"nori_user_dict","filter":["my_posfilter"]}},"tokenizer":{"nori_user_dict":{"type":"nori_tokenizer","decompound_mode":"discard"}},"filter":{"my_posfilter":{"type":"nori_part_of_speech","stoptags":["E","IC","J","MAG","MAJ","MM","SP","SSC","SSO","SC","SE","XPN","XSA","XSN","XSV","UNA","NA","VSV"]}}}}},"mappings":{"properties":{"author":{"type":"text"},"post_create_datetime":{"type":"date"},"title":{"type":"text","fielddata":1},"content":{"type":"text","fielddata":1},"url":{"type":"text"},"publisher":{"type":"keyword"},"tag":{"type":"keyword"}}}}
            res = es.indices.create(index="stock_news", body=body, include_type_name=True, ignore=[400, 404])

        docs = news_data
        for doc in docs:
            res = es.index(index="stock_news",  body=doc)
            
