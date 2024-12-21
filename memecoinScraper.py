#Stage 1: Get candidate tokens from pump fun
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from utils import *
import logging
import time

def getCoins():
    # Set up headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Setup WebDriver (make sure you have the ChromeDriver installed)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open the page
    logging.info("Visiting website")
    driver.get("https://www.pump.fun/advanced")
    logging.info("Website visit successful")

    # Wait for the page to load
    time.sleep(3)  # Adjust wait time based on the loading time of the page

    # Find anchor tags with the specified classes
    elements = driver.find_elements(By.CSS_SELECTOR, 'a.flex.items-center.bg-gray-800.rounded-lg')

    coins = dict()
    for element in elements:
        name, link, marketcap, volume, age = extract_data_from_element(element)
        coins[link] = {
            'name': name,
            'marketcap': marketcap,
            'volume': volume,
            'age': age,
            'volume-marketcap-ratio': round(volume / marketcap, 2),
            'volume-age-ratio': round(volume / age, 2),
            'marketcap-age-ratio': round(marketcap / age, 2)
        }

    # sort by volume marketcap
    sorted_coins = sorted(coins.items(), key=lambda x: x[1]['volume-marketcap-ratio'], reverse=True)

    # Close the browser
    driver.quit()
    return sorted_coins