import scrapy


class ToScrapeSpider(scrapy.Spider):
    name = "toscrape-xpath"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        # For a specific tag, use: -a tag='tag_name'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('span[@class="text"]/text()').get(),
                'author': quote.xpath('span/small[@class="author"]/text()').get(),
                'tags': quote.xpath('div[@class="tags"]/a[@class="tag"]/text()').getall(),
            }

        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
