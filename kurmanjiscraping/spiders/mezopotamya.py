import scrapy

from utils import normalize_text


class MezopotamyaSpider(scrapy.Spider):
    name = "mezopotamya"
    allowed_domains = ["mezopotamyaajansi43.com"]
    start_urls = ["https://www.mezopotamyaajansi43.com/kr/HEM-NCE"]

    def parse(self, response):
        articles = set(response.css(".column.column_2_3 .row a::attr(href)").getall())
        for article in articles:
            article_url = f"https://www.mezopotamyaajansi43.com{article}"
            yield scrapy.Request(article_url, callback=self.parse_article)

        next_page_endpoint = response.css(
            ".pagination.clearfix.page_margin_top_section .right ::attr(href)"
        ).get()
        if next_page_endpoint:
            url = f"{self.start_urls[0]}{next_page_endpoint}"
            yield scrapy.Request(url, callback=self.parse)

    def parse_article(self, response):
        text_list = response.css(".post_content.clearfix ::text").getall()
        title = response.css(".post_title ::text").get().strip()
        yield {
            "title": title,
            "content": normalize_text(text_list),
            "url": response.url,
        }
