import scrapy


class WelattvSpider(scrapy.Spider):
    name = "welattv"
    allowed_domains = ["welattv.com"]
    start_urls = ["https://welattv.com"]

    def parse(self, response):
        sections = response.css(".section-title a::attr(href)").getall()
        for section in sections:
            section_url = self.get_url(section)
            yield scrapy.Request(section_url, callback=self.parse_section)

    def parse_section(self, response):
        articles = response.css(".entry__title a::attr(href)").getall()
        for article in articles:
            url = self.get_url(article)
            yield scrapy.Request(url, self.parse_article)

        next_page = response.css(".pager-next a::attr(href)").get()
        if next_page:
            next_page_url = self.get_url(next_page)
            yield scrapy.Request(next_page_url, self.parse_section)

    def parse_article(self, response):
        title = response.css(".single-post__entry-title ::text").get()
        text_array = response.css(".entry__article ::text").getall()
        yield {
            "title": title,
            "content": "\n".join(text_array),
            "url": response.url,
        }

    def get_url(self, endpoint):
        if endpoint.startswith("/ko"):
            return f"{self.start_urls[0]}{endpoint}"

        return endpoint
