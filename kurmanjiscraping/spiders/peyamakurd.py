import scrapy

from utils import normalize_text


class PeyamakurdSpider(scrapy.Spider):
    name = "peyamakurd"
    allowed_domains = ["peyamakurd.info"]
    start_urls = ["https://peyamakurd.info/kurmanci"]

    def parse(self, response):
        sections = [
            "/kurmanci/kurdistan",
            # "/kurmanci/niviskar",
            "/kurmanci/cihan",
            "/kurmanci/huner",
            "/kurmanci/magazin",
            "/kurmanci/tendrusti",
            "/kurmanci/werzis",
            "/kurmanci/abori",
            "/kurmanci/hevpeyvin",
            "/kurmanci/analiz",
        ]

        for section in sections:
            section_url = f"https://peyamakurd.info{section}"
            yield scrapy.Request(section_url, callback=self.get_sections)

    def get_sections(self, response):
        target_text = "Ji bo nûçeyên hemî kategoriyê bikirtînin..."
        target_element = response.xpath(f'//a[contains(text(), "{target_text}")]')
        href = target_element.attrib["href"]
        section_url = f"https://peyamakurd.info{href}"
        yield scrapy.Request(section_url, callback=self.parse_section)

    def parse_section(self, response):
        articles = set(
            response.css("div.news-boxes.threeboxes div.boxes a::attr(href)").getall()
        )
        for article in articles:
            article_url = f"https://peyamakurd.info{article}"
            yield scrapy.Request(article_url, callback=self.parse_article)

        active_li = response.css("ul.pagination li.active")
        next_page_li = active_li.xpath("following-sibling::li[1]")
        if next_page_li:
            endpoint = next_page_li.css("a::attr(href)").get()
            url = f"https://peyamakurd.info{endpoint}"
            yield scrapy.Request(url, callback=self.parse_section)

    def parse_article(self, response):
        container = response.css("#content")
        title = container.css(".heading-detail h1::text").get()
        text_list = container.css("div.block ::text").getall()
        exclude_texts = ["PeyamaKurd –\xa0", "PeyamaKurd –", "PeyamaKurd" "PeyamaKurd "]
        yield {
            "title": title,
            "content": normalize_text(text_list, exclude_texts),
            "url": response.url,
        }
