from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from utils import *
import logging
import time

def getCoins():
    # Set up headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Setup WebDriver, installing ChromeDrivef if not available
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        logging.info("Visiting website...")
        driver.set_page_load_timeout(30)  
        driver.get("https://www.pump.fun/advanced")
        logging.info("Website visit successful.")

        # Wait for the page to load
        time.sleep(5)  # Adjust wait time based on the loading time of the page

        # Find anchor tags with the specified classes
        elements = driver.find_elements(By.CSS_SELECTOR, 'a.flex.items-center.bg-gray-800.rounded-lg')

        if not elements:
            logging.warning("No elements found. The page may not have loaded correctly.")

        coins = {}
        for element in elements:
            try:
                name, link, marketcap, volume, age = extract_data_from_element(element)
                coins[link] = {
                    'name': name,
                    'marketcap': marketcap,
                    'volume': volume,
                    'age': age,
                    'volume-marketcap-ratio': round(volume / marketcap, 2) if marketcap > 0 else 0,
                    'volume-age-ratio': round(volume / age, 2) if age > 0 else 0,
                    'marketcap-age-ratio': round(marketcap / age, 2) if age > 0 else 0
                }
            except Exception as e:
                logging.error(f"Error processing element: {e}")
        
        # Sort by volume-marketcap ratio
        sorted_coins = sorted(coins.items(), key=lambda x: x[1]['volume-marketcap-ratio'], reverse=True)

        return sorted_coins

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return []

    finally:
        # Ensure the browser is closed
        logging.info("Closing the browser.")
        driver.quit()