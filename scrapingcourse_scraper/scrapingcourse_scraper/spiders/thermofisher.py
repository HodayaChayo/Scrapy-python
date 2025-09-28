import scrapy


class ThermoSpider(scrapy.Spider):
    name = "thermo"
    base_url = "https://www.thermofisher.com/search/browse/category/us/en/80013650"
    table_data = {
    "Boiling Point": None,
    "CAS": None,
    "Chemical Name or Material": None,
    "Color": None,
    "Molecular Formula": None,
    "Packaging": None,
    "Synonym": None,
    "Grade": None,
    "Molecular Weight (g/mol)": None,
    "Percent Purity": None,
    "Quantity": None,
    "Unit Size": None,
    "IUPAC Name": None,
    "InChI Key": None,
    "SMILES": None,
    "Appearance (Color)": None,
    "Appearance (Form)": None,
    "Infrared spectrum": None,
    "Melting point": None,
    "Titration with NaOH": None,
    "Form": None,
    "Assay (Aqueous acid-base Titration)": None,
    "Identification (FTIR)": None,
    "Refractive Index": None,
    "Assay from Supplier's CofA": None,
    "Comment": None,
    "Melting Point": None,
    "Assay (Silylated GC)": None,
    "Residue after ignition": None,
    "Chloride (Cl)": None,
    "HPLC": None,
    "Heavy metals (as Pb)": None,
    "Impurity content": None,
    "Trace Metal": None,
    "Melting Point (clear melt)": None,
    "Optical Rotation": None,
    "Assay (GC)": None,
    "Free base (titration)": None,
    "Carboniz. sub. by hot H2SO4": None,
    "Beilstein": None,
    "ChEBI": None,
    "Water Content (Karl Fischer Titration)": None,
    "Titration Argentometric": None,
    "Loss on drying": None,
    "Water": None,
    "UV": None,
    "Color scale": None,
    "Heavy metals (ICP-OES)": None,
    "Titration with KMnO4": None,
    "Substance darkened by H2SO4": None,
    "Total Metal Impurities": None,
    "Chloride content": None,
    "Iron (Fe)": None,
    "Titration with CHA": None,
    "Specific optical rotation": None,
    "Arsenic (As)": None,
    "Sulfate (SO4)": None,
    "Refractive index": None,
    "Residue after evaporation": None,
    "K2Cr2O7-reducing substance": None,
    "Cadmium (Cd)": None,
    "Identification A": None,
    "Identification B": None,
    "Residue on ignition": None,
    "Assay (unspecified)": None,
    "Dnase,Rnase,Protease activity": None,
    "Oxalate (C2O4)": None,
    "Acid value": None,
    "Density": None,
    "GC": None,
    "Phosphate (PO4)": None,
    "Sodium (Na)": None,
    "Sugars, dextrin": None,
    "Zinc (Zn)": None,
    "Sulfuric acid": None,
    "Titration with HClO4": None,
    "Acidity/alkalinity": None,
    "Name Note": None,
    "Physical Form": None,
    "Recommended Storage": None,
    "KMnO4-reducing substance": None,
    "Optical Absorbance at": None,
    "Insoluble matter": None,
    "Acid-base back titration": None,
    "Dilution test": None,
    "Sulfite (SO3)": None,
    "Enantiomeric excess": None,
    "Titration excess NaOH": None,
    "Reducing sugars": None,
    "Assay": None,
    "Titration with HCl": None,
    "Aluminium (Al)": None,
    "Heavy Metals (as Pb)": None,
    "Sulfated ash": None,
    "Assay (Titration)": None,
    "Concentration": None,
    "EINECS Number": None,
    "Potassium (K)": None,
    "Calcium (Ca)": None,
    "Magnesium (Mg)": None,
    "Assay from Suppliers CofA": None,
    "Clarity of solution": None,
    "Strength": None,
    "Ash": None,
    "pH": None,
    "Sugars": None,
    "Acids": None,
    "Impurity": None,
    "Moisture holding capacity": None,
    "Trace Metals": None,
    "Sulfur compounds (as SO4)": None,
    "DOT Information": None,
    "Assay (Non-aqueous acid-base Titration)": None,
    "Assay (Argentometric Titration)": None,
    "Clarity": None,
    "Residual water": None,
    "Ammonium (NH4)": None,
    "Proton NMR": None,
    "Loss on Drying": None,
    "Assay (HPLC)": None,
    "Transition Temperature": None,
    "Elemental Analysis": None,
    "Fumaric and maleic acid": None,
    "Identification": None,
    "Fluoride (F)": None,
    "lambda-max (UV-Vis)": None,
    "Insoluble material": None,
}

    custom_settings = {
        # Playwright setup (כמו שהיה)
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",

        # Rotate User-Agent (scrapy-user-agents)
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
            "scrapy_user_agents.middlewares.RandomUserAgentMiddleware": 400,
        },

        # קצת האטה כדי לא להצטייר כרובוט
        "DOWNLOAD_DELAY": 0.5,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
        "CONCURRENT_REQUESTS": 5,

        # אופציונלי: להציג יותר לוגים של retries
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 2,
    }

    def start_requests(self):
        first_page_url = f"{self.base_url}?resultPage=1&resultsPerPage=60"
        yield scrapy.Request(
            first_page_url,
            callback=self.parse_first_page,
            meta={"playwright": True, "playwright_include_page": True},
        )

    async def parse_first_page(self, response):
        page = response.meta["playwright_page"]

        # wait for both products and pagination controls
        await page.wait_for_selector(".search-card")
        await page.wait_for_selector(".c-pagination__page")

        # get total number of pages
        pages = response.css(".c-pagination__page::text").getall()
        total_pages = int(pages[-1]) if pages else 1
        self.logger.info(f"Found {total_pages} pages in total")

        # collect links from the first page
        async for item in self.extract_links(response):
            yield item

        # now loop over the rest of the pages
        for page_num in range(2, total_pages + 1):
            next_page_url = f"{self.base_url}?resultPage={page_num}&resultsPerPage=60"
            yield scrapy.Request(
                next_page_url,
                callback=self.parse_links,
                meta={"playwright": True},
            )

        await page.close()

    async def parse_links(self, response):
        async for item in self.extract_links(response):
            yield item

    async def extract_links(self, response):
        if response.meta.get("playwright_page"):
            page = response.meta["playwright_page"]
            await page.wait_for_selector(".search-card:nth-child(60)")

        links = response.css(".search-card .search-img-section a::attr(href)").getall()
        for link in links:
            yield scrapy.Request(
                response.urljoin(link),
                callback=self.parse_product,
                meta={"playwright": True, "playwright_include_page": True},
            )

        if response.meta.get("playwright_page"):
            await page.close()
            
    async def parse_product(self, response):
        
        # Reset values in table_data for this product
        for key in self.table_data.keys():
            self.table_data[key] = None
            
        page = response.meta.get("playwright_page")
        if page:
            # wait for product content to load
            await page.wait_for_selector(".pdp-title h1")
            # title = response.css("h1.product-title::text").get(default="").strip()
            
            buttons = await page.query_selector_all(".pdp-specifications__view-more")

            # לסגור את הבאנר של קונסנט אם קיים
            consent_btn = await page.query_selector("#truste-consent-button")
            if consent_btn:
                await consent_btn.click()
                await page.wait_for_timeout(500)
                
            # אם יש כפתורים – לוחצים על כולם
            if buttons:
                for button in buttons:
                    await button.click()
                    await page.wait_for_timeout(500) 
                    
            # מילון לאיסוף כל שורות הטבלה
            rows = response.css(".pdp-specification-row")
            for row in rows:
                key = row.css(".pdp-specification-row__name::text").get()
                value = row.css(".pdp-specification-row__value::text").get()
                if key:
                    if key not in self.table_data:
                        self.table_data[key] = None  # Add new key if not already present
                    self.table_data[key] = value.strip() if value else None
                    
            url = response.url
            await page.close()  # close the page after extracting data
        else:
            # fallback if somehow Playwright is missing
            # title = response.css("h1.product-title::text").get(default="").strip()
            url = response.url
            
        title = response.css(".pdp-title h1::text").get()
        product_desc = response.css("#product-description::text").get()
        image = response.css(".pdp-images-panel>img ::attr(src)").get()
        

        product_details = {
            "url": url,
            "title": title,
            "product_desc": product_desc,
            "image": response.urljoin(image) if image else None,
        }
        
        product_details.update(self.table_data)

        yield product_details


    def closed(self, reason):
        # Called when the spider finishes scraping
        # self.export_to_excel()
        print(self.table_data)