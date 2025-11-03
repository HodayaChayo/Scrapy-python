import scrapy
from urllib.parse import urlparse, urlunparse
import re

class SitemapSpider(scrapy.Spider):
    name = "konimbo"
    allowed_domains = ["www.gruberfarm.com"]
    start_urls = ["https://www.gruberfarm.com/"]

    visited_urls = set()  # Store visited URLs to avoid duplicates

    table_data = {}

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
        return "gruberfarm.com/items/" in response.url

    def extract_product_details(self, response):

        # Reset values in table_data for this product
        for key in self.table_data.keys():
            self.table_data[key] = None

        breadcrumbs_href = response.css("#bread_crumbs  a ::attr(href)").getall()
        breadcrumbs_href = ["https://www.huntertools.co.il" + href for href in breadcrumbs_href]
        breadcrumbs_text = response.css("#bread_crumbs  a ::text").getall()
        category_url = breadcrumbs_href[2] if len(breadcrumbs_href) >= 3 else ""
        category_name = breadcrumbs_text[2] if len(breadcrumbs_text) >= 3 else ""
        category_url2 = breadcrumbs_href[3] if len(breadcrumbs_href) >= 4 else ""
        category_name2 = breadcrumbs_text[3] if len(breadcrumbs_text) >= 4 else ""
        category_url3 = breadcrumbs_href[4] if len(breadcrumbs_href) >= 5 else ""
        category_name3 = breadcrumbs_text[4] if len(breadcrumbs_text) >= 5 else ""
        category_url4 = breadcrumbs_href[5] if len(breadcrumbs_href) >= 6 else ""
        category_name4 = breadcrumbs_text[5] if len(breadcrumbs_text) >= 6 else ""
        product_url = response.url
        product_name = response.css("#item_current_title h1 span::text").get()
        if product_name:
            product_name = product_name.strip() 
        product_SKU = response.css(".code_item ::text").get()   
        if product_SKU:
            product_SKU = product_SKU.strip() 

        # product_imgs = response.css(".swiper-slide.productImage ::attr(data-src)").getall()    
        # product_img_names = [re.search(r'/([^/]+)$', url).group(1) for url in product_imgs if re.search(r'/([^/]+)$', url)]
        # description = response.css(".productOrVariationSpoiler .collapse ::text").getall()
        # description_html = response.css(".productOrVariationSpoiler .collapse").get()
        # if description_html:
        #     description_html = self.remove_unwanted_attributes(description_html)
        
       


        product_details = {
            "category_url": category_url,
            "category_name": category_name,
            "category_url2": category_url2,
            "category_name2": category_name2,
            "category_url3": category_url3,
            "category_name3": category_name3,
            "category_url4": category_url4,
            "category_name4": category_name4,
            "product_url": product_url,
            "product_name": product_name,
            "product_SKU": product_SKU,
            # "product_img": self.extract_product_images(product_imgs),
            # "product_img_names": product_img_names,
            # "description": description,
            # "description_html": description_html
        }

        product_details.update(self.table_data)

        return product_details
    

    def extract_product_images(self, product_imgs):
        # Join the image URLs into a single string, each separated by a newline
        return "https://www.huntertools.co.il" + "\nhttps://www.huntertools.co.il".join(product_imgs) if product_imgs else ""
    
    def remove_unwanted_attributes(self, html):
        # Regular expression to match any HTML tag
        def clean_tag(match):
            tag_name = match.group(1)
            attributes = match.group(2)

            # Only keep attributes for <a> and <img> tags
            if tag_name in ['a', 'img']:
                return f"<{tag_name}{attributes}>"
            else:
                return f"<{tag_name}>"

        # Regex to match tags and their attributes
        regex = re.compile(r'<(\w+)(\s+[^>]*?)>')

        # Apply the regex to remove unwanted attributes
        return re.sub(regex, clean_tag, html)
    
    def closed(self, reason):
        # Called when the spider finishes scraping
        print(self.table_data)

    def is_valid_url(self, url):
        return self.allowed_domains[0] in url and "mailto:" not in url and "#" not in url