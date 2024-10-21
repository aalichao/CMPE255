import requests
import csv
import time
import urllib.parse

# Will use parent dictionary later to add column/feature to item
# https://www.csgodatabase.com/cases/
family = {
        'CS:GO Weapon Case': ['MP7 | Skulls', 'SG 553 | Ultraviolet', 'AUG | Wings', 'M4A1-S | Dark Water', 'USP-S | Dark Water', 'Glock-18 | Dragon Tattoo', 'AK-47 | Case Hardened', 'Desert Eagle | Hypnotic', 'AWP | Lightning Strike'],
          'eSports 2013 Case': ['M4A4 | Faded Zebra', 'MAG-7 | Memento', 'FAMAS | Doomkitty', 'Galil AR | Orange DDPAT', 'Sawed-Off | Orange DDPAT', 'P250 | Splash', 'AK-47 | Red Laminate', 'AWP | BOOM', 'P90 | Death by Kitty'],
          'Operation Bravo Case': ['Nova | Tempest', 'Dual Berettas | Black Limba', 'UMP-45 | Bone Pile', 'SG 553 | Wave Spray', 'Galil AR | Shattered', 'G3SG1 | Demeter', 'M4A1-S | Bright Water',
                                   'M4A4 | Zirka', 'MAC-10 | Graven', 'USP-S | Overgrowth', 'P90 | Emerald Dragon', 'P2000 | Ocean Foam', 'AWP | Graphite', 'Desert Eagle | Golden Koi', 'AK-47 | Fire Serpent'],
          'CS:GO Weapon Case 2': ['Tec-9 | Blue Titanium', 'M4A1-S | Blood Tiger', 'FAMAS | Hexane', 'P250 | Hive', 'SCAR-20 | Crimson Web', 'Five-SeveN | Case Hardened', 'MP9 | Hypnotic', 'Nova | Graphite',
                                  'Dual Berettas | Hemoglobin', 'P90 | Cold Blooded', 'USP-S | Serum', 'SSG 08 | Blood in the Water'],
          'eSports 2013 Winter Case': ['Galil AR | Blue Titanium', 'Five-SeveN | Nightshade', 'PP-Bizon | Water Sigil', 'Nova | Ghost Camo', 'G3SG1 | Azure Zebra', 'P250 | Steel Disruption', 'AK-47 | Blue Laminate', 'P90 | Blind Spot', 'FAMAS | Afterimage', 'AWP | Electric Hive', 'Desert Eagle | Cobalt Disruption', 'M4A4 | X-Ray'],
          'Winter Offensive Case': ['PP-Bizon | Cobalt Halftone', 'M249 | Magma', 'Five-SeveN | Kami', 'Galil AR | Sandstorm', 'Nova | Rising Skull', 'MP9 | Rose Iron', 'Dual Berettas | Marina', 'FAMAS | Pulse', 'M4A1-S | Guardian', 'P250 | Mehndi', 'AWP | Redline', 'Sawed-Off | The Kraken', 'M4A4 | Asiimov'],
          'CS:GO Weapon Case 3': ['Glock-18 | Blue Fissure', 'USP-S | Stainless', 'Dual Berettas | Panther', 'P2000 | Red FragCam', 'CZ75-Auto | Crimson Web', 'Five-SeveN | Copper Galaxy', 'Desert Eagle | Heirloom', 'Tec-9 | Titanium Bit', 'CZ75-Auto | Tread Plate', 'P250 | Undertow', 'CZ75-Auto | The Fuschia Is Now', 'CZ75-Auto | Victoria'],
          'Operation Phoenix Case': ['MAG-7 | Heaven Guard', 'Tec-9 | Sandstorm', 'Negev | Terrain', 'UMP-45 | Corporal', 'FAMAS | Sergeant', 'USP-S | Guardian', 'SG 553 | Pulse', 'MAC-10 | Heat', 'Nova | Antique', 'P90 | Trigon', 'AK-47 | Redline', 'AUG | Chameleon', 'AWP | Asiimov'],
          'Huntsman Weapon Case': ['P90 | Desert Warfare', 'P90 | Module', 'SSG 08 | Slashed', 'Galil AR | Kami', 'P2000 | Pulse', 'Dual Berettas | Retribution', 'CZ75-Auto | Twist', 'CZ75-Auto | Poison Dart', 'Tec-9 | Isaac', 'PP-Bizon | Antique', 'MAC-10 | Curse', 'MAC-10 | Tatter', 'XM1014 | Heaven Guard', 'AUG | Torque', 'SCAR-20 | Cyrex', 'USP-S | Caiman', 'USP-S | Orion', 'M4A1-S | Atomic Alloy', 'M4A4 | Desert-Strike', 'AK-47 | Vulcan', 'M4A4 | Howl'],
          'Operation Breakout Weapon Case': ['MP7 | Urban Hazard', 'SSG 08 | Abyss', 'P2000 | Ivory', 'UMP-45 | Labyrinth', 'Negev | Desert-Strike', 'PP-Bizon | Osiris', 'CZ75-Auto | Tigris', 'Nova | Koi', 'P250 | Supernova', 'Desert Eagle | Conspiracy', 'Glock-18 | Water Elemental', 'Five-SeveN | Fowl Play', 'P90 | Asiimov', 'M4A1-S | Cyrex'],
          'eSports 2014 Summer Case': ['MAC-10 | Ultraviolet', 'SSG 08 | Dark Water', 'CZ75-Auto | Hexane', 'XM1014 | Red Python', 'Negev | Bratatat', 'USP-S | Blood Tiger', 'P90 | Virus', 'PP-Bizon | Blue Streak', 'MP7 | Ocean Foam', 'Desert Eagle | Crimson Web', 'Glock-18 | Steel Disruption', 'P2000 | Corticera', 'AUG | Bengal Tiger', 'Nova | Bloomstick', 'AWP | Corticera', 'M4A4 | Bullet Rain', 'AK-47 | Jaguar'],
          'Operation Vanguard Case': ['MP9 | Dart', 'G3SG1 | Murky', 'Five-SeveN | Urban Hazard', 'UMP-45 | Delusion', 'MAG-7 | Firestarter', 'M4A4 | Griffin', 'Glock-18 | Grinder', 'Sawed-Off | Highwayman', 'M4A1-S | Basilisk', 'XM1014 | Tranquility', 'SCAR-20 | Cardiac', 'P250 | Cartel', 'AK-47 | Wasteland Rebel', 'P2000 | Fire Elemental'],
          'Chroma Case': ['MP9 | Deadly Poison', 'Glock-18 | Catacombs', 'XM1014 | Quicksilver', 'M249 | System Lock', 'SCAR-20 | Grotto', 'MAC-10 | Malachite', 'Dual Berettas | Urban Shock', 'Desert Eagle | Naga', 'Sawed-Off | Serenity', 'M4A4 | 龍王 (Dragon King)', 'AK-47 | Cartel', 'P250 | Muertos', 'Galil AR | Chatterbox', "AWP | Man-o'-war"],
          'Chroma 2 Case': ['MP7 | Armor Core', 'AK-47 | Elite Build', 'Desert Eagle | Bronze Deco', "Negev | Man-o'-war", 'Sawed-Off | Origami', 'P250 | Valence', 'CZ75-Auto | Pole Position', 'UMP-45 | Grand Prix', 'MAG-7 | Heat', 'AWP | Worm God', 'Galil AR | Eco', 'FAMAS | Djinn', 'Five-SeveN | Monkey Business', 'MAC-10 | Neon Rider', 'M4A1-S | Hyper Beast'],
          'Falchion Case': ['P90 | Elite Build', 'Galil AR | Rocket Pop', 'Glock-18 | Bunsen Burner', 'UMP-45 | Riot', 'Nova | Ranger', 'USP-S | Torque', 'MP9 | Ruby Poison Dart', 'M4A4 | Evil Daimyo', 'FAMAS | Neural Net', 'P2000 | Handgun', 'Negev | Loudmouth', 'MP7 | Nemesis', 'SG 553 | Cyrex', 'CZ75-Auto | Yellow Jacket', 'AK-47 | Aquamarine Revenge', 'AWP | Hyper Beast'],
          'Shadow Case': ['MAC-10 | Rangeen', 'FAMAS | Survivor Z', 'Dual Berettas | Dualing Dragons', 'Glock-18 | Wraiths', 'XM1014 | Scumbria', 'MAG-7 | Cobalt Core', 'SCAR-20 | Green Marine', 'MP7 | Special Delivery', 'Galil AR | Stone Cold', 'M249 | Nebula Crusader', 'P250 | Wingshot', 'SSG 08 | Big Iron', 'G3SG1 | Flux', 'AK-47 | Frontside Misty', 'USP-S | Kill Confirmed', 'M4A1-S | Golden Coil'],
          'Revolver Case': ['P2000 | Imperial', 'Desert Eagle | Corinthian', 'AUG | Ricochet', 'Sawed-Off | Yorick', 'SCAR-20 | Outbreak', 'R8 Revolver | Crimson Web', 'PP-Bizon | Fuel Rod', 'SG 553 | Tiger Moth', 'Tec-9 | Avalanche', 'Five-SeveN | Retrobution', 'XM1014 | Teclu Burner', 'Negev | Power Loader', 'P90 | Shapewood', 'G3SG1 | The Executioner', 'AK-47 | Point Disarray', 'M4A4 | Royal Paladin', 'R8 Revolver | Fade'],
          'Operation Wildfire Case': ['PP-Bizon | Photic Zone', 'MAC-10 | Lapis Gator', 'SSG 08 | Necropos', 'Dual Berettas | Cartel', 'Tec-9 | Jambiya', 'USP-S | Lead Conduit', 'MP7 | Impire', 'FAMAS | Valence', 'Glock-18 | Royal Legion', 'Five-SeveN | Triumvirate', 'MAG-7 | Praetorian', 'Desert Eagle | Kumicho Dragon', 'Nova | Hyper Beast', 'AWP | Elite Build', 'M4A4 | The Battlestar', 'AK-47 | Fuel Injector'],
          'Chroma 3 Case': ['MP9 | Bioleak', 'SG 553 | Atlas', 'G3SG1 | Orange Crash', 'P2000 | Oceanic', 'Dual Berettas | Ventilators', 'M249 | Spectre', 'Sawed-Off | Fubar', 'SSG 08 | Ghost Crusader', 'Galil AR | Firefight', 'CZ75-Auto | Red Astor', 'Tec-9 | Re-Entry', 'XM1014 | Black Tie', 'AUG | Fleet Flock', 'UMP-45 | Primal Saber', 'P250 | Asiimov', 'PP-Bizon | Judgement of Anubis', "M4A1-S | Chantico's Fire"],
          'Gamma Case': ['SG 553 | Aerial', 'Tec-9 | Ice Cap', 'PP-Bizon | Harvester', 'MAC-10 | Carnivore', 'Five-SeveN | Violent Daimyo', 'Nova | Exo', 'P250 | Iron Clad', 'P90 | Chopper', 'AUG | Aristocrat', 'Sawed-Off | Limelight', 'AWP | Phobos', 'R8 Revolver | Reboot', 'P2000 | Imperial Dragon', 'M4A4 | Desolate Space', 'SCAR-20 | Bloodsport', 'Glock-18 | Wasteland Rebel', 'M4A1-S | Mecha Industries'],
          'Gamma 2 Case': ['CZ75-Auto | Imprint', 'Five-SeveN | Scumbria', 'G3SG1 | Ventilator', 'Negev | Dazzle', 'P90 | Grim', 'UMP-45 | Briefing', 'XM1014 | Slipstream', 'Desert Eagle | Directive', 'Glock-18 | Weasel', 'MAG-7 | Petroglyph', 'SCAR-20 | Powercore', 'SG 553 | Triarch', 'AUG | Syd Mead', 'MP9 | Airlock', 'Tec-9 | Fuel Injector', 'FAMAS | Roll Cage', 'AK-47 | Neon Revolution'],
          'Glove Case': ['P2000 | Turf', 'MAG-7 | Sonar', 'MP9 | Sand Scale', 'Galil AR | Black Sand', 'MP7 | Cirrus', 'Glock-18 | Ironwork', 'CZ75-Auto | Polymer', 'USP-S | Cyrex', 'Nova | Gila', 'M4A1-S | Flashback', 'G3SG1 | Stinger', 'Dual Berettas | Royal Consorts', 'Sawed-Off | Wasteland Princess', 'P90 | Shallow Grave', 'FAMAS | Mecha Industries', 'M4A4 | Buzz Kill', 'SSG 08 | Dragonfire'],
          'Spectrum Case': ['MP7 | Akoben', 'Sawed-Off | Zander', 'SCAR-20 | Blueprint', 'PP-Bizon | Jungle Slipstream', 'P250 | Ripple', 'Five-SeveN | Capillary', 'Desert Eagle | Oxide Blaze', 'MAC-10 | Last Dive', 'UMP-45 | Scaffold', 'XM1014 | Seasons', 'Galil AR | Crimson Tsunami', 'M249 | Emerald Poison Dart', 'AWP | Fever Dream', 'CZ75-Auto | Xiangliu', 'M4A1-S | Decimator', 'AK-47 | Bloodsport', 'USP-S | Neo-Noir'],
          'Operation Hydra Case': ['UMP-45 | Metal Flowers', 'Tec-9 | Cut Out', 'MAG-7 | Hard Water', 'MAC-10 | Aloha', 'M4A1-S | Briefing', 'FAMAS | Macabre', 'USP-S | Blueprint', 'P2000 | Woodsman', 'P250 | Red Rock', 'P90 | Death Grip', "SSG 08 | Death's Head", 'AK-47 | Orbit Mk01', 'Dual Berettas | Cobra Strike', 'Galil AR | Sugar Rush', 'M4A4 | Hellfire', 'AWP | Oni Taiji', 'Five-SeveN | Hyper Beast'],
          'Spectrum 2 Case': ['SCAR-20 | Jungle Slipstream', 'Tec-9 | Cracked Opal', 'MAC-10 | Oceanic', 'Glock-18 | Off World', 'G3SG1 | Hunter', 'AUG | Triqua', 'Sawed-Off | Morris', 'XM1014 | Ziggy', 'UMP-45 | Exposure', 'CZ75-Auto | Tacticat', 'SG 553 | Phantom', 'MP9 | Goo', 'R8 Revolver | Llama Cannon', 'PP-Bizon | High Roller', 'M4A1-S | Leaded Glass', 'P250 | See Ya Later', 'AK-47 | The Empress'],
          'Clutch Case': ['XM1014 | Oxide Blaze', 'SG 553 | Aloha', 'R8 Revolver | Grip', 'PP-Bizon | Night Riot', 'P2000 | Urban Hazard', 'MP9 | Black Sand', 'Five-SeveN | Flame Test', 'UMP-45 | Arctic Wolf', 'Nova | Wild Six', 'Negev | Lionfish', 'MAG-7 | SWAG-7', 'Glock-18 | Moonrise', 'USP-S | Cortex', 'AUG | Stymphalian', 'AWP | Mortis', 'MP7 | Bloodsport', 'M4A4 | Neo-Noir'],
          'Horizon Case': ['Tec-9 | Snek-9', 'R8 Revolver | Survivalist', 'P90 | Traction', 'MP9 | Capillary', 'Glock-18 | Warhawk', 'Dual Berettas | Shred', 'AUG | Amber Slipstream', 'MP7 | Powercore', 'AWP | PAW', 'Nova | Toy Soldier', 'G3SG1 | High Seas', 'CZ75-Auto | Eco', 'Sawed-Off | Devourer', 'FAMAS | Eye of Athena', 'M4A1-S | Nightmare', 'AK-47 | Neon Rider', 'Desert Eagle | Code Red'],
          'Danger Zone Case': ['MP9 | Modest Threat', 'Glock-18 | Oxide Blaze', 'Nova | Wood Fired', 'M4A4 | Magnesium', 'Sawed-Off | Black Sand', 'SG 553 | Danger Close', 'Tec-9 | Fubar', 'G3SG1 | Scavenger', 'Galil AR | Signal', 'MAC-10 | Pipe Down', 'P250 | Nevermore', 'USP-S | Flashback', 'UMP-45 | Momentum', 'Desert Eagle | Mecha Industries', 'MP5-SD | Phosphor', 'AK-47 | Asiimov', 'AWP | Neo-Noir'],
          'Prisma Case': ['FAMAS | Crypsis', 'AK-47 | Uncharted', 'MAC-10 | Whitefish', 'Galil AR | Akoben', 'MP7 | Mischief', 'P250 | Verdigris', 'P90 | Off World', 'AWP | Atheris', 'Tec-9 | Bamboozle', 'Desert Eagle | Light Rail', 'MP5-SD | Gauss', 'UMP-45 | Moonrise', 'R8 Revolver | Skull Crusher', 'AUG | Momentum', 'XM1014 | Incinegator', 'Five-SeveN | Angry Mob', 'M4A4 | The Emperor'],
          'Shattered Web Case': ['SCAR-20 | Torn', 'R8 Revolver | Memento', 'Nova | Plume', 'MP5-SD | Acid Wash', 'M249 | Warbird', 'G3SG1 | Black Sand', 'Dual Berettas | Balance', 'P2000 | Obsidian', 'PP-Bizon | Embargo', 'MP7 | Neon Ply', 'AUG | Arctic Wolf', 'AK-47 | Rat Rod', 'Tec-9 | Decimator', 'SSG 08 | Bloodshot', 'SG-553 | Colony IV', 'MAC-10 | Stalker', 'AWP | Containment Breach'],
          'CS20 Case': ['Dual Berettas | Elite 1.6', 'Tec-9 | Flash Out', 'MAC-10 | Classic Crate', 'MAG-7 | Popdog', 'SCAR-20 | Assault', 'FAMAS | Decommissioned', 'Glock-18 | Sacrifice', 'M249 | Aztec', 'MP5-SD | Agent', 'Five-SeveN | Buddy', 'P250 | Inferno', 'UMP-45 | Plastique', 'MP9 | Hydra', 'P90 | Nostalgia', 'AUG | Death by Puppy', 'FAMAS | Commemoration', 'AWP | Wildfire'],
          'Prisma 2 Case': ['AUG | Tom Cat', 'AWP | Capillary', 'CZ75-Auto | Distressed', 'Desert Eagle | Blue Ply', 'MP5-SD | Desert Strike', 'Negev | Prototype', 'R8 Revolver | Bone Forged', 'P2000 | Acid Etched', 'Sawed-Off | Apocalypto', 'SCAR-20 | Enforcer', 'SG 553 | Darkwing', 'SSG 08 | Fever Dream', 'AK-47 | Phantom Disruptor', 'MAC-10 | Disco Tech', 'MAG-7 | Justice', 'M4A1-S | Player Two', 'Glock-18 | Bullet Queen'],
          'Fracture Case': ['Negev | Ultralight', 'P2000 | Gnarled', "SG 553 | Ol' Rusty", 'SSG 08 | Mainframe 001', 'P250 | Cassette', 'P90 | Freight', 'PP-Bizon | Runic', 'MAG-7 | Monster Call', 'Tec-9 | Brother', 'MAC-10 | Allure', 'Galil AR | Connexion', 'MP5-SD | Kitbash', 'M4A4 | Tooth Fairy', 'Glock-18 | Vogue', 'XM1014 | Entombed', 'Desert Eagle | Printstream', 'AK-47 | Legion of Anubis'],
          'Operation Broken Fang Case': ['CZ75-Auto | Vendetta', 'P90 | Cocoa Rampage', 'G3SG1 | Digital Mesh', 'Galil AR | Vandal', 'P250 | Contaminant', 'M249 | Deep Relief', 'MP5-SD | Condition Zero', 'Nova | Clear Polymer', 'AWP | Exoskeleton', 'Dual Berettas | Dezastre', 'SSG 08 | Parallax', 'UMP-45 | Gold Bismuth', 'Five-SeveN | Fairy Tale', 'USP-S | Monster Mashup', 'M4A4 | Cyber Security', 'Glock-18 | Neo-Noir', 'M4A1-S | Printstream'],
          'Snakebite Case': ['SG 553 | Heavy Metal', 'Glock-18 | Clear Polymer', 'M249 | O.S.I.P.R.', 'CZ75-Auto | Circaetus', 'UMP-45 | Oscillator', 'R8 Revolver | Junk Yard', 'Nova | Windblown', 'P250 | Cyber Shell', 'Negev | dev_texture', 'MAC-10 | Button Masher', 'Desert Eagle | Trigger Discipline', 'AK-47 | Slate', 'MP9 | Food Chain', 'XM1014 | XOXO', 'Galil AR | Chromatic Aberration', 'USP-S | The Traitor', 'M4A4 | In Living Color'],
          'Operation Riptide Case': ['AUG | Plague', 'Dual Berettas | Tread', 'G3SG1 | Keeping Tabs', 'MP7 | Guerrilla', 'PP-Bizon | Lumen', 'USP-S | Black Lotus', 'XM1014 | Watchdog', 'MAG-7 | BI83 Spectrum', 'FAMAS | ZX Spectron', 'Five-SeveN | Boost Protocol', 'MP9 | Mount Fuji', 'M4A4 | Spider Lily', 'MAC-10 | Toybox', 'Glock-18 | Snack Attack', 'SSG 08 | Turbo Peek', 'AK-47 | Leet Museo', 'Desert Eagle | Ocean Drive'],
          'Dreams & Nightmares Case': ['Sawed-Off | Spirit Board', 'SCAR-20 | Poultrygeist', 'P2000 | Lifted Spirits', 'MP5-SD | Necro Jr.', 'MAG-7 | Foresight', 'MAC-10 | Ensnared', 'Five-SeveN | Scrawl', 'USP-S | Ticket to Hell', 'XM1014 | Zombie Offensive', 'M4A1-S | Night Terror', 'G3SG1 | Dream Glade', 'PP-Bizon | Space Cat', 'MP7 | Abyssal Apparition', 'FAMAS | Rapid Eye Movement', 'Dual Berettas | Melondrama', 'MP9 | Starlight Protector', 'AK-47 | Nightwish'],
          'Recoil Case': ['Glock-18 | Winterized', 'UMP-45 | Roadblock', 'Negev | Drop Me', 'MAC-10 | Monkeyflage', 'M4A4 | Poly Mag', 'Galil AR | Destroyer', 'FAMAS | Meow 36', 'M249 | Downtown', 'R8 Revolver | Crazy 8', 'Dual Berettas | Flora Carnivora', 'P90 | Vent Rush', 'SG 553 | Dragon Tech', 'Sawed-Off | Kiss♥Love', 'P250 | Visions', 'AK-47 | Ice Coaled', 'USP-S | Printstream', 'AWP | Chromatic Aberration'],
          'Revolution Case': ['Tec-9 | Rebel', 'SG 553 | Cyberforce', 'MP5-SD | Liquidation', 'P250 | Re.built', 'SCAR-20 | Fragments', 'MP9 | Featherweight', 'MAG-7 | Insomnia', 'Glock-18 | Umbral Rabbit', 'MAC-10 | Sakkaku', 'M4A1-S | Emphorosaur-S', 'R8 Revolver | Banana Cannon', 'P90 | Neoqueen', 'AWP | Duality', 'UMP-45 | Wild Child', 'P2000 | Wicked Sick', 'M4A4 | Temukau', 'AK-47 | Head Shot'],
          'Kilowatt Case': ['Dual Berettas | Hideout', 'MAC-10 | Light Box', 'Nova | Dark Sigil', 'SSG 08 | Dezastre', 'Tec-9 | Slag', 'UMP-45 | Motorized', 'XM1014 | Irezumi', 'Glock-18 | Block-18', 'M4A4 | Etch Lord', 'Five-SeveN | Hybrid', 'MP7 | Just Smile', 'Sawed-Off | Analog Input', 'M4A1-S | Black Lotus', 'Zeus x27 | Olympus', 'USP-S | Jawbreaker', 'AWP | Chrome Cannon', 'AK-47 | Inheritance'],
          'Gallery Case': ['AUG | Luxe Trim', 'Desert Eagle | Calligraffiti', 'M249 | Hypnosis', 'MP5-SD | Statics', 'R8 Revolver | Tango', 'SCAR-20 | Trail Blazer', 'USP-S | 027', 'Dual Berettas | Hydro Strike', 'M4A4 | Turbine', 'MAC-10 | Saibā Oni', 'P90 | Randy Rush', 'SSG 08 | Rapid Transit', 'AK-47 | The Outsiders', 'P250 | Epicenter', 'UMP-45 | Neo-Noir', 'Glock-18 | Gold Toof', 'M4A1-S | Vaporwave']
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
    data = response.json()

    if 'prices' in data:
        return data['prices']
    else:
        return []

# Function to write price history to a CSV file
def write_to_csv(data, item_name, parent, filename=f"steam_730_price_history.csv"):

    # Overwrite CSV file with new fetched info
    with open(filename, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)

        # Write the price history data
        for entry in data:
            date, price, volume = entry  # date, price, and volume from the JSON response
            writer.writerow([item_name, parent, date, price, volume])
            # item_name, date, price, volumn, parent (case)

if __name__ == "__main__":
    game_id = 730
    filename = "steam_730_price_history.csv"

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
        
        conditions = ['(Battle-Scarred)', '(Well-Worn)', '(Field-Tested)', '(Minimal Wear)', '(Factory New)']

        for child in children:
            for condition in conditions:
                price_history = get_price_history(game_id, child + ' ' + condition)
                if price_history:
                    write_to_csv(price_history, child + ' ' + condition, parent)
                print(f"Fetched {0 if not price_history else len(price_history)} records for {child + ' ' + condition}.")
                time.sleep(3)

                # Prepend Stattrak
                price_history = get_price_history(game_id, 'StatTrak™ ' + child + ' ' + condition)
                if price_history:
                    write_to_csv(price_history, 'StatTrak ' + child + ' ' + condition, parent) # Not including the ™ symbol because it is unidentifiable
                print(f"Fetched {0 if not price_history else len(price_history)} records for {'StatTrak™ ' + child + ' ' + condition}.")
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