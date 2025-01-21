import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
import pandas as pd

class MarketSpider(scrapy.Spider):
    name = 'market_spider'
    start_urls = ['https://www.klsescreener.com/v2/screener/quote_results']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def parse(self, response):
        market_html = BeautifulSoup(response.body, 'html.parser')
        market_table = market_html.find('tbody')
        
        if not market_table:
            self.log("No table found!")
            return

        headers = ["Name", "Code", "Category", "Price", "Change", "Change%", "52week",
                   "Volume", "EPS", "DPS", "NTA", "PE", "DY", "ROE", "PTBV", "MCap.(M)", "hyperlink"]
        rows = []

        for row in market_table.find_all('tr'):
            cols = row.find_all('td')
            if cols:
                first_col = cols[0].find('a')
                if first_col:
                    name_text = first_col.get_text(strip=True)
                    hyperlink = f"https://www.klsescreener.com{first_col['href']}"
                else:
                    name_text = cols[0].get_text(strip=True)

                other_columns = [col.get_text(strip=True) for col in cols[1:-2]]
                rows.append([name_text] + other_columns + [hyperlink])

        if rows:
            scraped_data = pd.DataFrame(rows, columns=headers)
            scraped_data.to_csv('./market_data.csv', index=False)
            self.log("Data saved to market_data.csv.")
        else:
            self.log("No rows extracted from the table.")

def run_spider():
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "DEBUG"
    })
    process.crawl(MarketSpider)
    process.start()

if __name__ == '__main__':
    run_spider()
