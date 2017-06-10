# Copyright @2016 created by wangleifan 
# Github @minfun
# !/usr/bin/env python
# !-*-encoding:utf-8-*-
import scrapy
import re
import logging


logger = logging.getLogger(__name__)
BASE_URL = 'http://en.wikipedia.org'


class NWinnerItem(scrapy.Item):

    link = scrapy.Field()
    name = scrapy.Field()
    mini_bio = scrapy.Field()
    image_urls = scrapy.Field()
    bio_image = scrapy.Field()
    images = scrapy.Field()


class NWinnerSpider(scrapy.Spider):

    name = 'nwinners_minibio'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ["https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country"]

    def parse(self, response):

        filename = response.url.split('/')[-1]
        h2s = response.xpath('//h2')
        items = []

        for h2 in h2s:
            country = h2.xpath('span[@class="mw-headline"]/text()').extract()
            if country:
                winners = h2.xpath('following-sibling::ol[1]')
                for w in winners.xpath('li'):
                    wdata = {}
                    wdata['link'] = BASE_URL + w.xpath('a/@href').extract()[0]
                    request = scrapy.Request(wdata['link'], callback=self.get_mini_bio)
                    request.meta['item'] = NWinnerItem(**wdata)
                    yield request

    def get_mini_bio(self, response):

        BASE_URL_ESCAPED = 'http:\/\/en.wikipedia.org'
        item = response.meta['item']
        item['image_urls'] = []
        img_src = response.xpath('//table[contains(@class,"infobox")]//img/@src')
        if img_src:
            item['image_urls'] = ['http:' + img_src[0].extract()]
        # paras = response.xpath('//*[@id="mw-content-text"]/p[text() or normalize-space(.)=""]').extract()
        mini_bio = response.css('.mw-parser-output > p')[0].extract()
        # logger.info('paras')
        logger.info(mini_bio)
        mini_bio = mini_bio.replace('href="/wiki', 'href="' + BASE_URL + '/wiki')
        mini_bio = mini_bio.replace('href="#"', item['link'] + '#')
        item['mini_bio'] = mini_bio
        yield item
