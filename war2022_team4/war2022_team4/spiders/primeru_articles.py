import hashlib
import json

import scrapy
from scrapy.http import Request
from war2022_team4.items import War2022Team4Item


class PrimeruSpider(scrapy.Spider):
    name = 'primeru_articles'
    allowed_domains = ['1prime.ru']

    def start_requests(self):

        with open('primeru.json') as json_file:
            data = json.load(json_file)

        for link_url in data:
            print('URL: ' + link_url['article_url'])
            # Request to get the HTML content
            request = Request(link_url['article_url'], cookies={'store_language': 'ru'},
                              callback=self.parse)
            yield request

    def parse(self, response):
        item = War2022Team4Item()

        item['article_link'] = response.url
        item['article_uuid'] = hashlib.sha256(str(response.url).encode('utf-8')).hexdigest()
        item['article_id'] = response.url.split("/")[-1].split(".")[0]

        item['article_datetime'] = response.xpath('//div[@class="article-header__pre-title"]'
                                                  '/time[@class="article-header__datetime"]/@datetime').extract()

        item['article_title'] = response.xpath('//div[@itemprop="name"]/text()').extract()[0]

        content = response.xpath('//div[@class="article-body__content"]')
        text = []
        for article_text in content.xpath('.//p'):
            text.append(article_text.xpath('.//text()').extract())

        item['article_text'] = "\n" + " ".join([sent for sent_list in text for sent in sent_list])

        return (item)