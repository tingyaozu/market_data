from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

def fetch_market_data():
    # Set up Selenium WebDriver (ensure you have the driver installed)
    driver = webdriver.Chrome()
    driver.get('https://www.klsescreener.com/v2/screener/quote_results')

    # Wait for JavaScript to load content
    time.sleep(5)

    # Parse the loaded HTML
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    driver.quit()

    # Find the table
    market_table = soup.find('tbody')
    if not market_table:
        print("No table found.")
        return

    headers = ["Name", "Code", "Category", "Price", "Change", "Change%", "52week",
               "Volume", "EPS", "DPS", "NTA", "PE", "DY", "ROE", "PTBV", "MCap.(M)", "hyperlink"]
    rows = []

    # Extract rows
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

    # Save to CSV
    if rows:
        scraped_data = pd.DataFrame(rows, columns=headers)
        scraped_data.to_csv('./market_data.csv', index=False)
        print("Data saved to market_data.csv.")
    else:
        print("No rows extracted.")

if __name__ == '__main__':
    fetch_market_data()
