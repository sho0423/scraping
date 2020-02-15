# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KabItem(scrapy.Item):
  secCode = scrapy.Field()
  filerName = scrapy.Field()
  docDescription = scrapy.Field()
  periodStart = scrapy.Field()
  periodEnd = scrapy.Field()


  accouting_standard = scrapy.Field()
  sale = scrapy.Field()
  profit = scrapy.Field()
