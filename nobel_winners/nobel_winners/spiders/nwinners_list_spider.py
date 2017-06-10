# Copyright @2016 created by wangleifan 
# Github @minfun
# !/usr/bin/env python
# !-*-encoding:utf-8-*-
import scrapy
import re


BASE_URL = 'http://en.wikipedia.org'


class NWinnerItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    year = scrapy.Field()
    category = scrapy.Field()
    nationality = scrapy.Field()
    gender = scrapy.Field()
    born_in = scrapy.Field()
    date_of_birth = scrapy.Field()
    date_of_death = scrapy.Field()
    place_of_birth = scrapy.Field()
    place_of_death = scrapy.Field()
    text = scrapy.Field()


class NWinnerSpider(scrapy.Spider):

    name = 'nwinners_full'
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
                    wdata = process_winner_li(w, country[0])
                    print wdata['link']
                    try:
                        request = scrapy.Request(wdata['link'], callback=self.parse_bio, dont_filter=True)
                        request.meta['item'] = NWinnerItem(**wdata)
                        yield request
                    except:
                        print "except"
                        pass
                    #text = w.xpath('descendant-or-self::text()').extract()
                    #items.append(NWinnerItem(country=country[0], name=text[0], link_text=' '.join(text)))

    def parse_bio(self, response):
        item = response.meta['item']
        href = response.xpath("//li[@id='t-wikibase']/a/@href").extract()
        if href:
            request = scrapy.Request(href[0], callback=self.parse_wikidata, dont_filter=True)
            request.meta['item'] = item
            yield request

    def parse_wikidata(self, response):
        item = response.meta['item']

        property_codes = [
            {'name': 'date_of_birth', 'code': 'P569'},
            {'name': 'date_of_death', 'code': 'P570'},
            {'name': 'place_of_birth', 'code': 'P19', 'link': True},
            {'name': 'place_of_death', 'code': 'P20', 'link': True},
            {'name': 'gender', 'code': 'P21', 'link': True}
        ]
        p_template = '//*[@id="%(code)s"]/div[2]/div/div/div[2]/div[1]/div/div[2]/div[2]'
        for prop in property_codes:
            extra_html = ''
            if prop.get('link'):  # property string in <a> tag
                extra_html = '/a'
            sel = response.xpath(p_template % prop + extra_html + '/text()')
            if sel:
                item[prop['name']] = sel[0].extract()
        yield item


def process_winner_li(w, country=None):

    wdata = {}
    wdata['link'] = BASE_URL + w.xpath('a/@href').extract()[0]
    text = ' '.join(w.xpath('descendant-or-self::text()').extract())
    # get comma-delineated name and strip trailing white-space
    wdata['name'] = text.split(',')[0].strip()
    year = re.findall('\d{4}', text)
    if year:
        wdata['year'] = int(year[0])
    else:
        wdata['year'] = 0
        print('Oops, no year in ', text)
    category = re.findall('Physics|Chemistry|Physiology or Medicine|Literature|Peace|Economics', text)
    if category:
        wdata['category'] = category[0]
    else:
        wdata['category'] = ''
        print('Oops, no category in ', text)
    if country:
        if text.find('*') != -1:
            wdata['nationality'] = ''
            wdata['born_in'] = country
        else:
            wdata['nationality'] = country
            wdata['born_in'] = ''
            # store a copy of the link's text-string for any manual corrections
    wdata['text'] = text
    return wdata
