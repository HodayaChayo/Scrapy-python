import scrapy
import re
import json

class SitemapSpider(scrapy.Spider):
    name = 'next_products'
    allowed_domains = ['next.co.il']

    # Your list of product page URLs
    start_urls = [
        "https://www.next.co.il/en/style/su477532/aj5454#aj5454",
    "https://www.next.co.il/en/style/su477532/an8454#an8454",
    "https://www.next.co.il/en/style/su402127/e85115#e85115",
    "https://www.next.co.il/en/style/su402127/e85114#e85114",
    "https://www.next.co.il/en/style/su541255/aw4287#aw4287",
    "https://www.next.co.il/en/style/su541255/aw4284#aw4284",
    "https://www.next.co.il/en/style/su304489/b94099#b94099",
    "https://www.next.co.il/en/style/su304489/aa6943#aa6943",
    "https://www.next.co.il/en/style/su429119/aa8183#aa8183",
    "https://www.next.co.il/en/style/su429119/an6604#an6604",
    "https://www.next.co.il/en/style/su460277/ag6898#ag6898",
    "https://www.next.co.il/en/style/su460277/ag6896#ag6896",
    "https://www.next.co.il/en/style/su507099/am0183#am0183",
    "https://www.next.co.il/en/style/su507099/am0172#am0172",
    "https://www.next.co.il/en/style/su541255/aw4284#aw4284",
    "https://www.next.co.il/en/style/su541255/aw4286#aw4286",
    "https://www.next.co.il/en/style/su507099/am0177#am0177",
    "https://www.next.co.il/en/style/su507099/am0172#am0172",
    "https://www.next.co.il/en/style/su540971/aw3981#aw3981",
    "https://www.next.co.il/en/style/su540971/aw3975#aw3975",
    "https://www.next.co.il/en/style/su502335/al5331#al5331",
    "https://www.next.co.il/en/style/su502335/al5339#al5339",
    "https://www.next.co.il/en/style/su477534/aj5456#aj5456",
    "https://www.next.co.il/en/style/su683089/f92045#f92045",
    "https://www.next.co.il/en/style/su683089/f92060#f92060",
    "https://www.next.co.il/en/style/su563818/ay5972#ay5972",
    "https://www.next.co.il/en/style/su563818/ay5976#ay5976",
    "https://www.next.co.il/en/style/su402131/e85144#e85144",
    "https://www.next.co.il/en/style/su402131/e85122#e85122",
    "https://www.next.co.il/en/style/su029164/999399#999399",
    "https://www.next.co.il/en/style/su029164/n09165#n09165",
    "https://www.next.co.il/en/style/su569368/e45311#e45311",
    "https://www.next.co.il/en/style/su569368/e45303#e45303",
    "https://www.next.co.il/en/style/su518738/at7962#at7962",
    "https://www.next.co.il/en/style/su353662/n94801#n94801",
    "https://www.next.co.il/en/style/su353662/n98452#n98452",
    "https://www.next.co.il/en/style/su541884/aw4395#aw4395",
    "https://www.next.co.il/en/style/su541884/aw4396#aw4396",
    "https://www.next.co.il/en/style/su460276/ag6895#ag6895",
    "https://www.next.co.il/en/style/su460276/ag6892#ag6892",
    "https://www.next.co.il/en/style/su156620/n76943#n76943",
    "https://www.next.co.il/en/style/su156620/n09722#n09722",
    "https://www.next.co.il/en/style/su540578/aw2851#aw2851",
    "https://www.next.co.il/en/style/su540578/aw2853#aw2853",
    "https://www.next.co.il/en/style/su518143/at7945#at7945",
    "https://www.next.co.il/en/style/su518143/at7955#at7955",
    "https://www.next.co.il/en/style/su507220/am0620#am0620",
    "https://www.next.co.il/en/style/su507220/am0618#am0618",
    "https://www.next.co.il/en/style/su402132/e85116#e85116",
    "https://www.next.co.il/en/style/su402132/e85130#e85130",
    "https://www.next.co.il/en/style/su066371/q57833#q57833",
    "https://www.next.co.il/en/style/su066371/u78354#u78354",
    "https://www.next.co.il/en/style/su160859/e26127#e26127",
    "https://www.next.co.il/en/style/su160859/q82000#q82000",
    "https://www.next.co.il/en/style/su643026/f50327#f50327",
    "https://www.next.co.il/en/style/su643026/f40339#f40339",
    "https://www.next.co.il/en/style/su226545/693046#693046",
    "https://www.next.co.il/en/style/su226545/692933#692933",
    "https://www.next.co.il/en/style/su262844/n94795#n94795",
    "https://www.next.co.il/en/style/su262844/n94775#n94775",
    "https://www.next.co.il/en/style/su502448/al5620#al5620",
    "https://www.next.co.il/en/style/su502448/al5622#al5622",
    "https://www.next.co.il/en/style/su262842/n90207#n90207",
    "https://www.next.co.il/en/style/su262842/n90210#n90210",
    "https://www.next.co.il/en/style/su593566/q57098#q57098",
    "https://www.next.co.il/en/style/su593566/q56971#q56971",
    "https://www.next.co.il/en/style/su526537/au6850#au6850",
    "https://www.next.co.il/en/style/su526537/au6864#au6864",
    "https://www.next.co.il/en/style/su555731/ay3216#ay3216",
    "https://www.next.co.il/en/style/su555731/am9558#am9558",
    "https://www.next.co.il/en/style/su665010/av4680#av4680",
    "https://www.next.co.il/en/style/su665010/av4776#av4776",
    "https://www.next.co.il/en/style/su518143/av7759#av7759",
    "https://www.next.co.il/en/style/su518143/at7945#at7945",
    "https://www.next.co.il/en/style/su227994/am9555#am9555",
    "https://www.next.co.il/en/style/su227994/702154#702154",
    "https://www.next.co.il/en/style/su419406/aa6907#aa6907",
    "https://www.next.co.il/en/style/su419406/aa6908#aa6908",
    "https://www.next.co.il/en/style/su419408/aa6910#aa6910",
    "https://www.next.co.il/en/style/su419408/aa6909#aa6909",
    "https://www.next.co.il/en/style/su502335/al5339#al5339",
    "https://www.next.co.il/en/style/su502335/al5331#al5331",
    "https://www.next.co.il/en/style/su555659/k95319#k95319",
    "https://www.next.co.il/en/style/su555659/k95282#k95282",
    "https://www.next.co.il/en/style/su160859/q82000#q82000",
    "https://www.next.co.il/en/style/su160859/q81922#q81922",
    "https://www.next.co.il/en/style/su429119/an6606#an6606",
    "https://www.next.co.il/en/style/su429119/aa8183#aa8183",
    "https://www.next.co.il/en/style/su105916/q90083#q90083",
    "https://www.next.co.il/en/style/su105916/n18453#n18453",
    "https://www.next.co.il/en/style/su428968/ab8990#ab8990",
    "https://www.next.co.il/en/style/su428968/ab8980#ab8980",
    "https://www.next.co.il/en/style/su603245/f11821#f11821",
    "https://www.next.co.il/en/style/su603245/f11819#f11819",
    "https://www.next.co.il/en/style/su402127/e85114#e85114",
    "https://www.next.co.il/en/style/su402127/e85115#e85115",
    "https://www.next.co.il/en/style/su756623/aa7708#aa7708",
    "https://www.next.co.il/en/style/su756623/an6632#an6632",
    "https://www.next.co.il/en/style/su419406/aa6908#aa6908",
    "https://www.next.co.il/en/style/su419406/aa6907#aa6907",
    "https://www.next.co.il/en/style/st696598/aa6931#aa6931",
    "https://www.next.co.il/en/style/st696598/a82465#a82465",
    "https://www.next.co.il/en/style/su428969/ab8991#ab8991",
    "https://www.next.co.il/en/style/su428969/ab8997#ab8997",
    "https://www.next.co.il/en/style/st887155/m49691#m49691",
    "https://www.next.co.il/en/style/st887155/m49692#m49692",
    "https://www.next.co.il/en/style/su742325/n95240#n95240",
    "https://www.next.co.il/en/style/su353662/n98452#n98452",
    "https://www.next.co.il/en/style/su353662/n94801#n94801",
    "https://www.next.co.il/en/style/su536746/av7916#av7916",
    "https://www.next.co.il/en/style/su536746/av7911#av7911",
    "https://www.next.co.il/en/style/su713450/w32381#w32381",
    "https://www.next.co.il/en/style/su105916/n18453#n18453",
    "https://www.next.co.il/en/style/su105916/q90083#q90083",
    "https://www.next.co.il/en/style/su234963/835279#835279",
    "https://www.next.co.il/en/style/su234963/835223#835223",
    "https://www.next.co.il/en/style/su722907/w35505#w35505",
    "https://www.next.co.il/en/style/su634987/f44032#f44032",
    "https://www.next.co.il/en/style/su634987/f44022#f44022",
    "https://www.next.co.il/en/style/su683676/f91210#f91210",
    "https://www.next.co.il/en/style/su405455/e89434#e89434",
    "https://www.next.co.il/en/style/su405455/aj6998#aj6998",
    "https://www.next.co.il/en/style/su534523/av5613#av5613",
    "https://www.next.co.il/en/style/su534523/av5603#av5603",
    "https://www.next.co.il/en/style/st369149/d38900#d38900",
    "https://www.next.co.il/en/style/st369149/d38899#d38899",
    "https://www.next.co.il/en/style/su263893/n94099#n94099",
    "https://www.next.co.il/en/style/su263893/n90818#n90818",
    "https://www.next.co.il/en/style/su062910/u66873#u66873",
    "https://www.next.co.il/en/style/su062910/u66840#u66840",
    "https://www.next.co.il/en/style/st184430/387202#387202",
    "https://www.next.co.il/en/style/st184430/a65926#a65926",
    "https://www.next.co.il/en/style/su288177/b77207#b77207",
    "https://www.next.co.il/en/style/su288177/b68849#b68849",
    "https://www.next.co.il/en/style/su105916/b36411#b36411",
    "https://www.next.co.il/en/style/su105916/n18453#n18453",
    "https://www.next.co.il/en/style/su354322/921775#921775",
    "https://www.next.co.il/en/style/su354322/835248#835248",
    "https://www.next.co.il/en/style/su345177/e18399#e18399",
    "https://www.next.co.il/en/style/su345177/e18396#e18396",
    "https://www.next.co.il/en/style/su526515/au6866#au6866",
    "https://www.next.co.il/en/style/su526515/au6875#au6875",
    "https://www.next.co.il/en/style/su540526/aw2801#aw2801",
    "https://www.next.co.il/en/style/su540526/aw2800#aw2800",
    "https://www.next.co.il/en/style/su737855/b17565#b17565",
    "https://www.next.co.il/en/style/su587620/ar1455#ar1455",
    "https://www.next.co.il/en/style/su540971/aw3975#aw3975",
    "https://www.next.co.il/en/style/su540971/aw3981#aw3981",
    "https://www.next.co.il/en/style/su502331/al5333#al5333",
    "https://www.next.co.il/en/style/su502331/al5335#al5335",
    "https://www.next.co.il/en/style/su461966/ad9645#ad9645",
    "https://www.next.co.il/en/style/su253115/k93205#k93205",
    "https://www.next.co.il/en/style/su253115/k93244#k93244",
    "https://www.next.co.il/en/style/su234941/835127#835127",
    "https://www.next.co.il/en/style/su234941/835142#835142",
    "https://www.next.co.il/en/style/su541884/aw4398#aw4398",
    "https://www.next.co.il/en/style/su541884/aw4394#aw4394",
    "https://www.next.co.il/en/style/su345176/e18403#e18403",
    "https://www.next.co.il/en/style/su345176/e18398#e18398",
    "https://www.next.co.il/en/style/su518734/ah3733#ah3733",
    "https://www.next.co.il/en/style/su518734/ah3731#ah3731",
    "https://www.next.co.il/en/style/su148793/346878#346878",
    "https://www.next.co.il/en/style/su148793/334593#334593",
    "https://www.next.co.il/en/style/su477540/aj5462#aj5462",
    "https://www.next.co.il/en/style/su477536/aj5458#aj5458",
    "https://www.next.co.il/en/style/su541884/aw4396#aw4396",
    "https://www.next.co.il/en/style/su541884/aw4394#aw4394",
    "https://www.next.co.il/en/style/su540526/aw2802#aw2802",
    "https://www.next.co.il/en/style/su540526/aw2800#aw2800",
    "https://www.next.co.il/en/style/su263893/n90818#n90818",
    "https://www.next.co.il/en/style/su263893/n94099#n94099",
    "https://www.next.co.il/en/style/su304468/b84580#b84580",
    "https://www.next.co.il/en/style/su304468/b98576#b98576",
    "https://www.next.co.il/en/style/su507070/aw2761#aw2761",
    "https://www.next.co.il/en/style/su507070/am0157#am0157",
    "https://www.next.co.il/en/style/su542239/aw4564#aw4564",
    "https://www.next.co.il/en/style/su542239/aw4563#aw4563",
    "https://www.next.co.il/en/style/su477540/aj5463#aj5463",
    "https://www.next.co.il/en/style/su744420/b69609#b69609",
    "https://www.next.co.il/en/style/su419416/al5662#al5662",
    "https://www.next.co.il/en/style/su419416/aa6918#aa6918",
    "https://www.next.co.il/en/style/su160823/q81805#q81805",
    "https://www.next.co.il/en/style/su735903/e26252#e26252",
    "https://www.next.co.il/en/style/su160859/q81922#q81922",
    "https://www.next.co.il/en/style/su160859/q82000#q82000",
    "https://www.next.co.il/en/style/su541884/aw4397#aw4397",
    "https://www.next.co.il/en/style/su541884/aw4394#aw4394",
    "https://www.next.co.il/en/style/su744497/e54970#e54970",
    "https://www.next.co.il/en/style/su419416/aa6917#aa6917",
    "https://www.next.co.il/en/style/su419416/aa6918#aa6918",
    "https://www.next.co.il/en/style/su263546/n90208#n90208",
    "https://www.next.co.il/en/style/su263546/n90205#n90205",
    "https://www.next.co.il/en/style/su148543/841503#841503",
    "https://www.next.co.il/en/style/su148543/919905#919905",
    "https://www.next.co.il/en/style/su502331/al5335#al5335",
    "https://www.next.co.il/en/style/su502331/al5333#al5333",
    "https://www.next.co.il/en/style/su304494/b56402#b56402",
    "https://www.next.co.il/en/style/su304494/b35936#b35936",
    "https://www.next.co.il/en/style/su387777/k95283#k95283",
    "https://www.next.co.il/en/style/su387777/n48073#n48073",
    "https://www.next.co.il/en/style/su369450/e45305#e45305",
    "https://www.next.co.il/en/style/su369450/e45315#e45315",
    "https://www.next.co.il/en/style/su555731/ay3220#ay3220",
    "https://www.next.co.il/en/style/su555731/am9558#am9558",
    "https://www.next.co.il/en/style/su705235/at7970#at7970",
    "https://www.next.co.il/en/style/su705235/at7965#at7965",
    "https://www.next.co.il/en/style/su419404/aa6905#aa6905",
    "https://www.next.co.il/en/style/su461965/ad9644#ad9644",
    "https://www.next.co.il/en/style/su534522/av5612#av5612",
    "https://www.next.co.il/en/style/su626484/f34131#f34131",
    "https://www.next.co.il/en/style/su234965/835308#835308",
    "https://www.next.co.il/en/style/su234965/835209#835209",
    "https://www.next.co.il/en/style/su555647/am9557#am9557",
    "https://www.next.co.il/en/style/su304494/b35936#b35936",
    "https://www.next.co.il/en/style/su304494/b56402#b56402",
    "https://www.next.co.il/en/style/su387777/k95251#k95251",
    "https://www.next.co.il/en/style/su387777/n48073#n48073",
    "https://www.next.co.il/en/style/su263898/n94769#n94769",
    "https://www.next.co.il/en/style/su263898/n94771#n94771"
]

    scraped_data = [] # in json for spliting to excel sheets

    def parse(self, response):
        
        is_many_colors = response.css('.pdp-css-nhqfmf')
        
        #check if have many colors
        if is_many_colors:
            api_start = "https://www.next.co.il/en/_next/data/992863/en/style/"
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
        print(5555555555555555555555555555555555555555555555)
        print(product_details)
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
