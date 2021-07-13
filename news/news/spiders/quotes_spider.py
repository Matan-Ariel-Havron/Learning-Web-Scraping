from scrapy import Spider
from ..items import QuoteItem


class QuotesSpider(Spider):
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/'
    ]

    def parse(self, response):
        quote = QuoteItem()
        all_div_quotes = response.css('div.quote')

        for html_quote in all_div_quotes:
            title = html_quote.css('span.text::text').extract()
            author = html_quote.css('.author::text').extract()
            tags = html_quote.css('.tag::text').extract()

            quote['title'] = title
            quote['author'] = author
            quote['tags'] = tags
            yield quote

        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
