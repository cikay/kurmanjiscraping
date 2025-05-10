import scrapy


class AnfkurdSpider(scrapy.Spider):
    name = "anfkurd"
    allowed_domains = ["anfkurdi.com"]
    start_urls = ["https://anfkurdi.com/"]

    def parse(self, response):
        sections = [
            "/rojane",
            "/kurdistan",
            "/jin",
            "/rojava-sUriye",
            "/civak-ekolojI",
            "/cihan",
            "/Cand-U-huner",
            "/ewropa",
            "/analIz",
            "/zanist",
        ]
        for section in sections:
            section_url = f"https://anfkurdi.com{section}"
            yield scrapy.Request(section_url, callback=self.parse_section)

    def parse_section(self, response):
        articles = response.css("#last-news ::attr(href)").getall()
        for article in articles:
            yield scrapy.Request(article, callback=self.parse_article)

        next_button = response.css(".pagination li.next")
        if next_button and "disabled" not in next_button.attrib.get("class", ""):
            next_page_endpoint = next_button.css("a::attr(href)").get()
            if next_page_endpoint:
                next_page = f"https://anfkurdi.com{next_page_endpoint}"
                yield scrapy.Request(next_page, callback=self.parse_section)


    def parse_article(self, response):
        title = response.css("div.post-content h2.entry-title ::text").get()
        text_array = response.css("div.post-content div.entry-content ::text").getall()

        yield {
            "title": title,
            "content": "\n".join([text.strip() for text in text_array if text.strip()]),
            "url": response.url,
        }
