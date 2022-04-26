import scrapy
from scrapy.http import Request
from war2022_team4.items import War2022Team4Item


class PrimeruSpider(scrapy.Spider):
    name = 'primeru'
    allowed_domains = ['1prime.ru']
    start_urls = ['https://1prime.ru/trend/_price_product_RF_10022015/']

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
        content = response.xpath('//div[@class="rubric-list__articles"]')
        for article_link in content.xpath('.//article/h2/a'):
            item['article_url'] = article_link.xpath('.//@href').extract_first()

            item['article_url'] = "https://1prime.ru" + item['article_url']

            yield (item)