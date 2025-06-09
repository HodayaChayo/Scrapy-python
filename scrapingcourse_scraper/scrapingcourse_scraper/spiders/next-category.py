import scrapy
import re
import json

class SitemapSpider(scrapy.Spider):
    name = 'next_products'
    allowed_domains = ['next.co.il']

    # Your list of product page URLs
    start_urls = [
        "https://www.next.co.il/he/style/su029916/n51100#n51100",
    "https://www.next.co.il/he/style/st729187/u92898#u92898",
    "https://www.next.co.il/he/style/su478315/au5451#au5451",
    "https://www.next.co.il/he/style/su511979/al0349#al0349",
    "https://www.next.co.il/he/style/su413883/aa0138#aa0138",
    "https://www.next.co.il/he/style/su413496/e16055#e16055",
    "https://www.next.co.il/he/style/su568433/au0169#au0169",
    "https://www.next.co.il/he/style/su519591/au0159#au0159",
    "https://www.next.co.il/he/style/su478442/ah1082#ah1082",
    "https://www.next.co.il/he/style/su464407/ah1077#ah1077",
    "https://www.next.co.il/he/style/su410287/e96300#e96300",
    "https://www.next.co.il/he/style/st432697/n23333#n23333",
    "https://www.next.co.il/he/style/su119060/n16905#n16905",
    "https://www.next.co.il/he/style/su305096/b42831#b42831",
    "https://www.next.co.il/he/style/su415133/ac2746#ac2746",
    "https://www.next.co.il/he/style/su299210/f64789#f64789",
    "https://www.next.co.il/he/style/su413496/e16069#e16069",
    "https://www.next.co.il/he/style/su343268/e16082#e16082",
    "https://www.next.co.il/he/style/su348639/e23783#e23783",
    "https://www.next.co.il/he/style/su166207/b56989#b56989"
]

    scraped_data = [] # in json for spliting to excel sheets

    def parse(self, response):
        
        is_many_colors = response.css('.pdp-rtl-nhqfmf')
        
        #check if have many colors
        if is_many_colors:
            api_start = "https://www.next.co.il/he/_next/data/1014384/he/style/"
            variants = response.css('div[data-testid="colour-chips-button-group"]>button>img::attr(src)').getall()
            variants = [url.split('/')[-1].replace('.jpg', '') for url in variants]
            match = re.search(r'/style/([^/]+)/', response.url)
            if match:
                product = match.group(1)
            
            for variant in variants:
                api_url = f"{api_start}{product}/{variant.lower()}.json"
                yield scrapy.Request(url=api_url, callback=self.extract_product_colors, meta={'product_url': api_url})
            
        else:
            data = self.extract_product_details(response)
            self.scraped_data.append(data)
            yield data



    def extract_product_colors(self, response):
        api_data = json.loads(response.text)
        product_data = api_data['pageProps']['dehydratedState']['queries'][1]['state']['data']
        product_img = [item['imageUrl'] for item in product_data['itemMedia']]
        
        product_details = {
            "product_url": response.meta['product_url'],
            "product_name": product_data['title'],
            "product_sku": product_data['productCode'],
            "product_price": ''.join(re.findall(r'\d+', product_data['price'])),
            "product_img": 'https://xcdn.next.co.uk' + '\nhttps://xcdn.next.co.uk'.join(product_img),
            "product_description": product_data['itemDescription']['toneOfVoice'],
            "color": product_data['colour'],
        }
        print(product_data)
        self.scraped_data.append(product_details)
        yield product_details

    def extract_product_details(self, response):

        product_url = response.url
        product_name = response.css('h1.MuiTypography-h1 ::text').get()
        product_sku = response.css('span[data-testid="product-code"]::text').get()
        product_img = response.css('.pdp-css-1e4773f button img ::attr(src)').getall()
        product_img = [re.sub(r'\?.*$', '', url) for url in product_img]
        product_price = response.css('div[data-testid="product-now-price"] span ::text').get()
        product_price = ''.join(re.findall(r'\d+', product_price))
        product_description = response.css('p[data-testid="item-description"] ::text').get()

        product_details = {
            "product_url": product_url,
            "product_name": product_name,
            "product_sku": product_sku,
            "product_price": product_price,
            "product_img": '\n'.join(product_img),
            "product_description": product_description,
            "color": '',
        }

        return product_details
