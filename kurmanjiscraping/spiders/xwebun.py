import scrapy


class XwebunSpider(scrapy.Spider):
    name = "xwebun"
    allowed_domains = ["xwebun2.org"]
    start_urls = ["https://xwebun2.org/cat/raman/quncik-nivis/"]

    def parse(self, response):
        authors = response.css(".td-authors-name a::attr(href)").getall()
        for author in authors:
            yield scrapy.Request(author, callback=self.parse_author)

    def parse_author(self, response):
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
            yield scrapy.Request(next_page, callback=self.parse_author)

    def parse_article(self, response):
        title = response.css("h1.tdb-title-text ::text").get()

        texts = texts = response.css(
            ".td_block_wrap.tdb_single_content.tdi_80.td-pb-border-top.td_block_template_1.td-post-content.tagdiv-type .tdb-block-inner.td-fix-index p::text"
        ).getall()
        text = "\n".join(texts)

        yield {
            "title": title,
            "content": text,
            "url": response.url,
        }
