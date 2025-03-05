import scrapy
from urllib.parse import urlparse, urlunparse
from scrapy_selenium import SeleniumRequest
import re

class SitemapSpider(scrapy.Spider):
    name = "scraper7"
    allowed_domains = ["phonedepot.co.il"]
    start_urls = ["https://www.phonedepot.co.il/"]

    visited_urls = set()  # Store visited URLs to avoid duplicates

    def clean_url(self, url):
        """
        Remove query parameters from the URL to ensure duplicates are avoided.
        """
        parsed = urlparse(url)  # Break URL into parts
        cleaned_url = urlunparse(parsed._replace(query=""))  # Remove the query part
        return cleaned_url

    def start_requests(self):
        """
        Start requests using Selenium to ensure JavaScript-rendered content is fully loaded.
        """
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=5  # Ensure wait_time is correctly placed
            )

    def parse(self, response):
        # Clean the current response URL
        cleaned_url = self.clean_url(response.url)

        # Skip if URL has already been visited
        if cleaned_url in self.visited_urls:
            return
        self.visited_urls.add(cleaned_url)  # Add the cleaned URL to the visited set

        # Check if this is a product page
        if self.is_product_page(response):
            yield self.extract_product_details(response)

        # Extract all internal links
        links = response.css("a::attr(href)").getall()
        for link in links:
            url = response.urljoin(link)
            if self.is_valid_url(url) and url not in self.visited_urls:
                yield SeleniumRequest(
                    url=url,
                    callback=self.parse,
                    wait_time=5  # Correct placement
                )

    def is_product_page(self, response):
        """
        Determine if the page is a product page based on its URL.
        """
        return "product-page" in response.url

    def extract_product_details(self, response):

        breadcrumbs = response.css('div[data-hook="breadcrumbs"] a').getall()

        # breadcrumbs_href = response.css(".breadcrumb  a ::attr(href)").getall()
        # breadcrumbs_text = response.css(".breadcrumb  a ::text").getall()
        # category_url = breadcrumbs_href[2] if len(breadcrumbs_href) >= 3 else ""
        # category_name = breadcrumbs_text[2] if len(breadcrumbs_text) >= 3 else ""
        # category_url2 = breadcrumbs_href[3] if len(breadcrumbs_href) >= 4 else ""
        # category_name2 = breadcrumbs_text[3] if len(breadcrumbs_text) >= 4 else ""
        product_url = response.url
        product_name = response.css('h1[data-hook="product-title"] ::text').get()
        product_imgs = response.css('div[data-hook="product-gallery-root"] .slick-track wow-image img ::attr(src)').get()  

        product_details = {
            "breadcrumbs": breadcrumbs,
            # "category_url": category_url,
            # "category_name": category_name,
            # "category_url2": category_url2,
            # "category_name2": category_name2,
            "product_url": product_url,
            "product_name": product_name,
            "product_img": self.clean_image_url(product_imgs),
        }

        return product_details
    
    def clean_image_url(self, image_url):
        """
        Clean up image URL by removing unnecessary parameters.
        """
        return re.sub(r"/v1/.*", "", image_url) if image_url else None

    def is_valid_url(self, url):
        """
        Validate if a URL should be followed.
        """
        return self.allowed_domains[0] in url and "mailto:" not in url and "#" not in url
