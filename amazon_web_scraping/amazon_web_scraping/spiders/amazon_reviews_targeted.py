import scrapy

class AmazonReviewsTargetedSpider(scrapy.Spider):
    name = 'amazon_reviews_targeted'

    def __init__(self, *args, **kwargs):
        urls = kwargs.pop('urls', []) 
        if urls:
            self.start_urls = urls.split(',')
        self.logger.info(self.start_urls)
        super(AmazonReviewsTargetedSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # Navigate to "All reviews" page
        all_reviews_page = response.css('a[data-hook="see-all-reviews-link-foot"]::attr(href)').get()
        if all_reviews_page:
            yield response.follow(all_reviews_page, callback=self.parse)
        else:
            for review in response.css('div[data-hook="review"]'):
                yield {
                    'product_name': response.css('.a-text-ellipsis .a-link-normal::text').get(),
                    'review_title': review.css('a[data-hook="review-title"] span::text').get(),
                    'review_body': review.css('span[data-hook="review-body"] span::text').get(),
                    'review_author': review.css('.a-profile-content span::text').get(),
                    'review_rating': review.css('i[data-hook="review-star-rating"] span::text').get(),
                    'review_date': review.css('span[data-hook="review-date"]::text').get(),
                    'review_helpful_votes': review.css('span[data-hook="helpful-vote-statement"]::text').get(),
                }

            next_page = response.css('li.a-last a::attr(href)').get()
            # check if there is a next page and next page doesn't contain the class a-disabled
            if next_page and not 'a-disabled' in next_page:
                yield response.follow(next_page, callback=self.parse)

            response.css('a[data-hook="see-all-reviews-link-foot"]::attr(href)').get()
        