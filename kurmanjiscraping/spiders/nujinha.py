import scrapy

from utils import normalize_text


class NujinhaSpider(scrapy.Spider):
    name = "nujinha"
    allowed_domains = ["jinhaagency1.com"]
    start_urls = ["https://jinhaagency1.com/ku"]

    def parse(self, response):
        sections = [
            # "https://jinhaagency1.com/ku/latest-news",
            "https://jinhaagency1.com/ku/rojane",
            "https://jinhaagency1.com/ku/siyaset",
            "https://jinhaagency1.com/ku/civak-jiyan",
            "https://jinhaagency1.com/ku/ked-u-abori",
            "https://jinhaagency1.com/ku/cand-u-huner",
            "https://jinhaagency1.com/ku/ekoloji",
            "https://jinhaagency1.com/ku/dosya",
            "https://jinhaagency1.com/ku/hiqûq",
            "https://jinhaagency1.com/ku/lista-roje",
            "https://jinhaagency1.com/ku/tenduristi",
            "https://jinhaagency1.com/ku/cihwar-jin",
            "https://jinhaagency1.com/ku/werzis",
        ]

        for section in sections:
            yield scrapy.Request(section, callback=self.parse_section)

    def parse_section(self, response):
        if response.url == "https://jinhaagency1.com/ku/latest-news":
            yield from self.parse_latest_news(response)
        else:
            yield from self.parse_section_others(response)

    def parse_section_others(self, response):
        articles = set(
            response.css(
                ".category-items.category-items--lis a.title::attr(href)"
            ).getall()
        )

        for article in articles:
            yield scrapy.Request(article, callback=self.parse_article)

        next_page_li = response.css("div.paginator ul.pagination li.next")
        if next_page_li and not next_page_li.css("::attr(class)").re(r"disabled"):
            next_page_url = next_page_li.css("a::attr(href)").get()
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse_section_others)

    def parse_latest_news(self, response):
        articles = set(response.css(".latest-news-index a::attr(href)").getall())
        for article in articles:
            yield scrapy.Request(article, callback=self.parse_article)

        next_page_li = response.css("div.paginator ul.pagination li.next")
        if next_page_li and not next_page_li.css("::attr(class)").re(r"disabled"):
            next_page_url = next_page_li.css("a::attr(href)").get()
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse_latest_news)

    def parse_article(self, response):
        title = response.css("article.post h2.entry-title ::text").get().strip()
        text_list = response.xpath(
            "//article[@class='post']//text()[not(ancestor::ul[contains(@class, 'list-inline')])]"
        ).getall()

        title, content = normalize_text(text_list, title)

        yield {
            "title": title,
            "content": content,
            "url": response.url,
        }
