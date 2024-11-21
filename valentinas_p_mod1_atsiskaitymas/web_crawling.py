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
        else:
            raise ValueError("Svetaine nera sarase")

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
    for id, product in enumerate(product_nodes, start = 1):
        # Istraukiamas pavadinimas
        titles = product.xpath('.//div[contains(@class,\'product-name\')]/text()')
        titles = titles[0].strip() if titles else None

        # Istraukiama paveiksleliu URL
        images_url = product.xpath(".//div/img[contains(@class,'product-image')]/@src")
        images_url = images_url[0].strip() if images_url else None

        # Idedame i list
        dataList.append((id, titles,images_url))
    return dataList
def extractLrytas(tree):

    dataList = []
    article_nodes = tree.xpath("//div[contains(@class, 'col-span-12 lg:col-span-')]")
    for id, article in enumerate(article_nodes, start = 1):
        #Istraukiamas pavadinimas
        titles = article.xpath(".//h2[contains(@class,'text-base')]/a/text()")
        titles = titles[0].strip() if titles else None

        images_url = article.xpath(".//img/@src")
        images_url = images_url[0].strip() if images_url else None


        categories = article.xpath(".//div[contains(@class,'flex items-center')]/a/span[contains(@class, 'text-xs')]/text()")
        categories = categories[0].strip() if categories else None

        #idedame i list
        if titles and images_url and categories:
            dataList.append((id, titles, images_url, categories))
    return dataList
def save_to_file(source, dataList, return_format):

    if source == "camelia.lt":
        fileName = "vaistaiList"
    elif source == "lrytas.lt":
        fileName = "straipsniaiList"

    if return_format == "list":
        for i in dataList:
            print(i)

    # Jeigu formatas "csv", issaugoja faila i csv
    elif return_format == "csv":
        try:
            with open(f'{fileName}.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if fileName == "vaistaiList":
                    writer.writerow(['id','Pavadinimas', 'Nuotraukos URL'])
                elif fileName == "straipsniaiList":
                    writer.writerow(['id','Pavadinimas', 'Nuotraukos URL', "Kategorijos"])
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


