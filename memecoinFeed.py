from memecoinScraper import getCoins
from telegram_alerts import *
import asyncio
import os
import logging
import google.cloud.logging

investment = 0.1

# Function to simulate fetching updated data (replace with your actual coin data fetching logic)
def get_updated_data():
    # get data change over time
    coins = getCoins()
    return coins

# WebSocket server handler
async def handler():
    while True:
        # Fetch updated coin data
        os.system('cls' if os.name == 'nt' else 'clear')
        updated_coins = get_updated_data()
        # print(f"Investment: {investment}")
        tg_text = "Buy:\n\n"
        foundCoinsNumber = 0
        # Print the dictionary
        for i, coin_link in enumerate(updated_coins): # check later
            number = i + 1
            name = coin_link[1]['name']
            marketcap = coin_link[1]['marketcap']
            volume = coin_link[1]['volume']
            age = coin_link[1]['age']
            ret = round((coin_link[1]['volume-marketcap-ratio'] - 1) * 0.75, 2)
            hype = coin_link[1]['volume-age-ratio']
            marketcap_age_ratio = coin_link[1]['marketcap-age-ratio']
            link = coin_link[0]
            tp_value = round((1 + ret) * investment, 2)

            # print info 
            # print(f"#{number}")
            # print(f"Name: {name}")
            # print(f"Marketcap: {marketcap}")
            # print(f"Volume: {volume}")
            # print(f"Age: {age}")
            # print(f"Potential Return: {ret}x")
            # print(f"Hype: {hype}")
            # print(f"Marketcap-age-ratio: {marketcap_age_ratio}")
            # print(f"Link: {link}")
            # print(f"Close at: {tp_value} sol")
            # print("-" * 40)

            if age <= 7200 and marketcap >= 60000 and ret >= 0 and 50<= hype <= 200 and 50 <= marketcap_age_ratio <= 200:
                tg_text += f"#{number}. {name}- potential:{ret}x invest: {investment} sol, tp_value: {tp_value} sol, expected profit: {round(tp_value - investment, 2)} sol\n{link}\nMC{marketcap}\n\n"
                foundCoinsNumber += 1
        
        if tg_text != "Buy:\n\n":
            logging.info(f"Found { foundCoinsNumber}")
            sendMessage(tg_text)
        else:
            logging.info(" No suitable coins found")

        # Wait for 30 second before sending the next update
        await asyncio.sleep(5)

# Run the server
if __name__ == "__main__":
    # logger = logging.getLogger('selenium')
    # logger.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.INFO)
    if int(os.environ.get("PRODUCTION", 0)) == 1:
        logging_client = google.cloud.logging.Client()
        logging_client.setup_logging()
    logging.info(" Started coin scanner")
    asyncio.run(handler())