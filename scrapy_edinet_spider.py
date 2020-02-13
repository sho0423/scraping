# -*- coding: utf-8 -*-
import scrapy


class ScrapyEdinetSpiderSpider(scrapy.Spider):
    name = 'scrapy_edinet_spider'
    allowed_domains = ['disclosure.edinet-fsa.go.jp']
    start_urls = ['http://disclosure.edinet-fsa.go.jp/']

    def parse(self, response):
        pass
