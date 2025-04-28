import scrapy
import urllib.parse


def count_path_segments(url):
    parsed_url = urllib.parse.urlparse(url)

    path = parsed_url.path

    path = path.strip("/")

    if not path:
        return 0

    segments = path.split("/")
    return len(segments)


class XwebunSpider(scrapy.Spider):
    name = "xwebun"
    allowed_domains = ["xwebun2.org"]
    start_urls = ["https://xwebun2.org"]

    def parse(self, response):
        sections = response.css(".tdb-menu-item-text").xpath("../@href").getall()
        for section in sections:
            if "kirmancki" in section:
                continue
            if count_path_segments(section) <= 1:
                continue

            if "quncik-nivis" in section:
                continue

            if "/cat/hemu/" in section:
                continue

            yield scrapy.Request(section, callback=self.parse_section)

    def parse_section(self, response):
        article_links = response.css(
            ".entry-title.td-module-title a::attr(href)"
        ).getall()

        for article_link in article_links:
            yield scrapy.Request(article_link, callback=self.parse_article)

        next_page = (
            response.css("div.page-nav.td-pb-padding-side")
            .css('a[aria-label="next-page"]::attr(href)')
            .get()
        )

        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_section)

    def parse_article(self, response):
        title = response.css("h1.tdb-title-text ::text").get()

        texts = texts = response.css(
            ".td_block_wrap.tdb_single_content.tdi_80.td-pb-border-top.td_block_template_1.td-post-content.tagdiv-type .tdb-block-inner.td-fix-index ::text"
        ).getall()
        text = "\n".join(texts)

        yield {
            "title": title,
            "content": text,
            "url": response.url,
        }
