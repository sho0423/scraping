# -*- coding: utf-8 -*-
import scrapy
import json
from kab.items import KabItem

class ScrapyEdinetSpiderSpider(scrapy.Spider):
  name = 'scrapy_edinet_spider'
  allowed_domains = ['disclosure.edinet-fsa.go.jp']
  start_urls = ['https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date=2020-02-12&type=2']

  def parse(self, response):
    """
    レスポンスに対するパース処理
    """
    res_json = json.loads(response.body_as_unicode())['results']
    print('ぼえええええええ')
    print(res_json)

    # for doc in response.css()

