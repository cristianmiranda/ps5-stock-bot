#!/usr/bin/python3

import requests
import lxml.html
import json
import time
import sys

from datetime import datetime


def parseMusimundo(raw):
    stream = json.loads(raw)
    hits = stream['hits']['hits']

    items = []
    for hit in hits:
        items.append(hit["_source"]["Descripcion"])

    return items


def parseJumbo(raw):
    stream = json.loads(raw)

    items = []
    for element in stream:
        items.append(element["productTitle"])

    return items


GARBAGE = ['marvels', 'sackboy', 'souls', 'morales', 'dualsense', 'juego', 'ps4', 'cámara', 'camara', 'camera', 'control', 'joystick', 'dualshock', 'parlante', 'celular', 'funda', 'lavarropas', 'cocina', 'plancha', 'auriculares', 'auricular', 'headset', 'kombat', 'android', 'nes', 'retro', 'pc', 'mixer', 'xbox', 'microsoft', 'nintendo', 'audio', 'fighter', 'nba', 'vr', 'meses', 'posavasos', 'lámpara', 'remote', 'hd', 'kanji', 'stickers', 'duty', 'alien', 'lente', 'noga', 'torre', 'reflex', 'barra', 'compacta', 'minicomponente', 'atari', 'bateria', 'batería', 'ce7', 'radio', 'multimedia', 'reloj', 'cargador', 'nioh', 'pack', 'ratchet', 'returnal']

KEYWORDS = ['playstation', 'ps5', 'consola', 'console', 'sony']

STORES = [
    #
    # Garbarino
    #
    [False, 'https://www.garbarino.com/q/playstation/srch?q=playstation', '//*[contains(@id, "item-description")]/text()'],
    [False, 'https://www.garbarino.com/q/ps5/srch?q=ps5', '//*[contains(@id, "item-description")]/text()'],

    #
    # Sony
    #
    [False, 'https://store.sony.com.ar/playstation%205', './/a[@class="title ellipsis"]/text()'],
    [False, 'https://store.sony.com.ar/ps5', './/a[@class="title ellipsis"]/text()'],

    #
    # Musimundo
    #
    # [True, 'https://u.braindw.com/els/musimundoapi?ft=playstation&qt=100&sc=carsa&refreshmetadata=true&exclusive=0&aggregations=true', parseMusimundo],
    # [True, 'https://u.braindw.com/els/musimundoapi?ft=ps5&qt=100&sc=carsa&refreshmetadata=true&exclusive=0&aggregations=true', parseMusimundo],
    
    #
    # Jumbo
    #
    [True, 'https://www.jumbo.com.ar/api/catalog_system/pub/products/search/?=,&ft=playstation', parseJumbo],
    [True, 'https://www.jumbo.com.ar/api/catalog_system/pub/products/search/?=,&ft=ps5', parseJumbo],
    
    #
    # Fravega
    #
    [False, 'https://www.fravega.com/l/?keyword=playstation', '//*[contains(@class, "PieceTitle")]/text()'],
    [False, 'https://www.fravega.com/l/?keyword=ps5', '//*[contains(@class, "PieceTitle")]/text()'],

    #
    # Compumundo
    #
    [False, 'https://www.compumundo.com.ar/q/playstation/srch?q=playstation', '//*[contains(@id, "item-description")]/text()'],
    [False, 'https://www.compumundo.com.ar/q/ps5/srch?q=ps5', '//*[contains(@id, "item-description")]/text()'],
    
    #
    # Walmart
    #
    [False, 'https://www.walmart.com.ar/buscar?text=playstation', '//*[contains(@class, "prateleira__name")]/text()'],
    [False, 'https://www.walmart.com.ar/buscar?text=ps5', '//*[contains(@class, "prateleira__name")]/text()'],

    #
    # Naldo
    #
    [False, 'https://www.naldo.com.ar/search/?text=playstation', '//*[contains(@class, "product__list--name")]/text()'],
    [False, 'https://www.naldo.com.ar/search/?text=ps5', '//*[contains(@class, "product__list--name")]/text()'],
    
    #
    # Carrefour
    #
    [False, 'https://www.carrefour.com.ar/catalogsearch/result/?q=playstation', '//*[contains(@class, "producto-info")]/a/p[@class="title"]/text()'],
    [False, 'https://www.carrefour.com.ar/catalogsearch/result/?q=ps5', '//*[contains(@class, "producto-info")]/a/p[@class="title"]/text()'],
    
    #
    # Coppel
    #
    # [False, 'https://www.coppel.com.ar/search/?q=playstation', '//*[contains(@class, "item-name")]/text()'],
    # [False, 'https://www.coppel.com.ar/search/?q=ps5', '//*[contains(@class, "item-name")]/text()'],
    
    #
    # Falabella
    #
    # [False, 'https://www.falabella.com.ar/falabella-ar/category/cat10166/Mundo-gamer?facetSelected=true&f.product.brandName=sony&isPLP=1', '//*[contains(@class, "pod-subTitle")]/text()'],
    
    #
    # CD Market
    #
    [False, 'https://www.cdmarket.com.ar/Item/Result?getfilterdata=true&page=1&id=0&recsperpage=32&order=CustomDate&sort=False&itemtype=Product&view=&term=playstation&filters=&hasStock=true', '//*/div[contains(@class, "box_data") and not(contains(@class, "box_data nonavailable"))]/h3/text()'],
    [False, 'https://www.cdmarket.com.ar/Item/Result?getfilterdata=true&page=1&id=0&recsperpage=32&order=CustomDate&sort=False&itemtype=Product&view=&term=ps5&filters=&hasStock=true', '//*/div[contains(@class, "box_data") and not(contains(@class, "box_data nonavailable"))]/h3/text()'],

    #
    # Necxus
    #
    # [False, 'https://www.necxus.com.ar/buscar/ps5/', '*//titulo-producto-grilla/text()'],
    
    #
    # Cetrogar
    #
    [False, 'https://www.cetrogar.com.ar/catalogsearch/result/?q=ps5', '*//a[@class="product-item-link"]/text()'],
]


def main():
    bot_token = sys.argv[1]
    recipients = json.loads(sys.argv[2])
    start_time = time.time()

    results = []
    for store in STORES:
        results = scrap(store)
        results["items"] = cleanup(results["items"])
        print (results["items"])

        if results["items"]:
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%d-%m-%Y %H:%M:%S")
            message = "🎮 Encontré un vendedor con stock!\n\n📆 " + timestampStr + "\n🔗 " + results["store"] + "\n\n▶ " + ','.join(results["items"])
            print(message)
            telegram_bot_sendtext(message, bot_token, recipients)
    
    elapsed_time = time.time() - start_time
    elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%m-%Y %H:%M:%S")

    print("\n\n ---------------------")
    print("\nDate: " + timestampStr)
    print("\nElapsed time: " + elapsed)
    print("\n ---------------------\n\n")


def scrap(store):
    isJson = store[0]
    url = store[1]
    items = []

    print("Scraping " + url + "...")

    if isJson:
        callback = store[2]
        json = requests.get(url).content
        items = callback(json)
    else:
        xpath = store[2]
        html = requests.get(url)
        doc = lxml.html.fromstring(html.content)
        items = doc.xpath(xpath)

    return { "store": url, "items": items }


def cleanup(items):
    ps5Related = []
    for item in items:
        if not any(ext in item.lower() for ext in GARBAGE) and any(ext in item.lower() for ext in KEYWORDS):
            ps5Related.append(item)
    
    return ps5Related


def telegram_bot_sendtext(bot_message, bot_token, recipients):
    for bot_chatID in recipients:
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        print(response.json())


if __name__ == '__main__':
    main()
