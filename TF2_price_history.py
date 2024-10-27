import requests
import csv
import time
import urllib.parse

# Will use parent dictionary later to add column/feature to item
# https://www.csgodatabase.com/cases/
family = {

          }

session = requests.Session()

# https://www.blakeporterneuro.com/learning-python-project-3-scrapping-data-from-steams-community-market/
# ADD your steamLoginSecure cookie's content below once you log in for scraping (you can only access values if you are logged in)
steamLoginSecure = ""
cookie = {'steamLoginSecure': steamLoginSecure};

# Function to encode item name for URL
# def encode_item_name(item_name):
#     return urllib.parse.quote(item_name)

# Function to fetch price history
# https://github.com/Revadike/InternalSteamWebAPI/wiki/Get-Market-Price-History
def get_price_history(game_id, item_name):
    # Encode item name for URL to handle special characters
    # encoded_item_name = encode_item_name(item_name)

    # Construct URL for price history based on game_id and item_name
    url = f"https://steamcommunity.com/market/pricehistory/?appid={game_id}&market_hash_name={item_name}"
    print(f"Fetching price history from: {url}")

    response = session.get(url, cookies=cookie)
    # Check status code
    print("Status Code:", response.status_code)

    # Typical response codes: 200 (OK), 500 (No Content), 429 (Rate Limited)

    if response.status_code == 429 or response.status_code == 502:
        time.sleep(10)
        return get_price_history(game_id, item_name)

    data = response.json()

    if 'prices' in data: # 200 OK
        return data['prices']
    else: # 500 NO CONTENT
        return []

# Function to write price history to a CSV file
def write_to_csv(data, item_name, parent, filename):

    # Overwrite CSV file with new fetched info
    with open(filename, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)

        # Write the price history data
        for entry in data:
            date, price, volume = entry  # date, price, and volume from the JSON response
            writer.writerow([item_name, parent, date, price, volume])
            # item_name, date, price, volumn, parent (case)

if __name__ == "__main__":
    game_id = 440
    output = "steam_440_price_history.csv"

    # Create the file
    with open(output, mode='w', newline='') as file:
        writer = csv.writer(file)

        # If the file is newly created or empty, write the header
        writer.writerow(["Item Name", "Parent", "Date", "Price", "Volume"])


    for parent, children in family.items():
        # parent
        price_history = get_price_history(game_id, parent)
        if price_history:
            write_to_csv(price_history, parent, None, output)
        print(f"Fetched {0 if not price_history else len(price_history)} records for {parent}.")
        time.sleep(3)

        qualities = ['Strange', 'Unusual', 'Specialized', 'Professional'] # 'Vintage', 'Genuine', 'Haunted', "Collector's"]
        
        # conditions = ['(Battle-Scarred)', '(Well-Worn)', '(Field-Tested)', '(Minimal Wear)', '(Factory New)']

        # children
        for child in children:
            # Case for no quality or condition
            price_history = get_price_history(game_id, child)
            if price_history:
                write_to_csv(price_history, child, parent, output)
            print(f"Fetched {0 if not price_history else len(price_history)} records for {child}.")
            time.sleep(3)

            # for condition in conditions:
            #     # mandatory condition
            #     price_history = get_price_history(game_id, child + f' {condition}')
            #     if price_history:
            #         write_to_csv(price_history, child + ' ' + condition, parent, output)
            #     print(f"Fetched {0 if not price_history else len(price_history)} records for {child + ' ' + condition}.")
            #     time.sleep(3)

            # Prepend Quality
            for quality in qualities:
                price_history = get_price_history(game_id, quality + ' ' + child)
                if price_history:
                    write_to_csv(price_history, f'{quality} ' + child, parent, output) # Not including the ™ symbol because it is unidentifiable
                print(f"Fetched {0 if not price_history else len(price_history)} records for {quality + ' ' + child}.")
                time.sleep(3)

    # for game_id, item_name in game_items:
    #     price_history = get_price_history(game_id, item_name)
    #     # print(price_history)
    #     if price_history:
    #         write_to_csv(price_history, item_name)
    #     print(f"Fetched {0 if not price_history else len(price_history)} records for {item_name}.")
    #     time.sleep(3)  # Pause between requests to avoid being blocked
        # We have 20 requests per minute, so sleeping for 3 seconds
        # lets us achieve the max # of requests