import scrapy


class BianetSpider(scrapy.Spider):
    name = "bianet"
    allowed_domains = ["bianet.org"]
    start_urls = ["https://bianet.org/kurdi"]

    def parse(self, response):
        sections = [
            "/kategori/maf-29",
            "/kategori/jiyan-30",
            "/kategori/zayenda-civaki-31",
            "/kategori/abori-32",
            "/kategori/cand-u-huner-33",
            "/kategori/medya-34",
            "/kategori/nuce-38",
            "/kategori/cihan-35",
        ]

        for section in sections:
            section_url = f"https://bianet.org{section}"
            yield scrapy.Request(section_url, callback=self.parse_section)

    def parse_section(self, response):
        articles = response.css(".row.section__content a::attr(href)").getall()
        for article in articles:
            article_url = f"https://bianet.org{article}"
            yield scrapy.Request(article_url, self.parse_article)

        next_page = response.css(
            "div.pagination ul li.active + li a.page-link::attr(href)"
        ).get()

        if next_page:
            next_page_url = f"https://bianet.org{next_page}"
            yield scrapy.Request(next_page_url, self.parse_section)

    def parse_article(self, response):
        title = response.css(".top-part .txt-wrapper h1.headline::text").get()
        first = response.css(".top-part .txt-wrapper .desc::text").get()

        text_array = response.css(".bottom-part .content ::text").getall()

        yield {
            "title": title,
            "content": "\n".join(
                [text.strip() for text in [first, *text_array] if text.strip()]
            ),
            "url": response.url,
        }
