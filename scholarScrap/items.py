# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# class ScholarscrapItem(scrapy.Item):

class PaperItem(scrapy.Item):
    # full_name = scrapy.Field()
    # id = scrapy.Field()
    # papers = {
    # "title": scrapy.Field(),
    # "citations": scrapy.Field(),
    # "year": scrapy.Field()
    # }
    title = scrapy.Field()
    citations = scrapy.Field()
    year = scrapy.Field()

class ScholarItem(scrapy.Item):
    full_name = scrapy.Field()
    auth = scrapy.Field()
    url = scrapy.Field()
