# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MycartoonItem(scrapy.Item):
    # define the fields for your item here like:
    dirName = scrapy.Field()
    linkUrl = scrapy.Field()
    imgUrl = scrapy.Field()
    fileName = scrapy.Field()
    pass
