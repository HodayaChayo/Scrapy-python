import scrapy


class ScraperSpider(scrapy.Spider):
    name = "scraper2"
    allowed_domains = ["www.ledico.com"]
    start_urls = ["https://www.ledico.com/sectors/"]

    visited_urls = set()  # A set to store visited URLs


    def parse(self, response):
        # Get all category links
        categories = response.css("#menu-item-445 > ul > li > a")

        for category in categories:
            category_name = category.attrib.get("aria-label")
            category_url = category.attrib.get("href")

            if category_url not in self.visited_urls:
                self.visited_urls.add(category_url)  # Mark URL as visited
                # Follow each category URL to extract subcategory data
                yield scrapy.Request(
                    url=response.urljoin(category_url),
                    callback=self.parse_category,  # Use a separate method to parse subcategories
                    meta={"subcategory_url": category_url, "subcategory_name": category_name}  # Pass the parent category URL for context
                )

    def parse_category(self, response):
        is_product = response.css(".product_wrapper")
        if is_product:
            product_name = response.css(".product_wrapper h1 ::text").get()
            product_url = response.url
            product_price = response.css(".product_wrapper .woocommerce-Price-amount ::text").get()
            if product_price:
                product_price = product_price.replace(u'\xa0', u'')
            product_img = response.css(".woocommerce-product-gallery__image > a::attr(href)").get()
            prosuct_description = response.css(".woocommerce-product-details__short-description").get()
            product_SKU = response.css(".sku ::text").get()

            table_rows = response.css(".technical_description-div table tr")
            table_data = {}
            for row in table_rows:
                key = row.css("td:nth-child(2) ::text").get()
                value = row.css("td:nth-child(1) ::text").get()
                if key and value:
                    table_data[key.strip()] = value.strip()

            yield {
                **response.meta,
                "product_url": product_url,
                "product_name": product_name,
                "prosuct_description": prosuct_description,
                "product_SKU": product_SKU,
                "product_price": product_price,
                "product_img": product_img,
                "technical_data": table_data,
            }

        else:            
            # Extract subcategory details
            subcategories = response.css(".isotope-item a")  # Update this selector if needed
            for subcategory in subcategories:
                
                subcategory_name = subcategory.css(".name-m ::text").get()  # Text of the subcategory
                subcategory_url = subcategory.attrib.get("href")  # URL of the subcategory

                if subcategory_url not in self.visited_urls:
                    self.visited_urls.add(subcategory_url)  # Mark URL as visited

                    # Dynamically determine the next available subcategory key
                    meta = response.meta.copy()  # Copy the existing meta to avoid altering it directly
                    counter = 1  # Start with subcategory_name1/subcategory_url1
                    
                    # Find the next available subcategory name and URL keys
                    while f"subcategory_name{counter}" in meta:
                        counter += 1

                    # Add the new unique subcategory name and URL to meta
                    meta[f"subcategory_name{counter}"] = subcategory_name
                    meta[f"subcategory_url{counter}"] = response.urljoin(subcategory_url)

                    # Create and yield the request with the updated meta
                    yield scrapy.Request(
                        url=response.urljoin(subcategory_url),
                        callback=self.parse_category,
                        meta=meta
                    )

                # Handle pagination if ".pages" exists
                pagination_links = response.css(".pages a.page-numbers::attr(href)").getall()
                for link in pagination_links:
                    paginated_url = response.urljoin(link)
                    if paginated_url not in self.visited_urls:
                        self.visited_urls.add(paginated_url)  # Mark URL as visited
                        yield scrapy.Request(
                            url=response.urljoin(link),
                            callback=self.parse_category,  # Call parse_category to process paginated pages
                            meta=response.meta.copy()  # Keep the current meta
                        )
