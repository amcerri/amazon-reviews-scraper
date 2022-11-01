import scrapy

class AmazonReviewsSpider(scrapy.Spider):
    name = 'amazon_reviews'

    def __init__(self, *args, **kwargs):
        urls = kwargs.pop('urls', []) 
        if urls:
            self.start_urls = urls.split(',')
        self.logger.info(self.start_urls)
        super(AmazonReviewsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        data = response.css('.a-color-base .a-text-normal')

        yield {
            'product': data.xpath('.//text()').extract_first(),
        }