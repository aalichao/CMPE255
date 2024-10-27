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
    "Mann Co. Supply Crate Series #32": ["Strange Brass Beast", "Strange Ubersaw", "Strange L'Etranger", "Strange Equalizer"],
    "Mann Co. Supply Crate Series #33": ["Strange Soda Popper", "Strange Family Business", "Strange Amputator", "Strange Your Eternal Reward"],
    "Mann Co. Supply Crate Series #34" : ["Strange Reserve Shooter", "Strange Atomizer", "Strange Southern Hospitality", "Strange Scottish Resistance"],
    "Naughty Winter Crate Series #35" : ["Strange Festive Scattergun", "Strange Festive BatFestive Bat", "Strange Festive Rocket Launcher", "Strange Festive Flame Thrower", "Strange Festive Stickybomb Launcher", "Strange Festive Minigun", "Strange Festive Wrench", "Strange Festive Medi Gun", "Strange Festive Sniper Rifle", "Strange Festive Knife"],
    "Nice Winter Crate Series #36" : ["Strange Wrap Assassin", "Strange Holiday Punch", "Strange Spy-cicle"],
    "Mann Co. Supply Crate Series #37" : ["Strange Bazaar Bargain", "Strange Big Earner", "Strange Blutsauger", "Strange Liberty Launcher"],
    "Mann Co. Supply Crate Series #38" : ["Strange Dead Ringer", "Strange SMG", "Strange Quick-Fix", "Strange Killing Gloves of Boxing"],
    "Mann Co. Supply Crate Series #39" : ["Strange Loch-n-Load", "Strange Overdose", "Strange Knife"],
    "Salvaged Mann Co. Supply Crate Series #40" : ["Strange Holiday Punch", "Strange Huntsman", "Strange Widowmaker"],
    "Mann Co. Supply Crate Series #41" : ["Strange Bat", "Strange Direct Hit", "Strange Diamondback"],
    "Mann Co. Supply Crate Series #42" : ["Strange Bottle", "Strange Back Scratcher", "Strange Pistol"],
    "Mann Co. Supply Crate Series #43" : ["Strange Tribalman's Shiv", "Strange Detonator", "Strange Shortstop"],
    "Mann Co. Supply Crate Series #44" : ["Strange Rocket Launcher", "Strange Market Gardener", "Strange Equalizer"],
    "Mann Co. Supply Crate Series #45" : ["Strange Stickybomb Launcher", "Strange Scotsman's Skullcutter", "Strange Persian Persuader"],
    "Scorched Crate Series #46" : ["Strange Lollichop", "Strange Rainblower"],
    "Mann Co. Supply Crate Series #47" : ["Strange Force-A-Nature", "Strange Flame Thrower", "Strange Tomislav"],
    "Mann Co. Supply Crate Series #49" : ["Strange Homewrecker", "Strange Shovel", "Strange Scattergun"],
    "Naughty Winter Crate 2012 Series #52" : ["Strange Festive Holy Mackerel", "Strange Festive Axtinguisher", "Strange Festive Buff Banner", "Strange Festive Sandvich", "Strange Festive Ubersaw", "Strange Festive Frontier Justice", "Strange Festive Huntsman", "Strange Festive Grenade Launcher"],
    "Mann Co. Supply Crate Series #54" : ["Strange Wrap Assassin", "Strange Spy-cicle", "Strange Sniper Rifle"],
    "Mann Co. Supply Crate Series #55" : ["Strange Baby Face's Blaster", "Strange Pain Train", "Strange Medi Gun"],
    "Mann Co. Supply Crate Series #56" : ["Strange Fire Axe", "Strange Flying Guillotine", "Strange Beggar's Bazooka"],
    "Mann Co. Supply Crate Series #57" : ["Strange Fists of Steel", "Strange Neon Annihilator", "Strange Jarate"],
    "Mann Co. Supply Crate Series #59" : ["Strange Kukri", "Strange Huo-Long Heater", "Strange Enforcer"],
    "Select Reserve Mann Co. Supply Crate Series #60" : ["Strange Disciplinary Action", "Strange Loose Cannon", "Strange Fan O'War"],
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
content = "76561198044346545%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MTAyN18yNTQxQ0EyQV84QTNERSIsICJzdWIiOiAiNzY1NjExOTgwNDQzNDY1NDUiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3MzAwNjA3MDQsICJuYmYiOiAxNzIxMzMzODMxLCAiaWF0IjogMTcyOTk3MzgzMSwgImp0aSI6ICIxMDFCXzI1NDFDQTI5XzVFQjlEIiwgIm9hdCI6IDE3Mjk5NzM4MzEsICJydF9leHAiOiAxNzQ4NTU3NzI3LCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiNjcuMTg4LjYwLjQ1IiwgImlwX2NvbmZpcm1lciI6ICI2Ny4xODguNjAuNDUiIH0.YMAPYXtPHcoc31ZVQwNSPVXtK0RzoNU79E33PEI1YzIfOnXkt2fACi2dMapOEOF4BHVpv90TnIa5An1GL4WWCQ"
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
def write_to_csv(data, item_name, parent, filename="steam_price_history_tf2_32-103.csv"):

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


   