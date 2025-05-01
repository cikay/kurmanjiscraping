import scrapy


class WelattvSpider(scrapy.Spider):
    name = "nuhev"
    allowed_domains = ["nuhev.com"]
    start_urls = ["https://www.nuhev.com/"]

    def parse(self, response):
        sections = response.css(
            ".jeg_nav_item.jeg_main_menu_wrapper a::attr(href)"
        ).getall()
        for section in sections:
            if section == "https://www.nuhev.com/market/":
                continue

            yield scrapy.Request(section, callback=self.parse_section)

    def parse_section(self, response):
        articles = response.css(".jeg_postblock_content a::attr(href)").getall()
        for article in articles:
            yield scrapy.Request(article, self.parse_article)

        next_page = response.css(".page_nav.next::attr(href)").get()
        if next_page:
            yield scrapy.Request(next_page, self.parse_section)

    def parse_article(self, response):
        title = response.css(".jeg_post_title ::text").get()
        text_array = response.css(".content-inner ::text").getall()
        yield {
            "title": title,
            "content": "\n".join([text.strip() for text in text_array if text.strip()]),
            "url": response.url,
        }
