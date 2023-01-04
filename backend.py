import urllib.request, json 
import time

import json

import nbt
import io
import base64

bzStuff = {}

bzHyIDs = []
bzVolumes = []
bzBuyOrderPrices = []
bzSellOfferPrices = []

bins = {}
lbins = {}

npcStuff = {}

npcHyIDs = []
npcPrices = []

itemStuff = {}

hyIDs = []
items = []

# GETTERS AND SETTERS
def getLBins():
    bins.clear()
    index = 0
    with urllib.request.urlopen("https://api.hypixel.net/skyblock/auctions?page=0") as url:
        data = json.loads(url.read().decode('utf-8'))
        data = data["auctions"]
        for key in data:
            internalID = str(nbt.nbt.NBTFile(fileobj = io.BytesIO(base64.b64decode(key["item_bytes"]))))
            price = int(key["starting_bid"])
            if "bin" in key and key["bin"] == True:
                bins.update({str(index): {"item": fixAH(key["item_name"]), "cost": price}})
            index += 1
    
    keys_by_item = {}
    value_by_key = {}
    price_compare = {}
    lbins = {}

    lbins.clear()

    # Loop through the bins and add the keys and values to the maps
    for key, value in bins.items():
        item = value.get("item")
        if item not in keys_by_item:
            keys_by_item[item] = []
        keys_by_item[item].append(key)
        value_by_key[key] = value

    # Loop through the map and print the values for each item value
    for item, keys in keys_by_item.items():
        for key in keys:
            value = value_by_key[key]
            for k, v in bins.items():
                if v == value:
                    price_compare.update({k: value})
        sorted = list(price_compare.items())
        sorted.sort(key=lambda x: x[1]['cost'], reverse=False)
        lbins.update({sorted[0][0]: sorted[0][1]})
        price_compare.clear()

def getBZ():
    # This function retrieves data on items available for purchase on the Bazaar in the game Hypixel Skyblock

    # Clear all lists that will store data on Bazaar items
    bzStuff.clear()
    index = 0

    # Retrieve data on Bazaar items from the Hypixel Skyblock API
    with urllib.request.urlopen("https://api.hypixel.net/skyblock/bazaar") as url:
        data = json.loads(url.read().decode('utf-8'))
        data = data["products"]
        
        # For each Bazaar item, get its ID, volume, buy order price, and sell offer price
        for key in data:
            hyid = data[key]["product_id"]
            volume = data[key]["quick_status"]["buyVolume"]
            buyOrderPrice = data[key]["quick_status"]["sellPrice"]
            sellOfferPrice = data[key]["quick_status"]["buyPrice"]

            bzStuff.update({str(index): {"hyid": hyid, "volume": volume, "bop": buyOrderPrice, "sop": sellOfferPrice}})

            index += 1

def getNPC():
    # This function retrieves data on NPC-sellable items in the game Hypixel Skyblock

    # Clear all lists that will store data on NPC-sellable items
    npcStuff.clear()
    index = 0

    # Retrieve data on NPC-sellable items from the Hypixel Skyblock API
    with urllib.request.urlopen("https://api.hypixel.net/resources/skyblock/items") as url:
        data = json.loads(url.read().decode('utf-8'))
        data = data["items"]
        
        # For each NPC-sellable item, get its ID and sell price
        for key in data:
            if "npc_sell_price" in key:
                hyid = key["id"]
                npcprice = key["npc_sell_price"]
                
                npcStuff.update({str(index): {"hyid": hyid, "npcprice": npcprice}})

                index += 1

def getItems():
    # This function retrieves data on all items in the game Hypixel Skyblock

    # Clear the list that will store data on all items
    itemStuff.clear()
    index = 0

    # Retrieve data on all items from the Hypixel Skyblock API
    with urllib.request.urlopen("https://api.hypixel.net/resources/skyblock/items") as url:
        data = json.loads(url.read().decode('utf-8'))
        data = data["items"]
        
        # For each item, get its ID and name
        for key in data:
            hyid = key["id"]
            item = key["name"]

            itemStuff.update({str(index): {"hyid": hyid, "item": item}})

            index += 1

# UTILITY FUNCTIONS

def fixAH(name: str):
    fixed = name.replace("⚚", "HERMES STAFF").replace("✪", "STAR ").replace("◆", "DIAMOND").replace("✿", "FLOWER").replace("✦", "SPARKLE")
    fixed = fixed.replace("➊", "ONE").replace("➋", "TWO").replace("➌", "FIVE").replace("➍", "FOUR").replace("➎", "FIVE")
    return fixed

def calculateAHProfit(lowestBin: int, price: int):
	if (lowestBin - price >= 1000000):
		return (lowestBin - price) - (lowestBin * 0.02);
	else:
		return (lowestBin - price) - (lowestBin * 0.02);

def refreshBZandNPC():
    getItems()
    getBZ()
    getNPC()









refreshBZandNPC()
getLBins()

with open('bz.json', 'w') as f:
    open('bz.json', 'w').close()
    # Write the dictionary to the file in JSON format
    json.dump(bzStuff, f)

with open('npc.json', 'w') as f:
    open('npc.json', 'w').close()
    # Write the dictionary to the file in JSON format
    json.dump(npcStuff, f)

with open('items.json', 'w') as f:
    open('items.json', 'w').close()
    # Write the dictionary to the file in JSON format
    json.dump(itemStuff, f)

with open('ah.json', 'w') as f:
    open('ah.json', 'w').close()
    # Write the dictionary to the file in JSON format
    json.dump(lbins, f)
