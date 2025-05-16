import scrapy


class AjansawelatSpider(scrapy.Spider):
    name = "ajansawelat"
    allowed_domains = ["ajansawelat.com"]
    start_urls = ["https://ajansawelat.com"]

    def parse(self, response):
        sections = [
            "https://ajansawelat.com/hemu-nuce/",
            "https://ajansawelat.com/rojane/",
            "https://ajansawelat.com/jin/",
            "https://ajansawelat.com/cand/",
            "https://ajansawelat.com/abori/",
            "https://ajansawelat.com/politika/",
            "https://ajansawelat.com/ekoloji/",
            "https://ajansawelat.com/civak/",
            "https://ajansawelat.com/tenduristi/",
            "https://ajansawelat.com/daraz/",
            "https://ajansawelat.com/cihan/",
        ]

        for section in sections:
            yield scrapy.Request(section, callback=self.parse_section)

    def parse_section(self, response):
        articles = response.css(
            ".jeg_posts.jeg_block_container h3.jeg_post_title a::attr(href)"
        ).getall()
        for article in articles:
            yield scrapy.Request(article, callback=self.parse_article)

        next_page = response.css("a.page_nav.next::attr(href)").get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_section)

    def parse_article(self, response):
        title = response.css("div.jeg_inner_content h1.jeg_post_title ::text").get()
        text_array = response.css(
            "div.jeg_inner_content div.content-inner ::text"
        ).getall()

        yield {
            "title": title,
            "content": "\n".join([text.strip() for text in text_array if text.strip()]),
            "url": response.url,
        }
