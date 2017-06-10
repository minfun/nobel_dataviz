# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline


class NobelWinnersPipeline(object):

    def process_item(self, item, spider):
        return item


class DropNonPersons(object):

    def process_item(self, item, spider):
        if not item['gender']:
            raise DropItem("No gender for %s" % item['name'])
        return item


class NobelImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if image_paths:
            item['bio_image'] = image_paths[0]
        return item
