import scrapy
import logging


class NupeltvDirectSpider(scrapy.Spider):
    name = "nupeltv"
    allowed_domains = ["nupel.tv"]
    start_urls = ["https://nupel.tv/kategori/kurdi/page/1/"]

    max_pages = 59

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,tr-TR;q=0.8,tr;q=0.7",
            "Referer": "https://nupel.tv/kategori/kurdi/",
        },
        "ROBOTSTXT_OBEY": True,
        "LOG_LEVEL": "INFO",
    }

    def parse(self, response):
        self.logger.info(f"Processing page: {response.url}")

        articles = response.css(
            ".l-section.wpb_row.height_small .w-post-elm.post_title.usg_post_title_1.entry-title.color_link_inherit a::attr(href)"
        ).getall()

        current_page = response.url.split("/")[-2]
        if current_page == "kurdi":
            current_page = 1
        else:
            current_page = int(current_page)

        self.logger.info(f"Found {len(articles)} articles on {current_page} page")

        for article_url in articles:
            yield scrapy.Request(article_url, callback=self.parse_article)

        if current_page < self.max_pages:
            next_page = current_page + 1
            next_url = f"https://nupel.tv/kategori/kurdi/page/{next_page}/"
            self.logger.info(f"Moving to page {next_page}: {next_url}")
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_article(self, response):
        title = response.css(".w-post-elm.post_title ::text").get()
        content_elements = response.css(".w-post-elm.post_content ::text").getall()
        content = "\n".join([text.strip() for text in content_elements if text.strip()])

        yield {
            "title": title,
            "content": content,
            "url": response.url,
        }
