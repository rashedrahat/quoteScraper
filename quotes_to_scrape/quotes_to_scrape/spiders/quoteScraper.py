# -*- coding: utf-8 -*-
import scrapy
from ..items import QuotesToScrapeItem


class QuoteScraperSpider(scrapy.Spider):
    name = 'quoteScraper'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')
        items = QuotesToScrapeItem()
        for quote in quotes:
            text = quote.css('.text::text').extract()
            author = quote.css('.author::text').extract()
            tags = quote.css('.tag::text').extract()

            items['text'] = text
            items['author'] = author
            items['tag'] = tags

            yield items

        next_page = response.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "next", " " ))]//a/@href').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
