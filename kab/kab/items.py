# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KabItem(scrapy.Item):
  name = scrapy.Field()
  ticker = scrapy.Field()
  periodStart = scrapy.Field()
  periodEnd = scrapy.Field()
  year = scrapy.Field()
  quarter = scrapy.Field()
  accouting_standard = scrapy.Field()

  sale = scrapy.Field()
  profit = scrapy.Field()
