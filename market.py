import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
import pandas as pd

class MarketSpider(scrapy.Spider):
    name = 'market_spider'
    start_urls = ['https://www.klsescreener.com/v2/screener/quote_results']
    
    # Define the scraping process
    def parse(self, response):
        # Parse the HTML with BeautifulSoup
        market_html = BeautifulSoup(response.body, 'html.parser')
        market_table = market_html.find('tbody')  # Find the table body
        
        if not market_table:
            self.log("No table found on the page.")
            return

        # Define table headers
        headers = ["Name", "Code", "Category", "Price", "Change", "Change%", "52week",
                   "Volume", "EPS", "DPS", "NTA", "PE", "DY", "ROE", "PTBV", "MCap.(M)", "hyperlink"]

        # Prepare data extraction
        rows = []
        for row in market_table.find_all('tr'):  # Iterate over table rows
            cols = row.find_all('td')
            if cols:
                # Extract text and hyperlink for the first column
                first_col = cols[0].find('a')
                if first_col:
                    name_text = first_col.get_text(strip=True)
                    hyperlink = f'https://www.klsescreener.com{first_col["href"]}'
                else:
                    name_text = cols[0].get_text(strip=True)

                # Extract the rest of the columns (excluding the last one)
                other_columns = [col.get_text(strip=True) for col in cols[1:-2]]
                rows.append([name_text] + other_columns + [hyperlink])

        if rows:
            # Create a DataFrame from scraped data
            scraped_data = pd.DataFrame(rows, columns=headers)

            # Save the updated dataset to a CSV file
            scraped_data.to_csv('./market_data.csv', index=False)
            self.log("Data saved to market_data.csv.")

            # Print the scraped data to the console
            self.log("Scraped Data:\n" + scraped_data.to_string(index=False))
        else:
            self.log("No rows extracted from the table.")

# Function to run the spider
def run_spider():
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "DEBUG",  # Adjust log level to DEBUG to see console output
    })
    process.crawl(MarketSpider)
    process.start()

# Run the spider
if __name__ == '__main__':
    run_spider()
