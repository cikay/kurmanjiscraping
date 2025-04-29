import scrapy
import re
import json


class NlkaNetSpider(scrapy.Spider):
    name = "nlka_net"
    allowed_domains = ["nlka.net"]
    start_urls = ["https://nlka.net/ku"]

    def parse(self, response):
        sections = response.css(".section-heading.sh-t6.sh-s2 a::attr(href)").getall()

        self.logger.info(f"Found {len(sections)} sections: {sections}")

        for section in sections:
            yield scrapy.Request(section, callback=self.parse_section)

    def parse_section(self, response):
        self.logger.info(f"Processing section: {response.url}")

        articles = response.css(".post-title.post-url::attr(href)").getall()
        self.logger.info(f"Found {len(articles)} articles in this page")

        for article in articles:
            yield scrapy.Request(article, callback=self.parse_article)

        # Handle pagination - check if this is AJAX-based pagination
        pagination_data = self.extract_pagination_data(response)

        if pagination_data:
            current_page = pagination_data.get("current_page", 1)
            max_pages = pagination_data.get("max_num_pages", 1)

            self.logger.info(
                f"Pagination info: current page {current_page}, max pages {max_pages}"
            )

            if current_page < max_pages:
                next_page_url = self.construct_next_page_url(
                    response.url, current_page + 1
                )
                self.logger.info(f"Moving to next page: {next_page_url}")
                yield scrapy.Request(next_page_url, callback=self.parse_section)
        else:
            # Try traditional pagination if AJAX pagination data not found
            next_page = response.css(".btn-bs-pagination.next::attr(href)").get()
            if next_page:
                self.logger.info(f"Found traditional next page: {next_page}")
                yield scrapy.Request(next_page, callback=self.parse_section)

    def extract_pagination_data(self, response):
        """Extract pagination data from JavaScript variables in the page"""
        # Look for pagination data in script tags
        script_content = response.xpath(
            '//script[contains(., "bs_ajax_paginate_")]/text()'
        ).get()

        if not script_content:
            return None

        try:
            # Extract the JSON configuration for pagination
            pagination_match = re.search(
                r"var bs_ajax_paginate_\d+ = (.*?);", script_content
            )
            if pagination_match:
                pagination_data = json.loads(pagination_match.group(1))
                return pagination_data

            # Alternative pattern to find pagination data
            pages_match = re.search(
                r'"max_num_pages":(\d+).*?"current_page":(\d+)', script_content
            )
            if pages_match:
                max_pages = int(pages_match.group(1))
                current_page = int(pages_match.group(2))
                return {"max_num_pages": max_pages, "current_page": current_page}
        except Exception as e:
            self.logger.error(f"Error extracting pagination data: {e}")

        return None

    def construct_next_page_url(self, current_url, next_page):
        """Construct URL for the next page based on current URL patterns"""
        # Check if the URL already has a page parameter
        if "page/" in current_url:
            return re.sub(r"page/\d+", f"page/{next_page}", current_url)
        else:
            # Add page parameter
            if current_url.endswith("/"):
                return f"{current_url}page/{next_page}/"
            else:
                return f"{current_url}/page/{next_page}/"

    def parse_article(self, response):
        self.logger.info(f"Processing article: {response.url}")

        title = response.css(".single-post-title ::text").get()
        if title:
            title = title.strip()
        else:
            title = "No title found"

        paragraphs = response.css(".continue-reading-content p")
        filtered_paragraphs = []

        if paragraphs:
            first = paragraphs[0].css("::text").get()
            if first and (
                "Made bi erebî" in first
                or "ألعربية" in first
                or re.search(r"Made bi \w+", first)
            ):
                start = 1
            else:
                start = 0

            for index in range(start, len(paragraphs)):
                p_tag = paragraphs[index]
                p_text = " ".join(p_tag.css("::text").getall()).strip()
                if p_text:
                    filtered_paragraphs.append(p_text)

        content = "\n".join(filtered_paragraphs)

        yield {
            "title": title,
            "content": content,
            "url": response.url,
        }
