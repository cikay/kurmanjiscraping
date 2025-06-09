import scrapy

from utils import normalize_text


class RupelanuSpider(scrapy.Spider):
    name = "rupelanu"
    allowed_domains = ["rupelanu.com"]
    start_urls = ["https://www.rupelanu.com/"]

    def parse(self, response):
        sections = [
            "https://www.rupelanu.com/cand-huner-haberleri-21hk-p1.htm",
            "https://www.rupelanu.com/kurdistan-haberleri-12hk-p1.htm",
            "https://www.rupelanu.com/cihan-haberleri-15hk-p1.htm",
        ]

        for section in sections:
            yield scrapy.Request(section, callback=self.parse_section)

    def parse_section(self, response):
        articles = set(
            response.css("div.box-news div.row ::attr(href)").getall()
        )

        for article in articles:
            yield scrapy.Request(article, callback=self.parse_article)

        next_page = response.css("div.holder a.next::attr(href)").get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_section)

    def parse_article(self, response):
        title = response.css("h1.content-title ::text").get().strip()
        text_list = response.css(".text-content ::text").getall()

        title, content = normalize_text(text_list, title)

        yield {
            "title": title,
            "content": content,
            "url": response.url,
        }
