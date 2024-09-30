import requests
import csv
import time
import urllib.parse

# Will use parent dictionary later to add column/feature to item
parent = {'Dreams & Nightmares Case': []}

# List of (game_id, item_name) tuples
game_items = [
    (730, "Dreams & Nightmares Case"),  # CS:GO Glove Case Key
    # (570, "Treasure Key"),  # Dota 2 Treasure Key
    # (440, "Mann Co. Supply Crate Key"),  # TF2 Key
    # Add more items as needed
]

session = requests.Session()

# https://www.blakeporterneuro.com/learning-python-project-3-scrapping-data-from-steams-community-market/
# ADD your steamLoginSecure cookie's content below once you log in for scraping (you can only access values if you are logged in)
content = ""
cookie = {'steamLoginSecure': content};

# Function to encode item name for URL
def encode_item_name(item_name):
    return urllib.parse.quote(item_name)

# Function to fetch price history
# https://github.com/Revadike/InternalSteamWebAPI/wiki/Get-Market-Price-History
def get_price_history(game_id, item_name):
    # Encode item name for URL to handle special characters
    encoded_item_name = encode_item_name(item_name)

    # Construct URL for price history based on game_id and item_name
    url = f"https://steamcommunity.com/market/pricehistory/?appid={game_id}&market_hash_name={encoded_item_name}"
    print(f"Fetching price history from: {url}")

    response = session.get(url, cookies=cookie)
    data = response.json()

    if 'prices' in data:
        return data['prices']
    else:
        return []

# Function to write price history to a CSV file
def write_to_csv(data, item_name, filename="steam_price_history.csv"):

    # Overwrite CSV file with new fetched info
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # If the file is newly created or empty, write the header
        writer.writerow(["Item Name", "Date", "Price", "Volume"])

        # Write the price history data
        for entry in data:
            date, price, volume = entry  # date, price, and volume from the JSON response
            writer.writerow([item_name, date, price, volume])
            # item_name, date, price, volumn, parent (case)

if __name__ == "__main__":
    for game_id, item_name in game_items:
        price_history = get_price_history(game_id, item_name)
        print(price_history)
        if price_history:
            write_to_csv(price_history, item_name)
        print(f"Fetched {len(price_history)} records for {item_name}.")
        time.sleep(3)  # Pause between requests to avoid being blocked
        # We have 20 requests per minute, so sleeping for 3 seconds
        # lets us achieve the max # of requests