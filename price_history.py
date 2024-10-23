import requests
import csv
import time
import urllib.parse

#"The Concealed Killer Weapons Case" : ['Sand Cannon Rocket Launcher', 'Red Rock Roscoe Pistol', 
#    'Psychedelic Slugger Revolver', 'Purple Range Sniper Rifle' , 'Sudden Flurry Stickybomb Launcher', 
 #   'Night Terror Scattergun', 'Carpet Bomber Stickybomb Launcher', 'Woodland Warrior Rocket Launcher', 
 #   'Wrapped Reviver Medi Gun', 'Night Owl Sniper Rifle', 'Woodsy Widowmaker SMG', 'Backwoods Boomstick Shotgun',
 #   'King of the Jungle Minigun', 'Masked Mender Medi Gun', 'Forest Fire Flame Thrower'],
 #   "The Powerhouse Weapons Case" : ['Liquid Asset Stickybomb Launcher', 'Thunderbolt Sniper Rifle', 
 #   'Current Event Scattergun', 'Pink Elephant Stickybomb Launcher', 'Shell Shocker Rocket Launcher',
 #   'Flash Fryer Flame Thrower', 'Spark of Life Medi Gun', 'Dead Reckoner Revolver', 'Black Dahlia Pistol'
 #   'Sandstone Special Pistol', 'Brick House Minigun', 'Aqua Marine Rocket Launcher', 'Low Profile SMG'
 #   'Turbine Torcher Flame Thrower', 'Lightning Rod Shotgun']

# Will use parent dictionary later to add column/feature to item
family = {
    "Mann Co. Supply Crate Series #71" : ['Strange Bonk! Atomic Punch', "Strange Hitman's Heatmaker", "Strange Battalion's Backup"],
    "Mann Co. Supply Crate Series #75" : ['Strange Crit-a-Cola', 'Strange Solemn Vow', 'Strange Sydney Sleeper'],
    "Mann Co. Supply Crate Series #76" : ['Strange Concheror', 'Strange Revolver', 'Strange Eviction Notice'],
    "Mann Co. Supply Crate Series #77" : ['Strange Rescue Ranger', 'Strange Grenade Launcher', 'Strange Scorch Shot'],
    "Mann Co. Supply Munition Series #90" : ['Strange AWPer Hand', 'Strange Ullapool Caber', 'Strange Winger'],
    "Mann Co. Supply Munition Series #92" : ['Strange Candy Cane', 'Strange Dalokohs Bar', "Strange Warrior's Spirit",
    'Strange Apoco-Fists', 'Strange Red-Tape Recorder', 'Strange Claidheamh Mòr', 'Strange Wrangler', 'Strange Shahanshah', 
    'Strange Cloak and Dagger', 'Strange Buff Banner', 'Strange Kritzkrieg'],
    "Mann Co. Supply Munition Series #103" : ['Strange Sandvich', 'Strange Natascha', 'Strange Powerjack', 'Strange Degreaser', 
    'Strange Reserve Shooter','Strange Ambassador', 'Strange Quickiebomb Launcher', 'Strange Back Scatter', 'Strange Panic Attack', 
    'Strange Iron Bomber'],
}

session = requests.Session()

# https://www.blakeporterneuro.com/learning-python-project-3-scrapping-data-from-steams-community-market/
# ADD your steamLoginSecure cookie's content below once you log in for scraping (you can only access values if you are logged in)
content = "76561198044346545%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MTAyRF8yNTQxQzlGRF83RkEzOCIsICJzdWIiOiAiNzY1NjExOTgwNDQzNDY1NDUiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3Mjk3NDQwNzQsICJuYmYiOiAxNzIxMDE3MzgzLCAiaWF0IjogMTcyOTY1NzM4MywgImp0aSI6ICIxMDFCXzI1NDFDOUZGXzdENTYyIiwgIm9hdCI6IDE3Mjk2NTczODMsICJydF9leHAiOiAxNzQ3NTY2MDIxLCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiNjcuMTg4LjYwLjQ1IiwgImlwX2NvbmZpcm1lciI6ICI2Ny4xODguNjAuNDUiIH0.MLP_ooTBgM4zSgt_trVle_qKxjFJ75Lahw3Zz7688Vce9QZ1szQBzvX5XwXj35Zde5KMIg76dmabI1SnRvUcAA"
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
def write_to_csv(data, item_name, parent, filename="steam_price_history_tf2_71-92.csv"):

    #Overwrite CSV file with new fetched info
    with open(filename, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)

        # Write the price history data
        for entry in data:
            date, price, volume = entry  # date, price, and volume from the JSON response
            writer.writerow([item_name, parent, date, price, volume])
            # item_name, date, price, volumn, parent (case)


if __name__ == "__main__":
    game_id = 440
    filename = "steam_price_history_tf2_71-92.csv"

    # Create the file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # If the file is newly created or empty, write the header
        writer.writerow(["Item Name", "Parent", "Date", "Price", "Volume"])

    for parent, children in family.items():
        price_history = get_price_history(game_id, parent)
        if price_history:
            write_to_csv(price_history, parent, None)
        print(f"Fetched {0 if not price_history else len(price_history)} records for {parent}.")
        time.sleep(3)
        
        #conditions = ['(Battle-Scarred)', '(Well-Worn)', '(Field-Tested)', '(Minimal Wear)', '(Factory New)']

        for child in children:
            price_history = get_price_history(game_id, child)
            if price_history:
                write_to_csv(price_history, child, parent)
            print(f"Fetched {0 if not price_history else len(price_history)} records for {child}.")
            time.sleep(3)


   