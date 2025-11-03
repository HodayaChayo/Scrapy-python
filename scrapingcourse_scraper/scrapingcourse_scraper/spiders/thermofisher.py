import scrapy
import pandas as pd
from pathlib import Path
import asyncio

class ThermoBreadcrumbsSpider(scrapy.Spider):
    name = "thermo_breadcrumbs"

    custom_settings = {
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": False,  # רואים את הדפדפן
            "slow_mo": 100,     # איטיות בין הפעולות למניעת חסימה
        },
        "DOWNLOAD_DELAY": 5,  # השהייה של 10 שניות בין בקשות
        "CONCURRENT_REQUESTS": 1,  # בקשה אחת בכל רגע
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 10000,  # עד 60 שניות לטעינת דף
    }

    def start_requests(self):
        # מיקום האקסל
        self.excel_path = Path("thermofisher.xlsx")

        # קריאת הקובץ
        self.df = pd.read_excel(self.excel_path)

        # יצירת בקשות לכל URL
        for index, row in self.df.iterrows():
            url = row["Product URL"]
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "row_index": index,
                    "playwright_include_page": True,
                },
                callback=self.parse_page
            )

    async def parse_page(self, response):
        page = response.meta["playwright_page"]

        # נחכה להופעת הפירורים (במקום reload)
        try:
            await page.wait_for_selector(".pdp-breadcrumbs", timeout=10000)
        except Exception:
            self.logger.warning(f"No breadcrumbs found for {response.url}")
            await page.close()
            return

        # await asyncio.sleep(5) 

        # --- הדפסת HTML של ה-container ---
        html = await page.inner_html(".pdp-breadcrumbs")
        print(f"HTML of breadcrumbs for row {response.meta['row_index']}:\n", html)

        # --- חילוץ Breadcrumbs מ-Shadow DOM ---
        breadcrumbs = await page.evaluate("""
        () => {
            const items = [];
            const nodes = document.querySelectorAll('.pdp-breadcrumbs core-breadcrumb');
            if (!nodes.length) return items;
            nodes.forEach(node => {
                const bitems = node.querySelectorAll('core-breadcrumb-item');
                bitems.forEach(bnode => {
                    if(bnode.shadowRoot) {
                        const links = bnode.shadowRoot.querySelectorAll('.core-breadcrumb-item__link');
                        links.forEach(link => {
                            if(link.textContent) items.push(link.textContent.trim());
                        });
                    }
                });
            });
            return items;
        }
        """)

        print("Breadcrumbs found:", breadcrumbs)
        await page.close()

        # ניקוי והוספה לאקסל
        breadcrumbs = [b for b in breadcrumbs if b]
        index = response.meta["row_index"]
        for i, crumb in enumerate(breadcrumbs):
            col_name = f"breadcrumb_{i+1}"
            if col_name not in self.df.columns:
                self.df[col_name] = None
            self.df.at[index, col_name] = crumb

        # שמירה הדרגתית כל כמה שורות
        if index % 5 == 0:
            self.df.to_excel(self.excel_path, index=False)

    def closed(self, reason):
        # שמירה סופית
        self.df.to_excel(self.excel_path, index=False)
