# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Compose, Join
from w3lib.html import remove_tags

def clean_text(value):
    return int(value.replace("\r\n","").strip())

def add_head(value):
    return "https://stackoverflow.com" + value

class Practice2Item(scrapy.Item):
    # define the fields for your item here like:
    ques = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    answer_by = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    vote = scrapy.Field(input_processor=MapCompose(remove_tags, clean_text), output_processor=TakeFirst())
    views = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    weblink = scrapy.Field(input_processor=MapCompose(remove_tags, add_head), output_processor=TakeFirst())