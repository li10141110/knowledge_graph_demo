# -*- coding: utf-8 -*- 
# @Author: Shuang0420 
# @Date: 2016-07-20 18:59:50 
# @Last Modified by:   Shuang0420 
# @Last Modified time: 2016-07-20 18:59:50 

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class SearchItem(Item):
    '''
    name = Field()
    description = Field()
    link = Field()
    crawled = Field()
    spider = Field()
    url = Field()
    '''
    basic_info = Field()
    more_info = Field()

class GeneralItem(Item):
    basic_info = Field() 


class ExampleLoader(ItemLoader):
    default_item_class = SearchItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()
