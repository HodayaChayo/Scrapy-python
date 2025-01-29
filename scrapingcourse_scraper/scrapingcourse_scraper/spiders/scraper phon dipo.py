import scrapy
from urllib.parse import urlparse, urlunparse
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

    def parse(self, response):
        # Clean the current response URL
        cleaned_url = self.clean_url(response.url)

        # Skip if URL has already been visited
        if cleaned_url in self.visited_urls:
            return
        self.visited_urls.add(response.url)  # Add the URL to the visited set

        # Check if this is a product page
        if self.is_product_page(response):
            yield self.extract_product_details(response)

        # Extract all internal links
        links = response.css("a::attr(href)").getall()
        for link in links:
            url = response.urljoin(link)
            if self.is_valid_url(url) and url not in self.visited_urls:
                yield scrapy.Request(url, callback=self.parse)

    def is_product_page(self, response):
        if "product-page" in response.url:
            return True
        else: 
            return False

    def extract_product_details(self, response):

        product_url = response.url
        product_name = response.css('h1[data-hook="product-title"] ::text').get()
        product_imgs = response.css('div[data-hook="product-gallery-root"] .slick-track wow-image img ::attr(src)').get()  

        product_details = {
            "product_url": product_url,
            "product_name": product_name,
            "product_img": self.clean_image_url(product_imgs),
        }

        product_details.update(self.table_data)

        return product_details
    
    
    def clean_image_url(self, image_url):
        return re.sub(r"/v1/.*", "", image_url) if image_url else None

    def is_valid_url(self, url):
        return self.allowed_domains[0] in url and "mailto:" not in url and "#" not in url