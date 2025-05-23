import scrapy

from utils import normalize_text


class SerhatnewsSpider(scrapy.Spider):
    name = "serhatnews"
    allowed_domains = ["serhatnews.com"]
    start_urls = ["https://www.serhatnews.com/ku/hemu-nuce/page/1"]

    def parse(self, response):
        articles = set(response.css(".kanews-post-href::attr(href)").getall())
        for article in articles:
            yield scrapy.Request(article, callback=self.parse_article)

        next_page = response.css('link[rel="next"]::attr(href)').get()
        if next_page:
            yield scrapy.Request(
                url=next_page, callback=self.parse
            )

    def parse_article(self, response):
        title = response.css(".kanews-article-title ::text").get().strip()
        text_list = response.css(".entry-content-wrapper ::text").getall()
        exclude_text = ["SERHAT NEWS"]
        yield {
            "title": title,
            "content": normalize_text(text_list, exclude_text),
            "url": response.url,
        }
