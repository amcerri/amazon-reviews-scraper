import scrapy

class AmazonReviewsCategorySpider(scrapy.Spider):
    name = 'amazon_reviews_category'

    def __init__(self, *args, **kwargs):
        urls = kwargs.pop('urls', []) 
        if urls:
            self.start_urls = urls.split(',')
        self.logger.info(self.start_urls)
        super(AmazonReviewsCategorySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        pass