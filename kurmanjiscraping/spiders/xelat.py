import scrapy


class XelatSpider(scrapy.Spider):
    name = "xelat"
    allowed_domains = ["xelat.org"]
    start_urls = ["https://xelat.org/"]

    def parse(self, response):
        sections = response.css(".section-head a::attr(href)").getall()
        for section in sections:
            yield scrapy.Request(section, callback=self.parse_section)

    def parse_section(self, response):
        articles_url = response.css(".post-item-image a::attr(href)").getall()
        for url in articles_url:
            yield scrapy.Request(url, callback=self.parse_article)

        next_page_url = response.css("li.next a::attr(href)").get()
        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse_section)

    def parse_article(self, response):
        title = response.css("h1.title ::text").get()
        text_array = response.css(".post-text ::text").getall()
        filtered = []
        for item in text_array:
            if item.strip() not in {"Xelat", "XELAT"}:
                filtered.append(item)

        yield {
            "title": title,
            "content": "\n".join(filtered),
            "url": response.url,
        }
