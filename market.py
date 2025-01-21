import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
import pandas as pd

class MarketSpider(scrapy.Spider):
    name = 'market_spider'
    start_urls = ['https://www.klsescreener.com/v2/screener/quote_results']
    
    #market klse
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
                    hyperlink = first_col['href']
                    hyperlink = f'https://www.klsescreener.com{hyperlink}'
                else:
                    name_text = cols[0].get_text(strip=True)
       
                # Extract the rest of the columns (excluding the last one)
                code = cols[1].get_text(strip=True)
                category = cols[2].get_text(strip=True)
                price = cols[3].contents[0].get_text(strip=True)
                # print(price)
                change = cols[4].get_text(strip=True)
                change_percent = cols[5].get_text(strip=True)
                week52 = cols[6].get_text(strip=True)
                volume = cols[7].get_text(strip=True)
                eps = cols[8].get_text(strip=True)
                dps = cols[9].get_text(strip=True)
                nta = cols[10].get_text(strip=True)
                pe = cols[11].get_text(strip=True)
                dy = cols[12].get_text(strip=True)
                roe = cols[13].get_text(strip=True)
                ptbv = cols[14].get_text(strip=True)
                mcap = cols[15].get_text(strip=True)
                
                rows.append([
                name_text, code, category, price, change, change_percent, week52,
                volume, eps, dps, nta, pe, dy, roe, ptbv, mcap, hyperlink
            ])
        # Create a DataFrame from scraped data
        scraped_data = pd.DataFrame(rows, columns=headers)

        # Save the updated dataset
        scraped_data.to_csv('market_data.csv', index=False)
        self.log(" data saved to market_data.csv.")


# Function to run the spider and print the output
def run_spider():
    process = CrawlerProcess(settings={
      "LOG_LEVEL": "ERROR",  # Suppress unnecessary logs for clarity
     })
    process.crawl(MarketSpider)

    process.start()


 
    # print(news_within_24_hours)

# Run the spider
if __name__ == '__main__':
    run_spider()
    
    
