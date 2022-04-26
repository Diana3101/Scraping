import scrapy
from scrapy.http import Request
from war2022_team4.items import War2022Team4Item


class RgruSpider(scrapy.Spider):
    name = 'rgru'
    allowed_domains = ['rg.ru']
    start_urls = ['https://rg.ru/sujet/3131/']

    def start_requests(self):
        for link_url in self.start_urls:
            print(link_url)
            # Request to get the HTML content
            request = Request(link_url, cookies={'store_language': 'en'},
                              callback=self.parse)
            yield request

    def parse(self, response):
        print("\n")
        print("HTTP STATUS: " + str(response.status))
        print(response.xpath("//h2/a/text()").get())
        print("\n")
        item = War2022Team4Item()
        # Gets HTML content where the article links are stored
        content = response.xpath('//div[@class="b-news-inner__list-item-wrapper"]')
        prev_url = ''
        for article_link in content.xpath('.//a'):
            if prev_url == article_link.xpath('.//@href').extract_first() or \
                    not article_link.xpath('.//@href').extract_first().startswith("/2"):
                continue

            item['article_url'] = article_link.xpath('.//@href').extract_first()
            prev_url = item['article_url']

            item['article_url'] = "https://rg.ru" + item['article_url']

            yield (item)
