import requests
import csv
import json
from lxml import html
from time import time
from typing import Optional


def crawling(time_limit: int = 60, source: str = "camelia.lt", return_format: str = "list") -> Optional[str]:

    #sukuriamas tuscias list
    dataList = []
    try:
        if source == "camelia.lt":
            url = "https://camelia.lt/c/prekiu-medis/vitaminai-maisto-papildai-mineralai/groziui-903"
            #dataList = extractCamelia(tree)
        elif source == "lrytas.lt":
            url = "https://www.lrytas.lt"
            #dataList = extractLrytas(tree)

        #Pradeda skaiciuoti laika
        start_time = time()
        #Requests
        response = requests.get(url, timeout=time_limit)

        # Raise HTTPError
        response.raise_for_status()

        # Parse HTML
        tree = html.fromstring(response.text)

        # Apskaiciuota, per kiek laiko rado paveikslelius ir teksta
        elapsed_time = time() - start_time
        print(elapsed_time)

        if source == "camelia.lt":
            dataList = extractCamelia(tree)
        elif source == "lrytas.lt":
            dataList = extractLrytas(tree)

        #Sukuriama funkcija, kuri issaugoja i faila
        save_to_file(source, dataList, return_format)

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def extractCamelia(tree):

    dataList = []
    product_nodes = tree.xpath("//div[contains(@class, 'product-card')]")
    for product in enumerate(product_nodes, start = 1):
        # Istraukiamas pavadinimas
        text = product.xpath(".//div[contains(@class,'product-name')]/text()")[0].strip()
        #Patikrinama, ar pavadinimas ne tuscias

        # Istraukiama paveiksleliu URL
        image_url = product.xpath(".//div/img[contains(@class,'product-image')]/@src")[0].strip("['']")
        #Patikrinama, ar img_url ne tuscias

        # Idedame i list
        dataList.append((text,image_url))
    return dataList
def extractLrytas(tree):

    dataList = []
    article_nodes = tree.xpath("//div[contains(@class, 'col-span-12 lg:col-span-')]")
    for id, article in enumerate(article_nodes, start = 1):
        #Istraukiamas pavadinimas
        title = article.xpath(".//h2[contains(@class,'text-base')]/a/text()")
        if title:
            title[0].strip()
        else:
            None

        image_url = article.xpath(".//img/@src")
        #Patikrinama, ar img_url ne tuscias
        if image_url:
           image_url[0].strip()
        else:
            None

        category = article.xpath(".//div[contains(@class,'flex items-center')]/a/span[contains(@class, 'text-xs')]/text()")
        if category:
           category[0].strip()
        else:
            None

        #idedame i list
        dataList.append((id, title, image_url, category))
    return dataList
def save_to_file(source, dataList, return_format):

    if source == "camelia.lt":
        fileName = "vaistaiList"
    elif source == "lrytas.lt":
        fileName = "straipsniaiList"
    else:
        print("error")

    if return_format == "list":
        for i in dataList:
            print(i)

    # Jeigu formatas "csv", issaugoja faila i csv
    elif return_format == "csv":
        try:
            with open(f'{fileName}.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if fileName == "vaistaiList":
                    writer.writerow(['Pavadinimas', 'Nuotraukos URL'])
                elif fileName == "straipsniaiList":
                    writer.writerow(['Pavadinimas', 'Nuotraukos URL', "Kategorijos"])
                for element in dataList:
                    writer.writerow(element)
            print(f"CSV failas sukurtas: {fileName}.csv")
        except Exception as e:
            print(f"CSV failo klaida: {e}")
            return None

    # Jeigu formatas "json", issaugoja faila i json
    elif return_format == "json":
        try:
            with open(f"{fileName}.json", "w", newline='', ) as jsonFile:
                json.dump(dataList, jsonFile, ensure_ascii=False, indent=4)
            print(f"Json failas sukurtas: {fileName}.json")
        except Exception as e:
            print(f"Json failo klaida: {e}")
    else:
        # Netinkamo formato error
        raise ValueError("Nepalaikomas formatas. Naudokite 'list', 'csv' arba 'json'.")


