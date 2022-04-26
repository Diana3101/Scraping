import hashlib
import json

import scrapy
from scrapy.http import Request
from war2022_team4.items import War2022Team4Item


class RgruSpider(scrapy.Spider):
    name = 'rgru_articles'
    allowed_domains = ['rg.ru']

    def start_requests(self):

        with open('rgru.json') as json_file:
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

        item['article_datetime'] = response.xpath('//div[@class="b-material-head__date"]/span/text()').extract()

        item['article_title'] = response.xpath('//title/text()').extract()

        text_bold = response.xpath('//div[@class="b-material-wrapper__lead"]/text()').extract()

        content = response.xpath('//div[@class="b-material-wrapper__text"]')
        text = []
        for article_text in content.xpath('.//p'):
            text.append(article_text.xpath('.//text()').extract())

        if text_bold:
            item['article_text'] = "\n" + " ".join([t for t in text_bold]) + "\n" + " ".join(
                [sent for sent_list in text for sent in sent_list])
        else:
            item['article_text'] = "\n" + " ".join([sent for sent_list in text for sent in sent_list])

        return (item)