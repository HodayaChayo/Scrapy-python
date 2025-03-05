import scrapy
import re
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
from openpyxl import Workbook

class SitemapSpider(scrapy.Spider):
    name = "axis"
    allowed_domains = ["www.axis.com"]
    start_urls = ["https://www.axis.com/"]

    visited_urls = set()  # Store visited URLs to avoid duplicates

    scraped_data = [] # in json for spliting to excel sheets
    
    # for attributes table
    table_data = {
    'Camera_Image sensor': None, 'Camera_Image sensor size': None, 'Camera_Lightfinder': None,
    'Camera_Wide dynamic range': None, 'Camera_Min illumination/ light sensitivity (Color)': None,
    'Camera_Min illumination/ light sensitivity (B/W)': None, 'Video_Max video resolution': None,
    'Video_Max frames per second': None, 'Video_Electronic image stabilization': None, 'Lens_Focal length': None,
    'Lens_Optical zoom': None, 'Lens_Horizontal field of view': None, 'Lens_Vertical field of view': None,
    'Compression_Zipstream': None, 'Compression_H.264': None, 'Compression_H.265': None, 'Compression_Motion JPEG': None,
    'Audio_Audio Support': None, 'Network_PoE Class': None, 'Security_Signed OS': None, 'Security_Secure boot': None,
    'Security_Secure keystore': None, 'General_Remote focus': None, 'General_Remote zoom': None, 'General_Built-in IR': None,
    'General_Local storage (memory card slot)': None, 'General_Operating temperature': None, 'General_Outdoor Ready': None,
    'General_Vandal rating': None, 'General_IP rating': None, 'General_Designed for repaint': None, 'General_Sustainability': None,
    'Power_Power (max)': None, 'Power_Power (average)': None, 'None_Form factor': None, 'None_Included licenses': None,
    'None_System storage (TB)': None, 'None_Total HDD bays': None, 'None_Free HDD bays': None, 'None_HDDs included': None,
    'None_Supported RAID level': None, 'None_Default RAID level': None, 'None_PoE total output power': None,
    'None_Power over Ethernet Plus': None, 'None_Validated video channels': None, 'None_Validated recording bitrate (Mbit/s)': None,
    'None_Operating system': None, 'Camera_Thermal sensitivity (NETD)': None, 'Camera_Thermal sensor resolution': None,
    'Video_Day and Night functionality': None, 'Video_Multiple color palettes': None, 'Lens_Varifocal lens': None,
    'Lens_Aperture': None, 'Lens_Lens mount': None, 'Lens_Replaceable lens': None, 'Audio_Two-way audio': None,
    'System integration_Audio detection': None, 'System integration_Active tampering': None, 'System integration_Alarm inputs/outputs': None,
    'System integration_Serial connectors': None, 'System integration_AXIS Camera Application Platform': None,
    'System integration_Digital I/O': None, 'Network_Power over Ethernet': None, 'Security_HTTPS encryption': None,
    'Security_IEEE 802.1X': None, 'Power_DC input voltage': None, 'None_Power over Ethernet': None, 'None_PoE Class': None,
    'None_DC input voltage': None, 'None_DC Output - Max': None, 'None_Relays': None, 'None_Digital I/O': None,
    'None_Alarm inputs/outputs': None, 'None_Operating temperature': None, 'None_Plenum rating': None,
    'None_Access control standards': None, 'None_ONVIF Profile': None, 'None_Eligible for five year warranty': None,
    'None_HTTPS encryption': None, 'None_Power consumption (max)': None, 'None_Serial connectors': None,
    'Video_Max video resolution H.264': None, 'Video_Max video resolution H.265': None, 'Video_Zipstream': None,
    'Video_Zipstream encoding': None, 'Video_Wide dynamic range': None, 'Lens_Day and Night functionality': None,
    'Lens_Max frames per second': None, 'Lens_Electronic image stabilization': None, 'Audio_Built-in microphone': None,
    'Wireless connectivity_Cellular technology': None, 'Wireless connectivity_Cellular bands supported': None,
    'Wireless connectivity_Operator approvals': None, 'Wireless connectivity_Wireless': None,
    'Wireless connectivity_Wireless standard': None, 'Wireless connectivity_Bluetooth': None, 'General_OptimizedIR': None,
    'General_Local storage': None, 'General_HTTPS encryption': None, 'General_Positioning system': None,
    'General_Built-in accelerometer': None, 'General_Built-in gyroscope': None, 'General_Battery type': None,
    'None_System storage (TB) *': None, 'None_Free HDD bays *': None, 'None_HDDs included *': None, 'None_Default RAID level *': None,
    'Security_TPM': None, 'Power_AC input voltage': None, 'None_Max video resolution': None, 'None_Horizontal field of view': None,
    'None_Min illumination/ light sensitivity (Color)': None, 'None_Built-in IR': None, 'None_HDMI Output': None,
    'None_Wide dynamic range': None, 'None_Zipstream': None, 'None_Vandal rating': None, 'None_Outdoor Ready': None,
    'None_IP rating': None, 'Lens_Focal length *': None, 'Lens_Horizontal field of view *': None, 'Lens_Vertical field of view *': None,
    'System Integration_Audio detection': None, 'System Integration_Active tampering': None, 'System Integration_Alarm inputs/outputs': None,
    'System Integration_Serial connectors': None, 'System Integration_Video motion detection': None, 'Lens_Aperture *': None,
    'Pan, Tilt, Zoom_Digital Pan/Tilt': None, 'Pan, Tilt, Zoom_Digital zoom': None, 'None_Monitors supported': None,
    'Video_Max frames per second *': None, 'Analytics_Autotracking version': None, 'Analytics_Orientation aid': None,
    'Pan, Tilt, Zoom_Optical zoom': None, 'Pan, Tilt, Zoom_Pan range': None, 'Pan, Tilt, Zoom_Tilt range': None,
    'Pan, Tilt, Zoom_Guard tour': None, 'Lens_Detection range: Human (1.5px)': None, 'Lens_Detection range: Vehicle (1.5px)': None,
    'Pan, Tilt, Zoom_Remote PTRZ': None, 'Compression_AV1': None, 'System Integration_ONVIF Profile': None,
    'System Integration_AXIS Camera Application Platform': None, 'Network_Wireless': None, 'None_Max video resolution H.264': None,
    'None_Max video resolution H.265': None, 'None_Image sensor size': None, 'None_Focal length': None,
    'None_Vertical field of view': None, 'None_Day and Night functionality': None, 'None_Max frames per second': None,
    'None_Audio Support': None, 'None_Built-in microphone': None, 'None_Lightfinder': None, 'None_Zipstream encoding': None,
    'None_OptimizedIR': None, 'Camera_Min illumination/ light sensitivity (Color) *': None,
    'Camera_Min illumination/ light sensitivity (B/W) *': None, 'Lens_Optical zoom *': None,
    'Security_Axis Edge Vault': None, 'Audio_Built-in microphone *': None
}

 

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
            data = self.extract_product_details(response)
            self.scraped_data.append(data)
            yield data

        # Extract all internal links
        links = response.css("a::attr(href)").getall()
        for link in links:
            url = response.urljoin(link)
            if self.is_valid_url(url) and url not in self.visited_urls:
                yield scrapy.Request(url, callback=self.parse)

    def is_product_page(self, response):
        return bool(response.css('article.product-page') and response.url.startswith("https://www.axis.com/products"))

    def extract_product_details(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        # Reset values in table_data for this product
        for key in self.table_data.keys():
            self.table_data[key] = None

        breadcrumbs_text = response.css('.breadcrumb__list-item a ::text').getall()
        product_url = response.url
        product_name = response.css('h1.title-attention ::text').get().strip()
        product_img = response.css('#product-img-carousel-main picture img ::attr(src), .product-top__canon-product-image picture img ::attr(src)').getall()
        product_img_names = [re.search(r'([^/]+)\.[^.]+(?:\?|$)', url).group(1) for url in product_img if re.search(r'([^/]+)\.[^.]+(?:\?|$)', url)]
        under_title = response.css('.product-top__product-features .tagline ::text').get()
        check_list = response.css('.list-check-circle li ::text').getall()
        overview_text = response.css('#show-more-overview .paragraph-wrapper ::text').getall()
        overview_text = [text.strip() for text in overview_text if text.strip()]
        overview_videos = response.css('#show-more-overview .paragraph-wrapper iframe ::attr(data-src), #show-more-overview .paragraph-wrapper video a ::attr(href)').getall()
        overview_videos = list(dict.fromkeys(overview_videos))
        overview_photos = response.css('#show-more-overview .paragraph-wrapper picture img ::attr(src)').getall()
        
        # Iterate through each table
        for table in response.css('.field-group-table table'):
            category = table.css("caption.ac-table__caption::text").get()

            # Iterate through each row in the table
            for row in table.css("tbody tr"):
                key = row.css("td.ac-table__cell--first::text").get()
                value = row.css("td.ac-table__cell--centered::text, td.ac-table__cell--centered span::text").get()

                if key:
                    formatted_key = f"{category}_{key.strip()}"  # Prefix key with category name
                    if formatted_key not in self.table_data:
                        self.table_data[formatted_key] = None  # Add new key if not already present
                    self.table_data[formatted_key] = value.strip() if value else None

        product_details = {
            "categories": '\n'.join(breadcrumbs_text),
            "product_url": product_url,
            "product_name": product_name,
            "product_img": ('https://www.axis.com' if product_img else '') + '\nhttps://www.axis.com'.join(product_img),
            "product_img_names": '\n'.join(product_img_names),
            "under_title": under_title,
            "check_list": '\n'.join(check_list),
            "overview": '\n\n'.join(overview_text),
            "overview_videos": '\n'.join(overview_videos),
            "overview_photos": ('https://www.axis.com' if overview_photos else '') + '\nhttps://www.axis.com'.join(overview_photos),
        }

        product_details.update(self.table_data)

        return product_details

    def is_valid_url(self, url):
        return self.allowed_domains[0] in url and "mailto:" not in url and "#" not in url and url.startswith("https://www.axis.com/products")
        
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
        # self.export_to_excel()
        print(self.table_data)

    def export_to_excel(self):
        # Create a new Excel workbook
        workbook = Workbook()

        # Sheet 1: Main product details
        sheet1 = workbook.active
        sheet1.title = "Products"
        sheet1.append(["product_url", "product_name", "product_SKU", "product_price"])
        for item in self.scraped_data:
            sheet1.append([item["product_url"], item["product_name"], item["product_SKU"], item["product_price"]])

        # Sheet 2: categories
        sheet2 = workbook.create_sheet(title="categories")
        sheet2.append(["category_url", "category_name", "subcategory_url", "subcategory_name", "product_url", "product_name"])
        for item in self.scraped_data:
            sheet2.append([item["category_url"], item["category_name"], item["subcategory_url"], item["subcategory_name"], item["product_url"], item["product_name"]])

        # Save the workbook to a file
        workbook.save("scraped_data.xlsx")
        self.log("Data exported to scraped_data.xlsx")
