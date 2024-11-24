from itertools import product
import requests
import csv
import json
from lxml import html
from time import time
from typing import Optional

start_time = time()

def crawling(time_limit: int, source: str = "camelia.lt", return_format: str = "list") -> Optional[str]:

    #sukuriamas tuscias list
    dataList = []
    try:
        #Pradeda skaiciuoti laika
        if source == "camelia.lt":
            url = "https://camelia.lt/c/prekiu-medis/vitaminai-maisto-papildai-mineralai/groziui-903"
            dataList = fetchingCamelia(url, start_time, time_limit)
        elif source == "lrytas.lt":
            url = "https://www.lrytas.lt"
            tree = parseHTML(url)
            dataList = extractLrytas(tree, start_time, time_limit)
        else:
            raise ValueError("Svetaine nera sarase")

        #Sukuriama funkcija, kuri issaugoja i faila
        saveToFile(source, dataList, return_format)

    except ValueError as e:
        print(f"Error: {e}")
        return None
def parseHTML(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        tree = html.fromstring(response.text)
        return tree
    except requests.exceptions.RequestException as e:
        print(f"Užklausa failed: {e}")
        return None
def fetchingCamelia(base_url, start_time: float, time_limit: int):

    dataList = []
    current_page = 1
    total_products = 0
    while True:
        #Skaiciuojamas laikas
        elapsed_time = time() - start_time
        if elapsed_time > time_limit:
            print(f"{time_limit}")
            break

        url = base_url if current_page == 1 else f"{base_url}?page={current_page}&offset=1#"
        print(f"Puslapiai, is kuriuos traukiama info: {url}\n")

        tree = parseHTML(url)
        if tree is None:
            print(f"Nepavyko gauti duomenų iš šitos svetainės: {current_page}.")
            break

        #tikrinama, kiek produktu yra
        if current_page == 1:
            idx = 1
            num_products_total = tree.xpath(".//div[contains(@data-test, 'products-total')]")
            if num_products_total:
                num = num_products_total[0].xpath(".//text()")
                num = [text.strip().replace('Produktų ', '') for text in num if text.strip()]
                total_products = int(num[0]) if num else 0
                print(f"Iš viso produktų: {total_products}")
            else:
                print("Nėra produktų")
                break
        else:
            idx = current_page * 24
        #Istraukiami produktai is svetaines
        page_data = extractCamelia(tree, idx)
        dataList.extend(page_data)
        #Sustabdoma, kai visi produktai surinkti
        if len(dataList) >= total_products:
            print("Visi produktai yra surintki")
            break
        #Pereinama i kita svetaine, kai is puslapio yra surinkti duomenys
        current_page += 1
    return dataList
def extractCamelia(tree, idx):

    dataList = []
    product_nodes = tree.xpath("//div[contains(@class, 'product-card')]")
    for id, product in enumerate(product_nodes, start=len(dataList)+idx):

        # Istraukiamas pavadinimas
        titles = product.xpath('.//div[contains(@class,\'product-name\')]/text()')
        titles = titles[0].strip() if titles else None

        # Istraukiama paveiksleliu URL
        images_url = product.xpath(".//div/img[contains(@class,'product-image')]/@src")
        images_url = images_url[0].strip() if images_url else None

        # Idedame i list
        dataList.append((id, titles, images_url))
    return dataList
def extractLrytas(tree, start_time: float, time_limit: int):
    dataList = []
    article_nodes = tree.xpath("//div[contains(@class, 'col-span-12 lg:col-span-')]")
    for id, article in enumerate(article_nodes, start = 1):

        elapsed_time = time() - start_time
        if elapsed_time > time_limit:
            print(f"{time_limit}")
            break
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
def saveToFile(source, dataList, return_format):

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
            with open(f'./results/{fileName}.csv', 'w', newline='', encoding='utf-8') as file:
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
            with open(f"./results/{fileName}.json", "w", newline='', ) as jsonFile:
                json.dump(dataList, jsonFile, ensure_ascii=False, indent=4)
            print(f"Json failas sukurtas: {fileName}.json")
        except Exception as e:
            print(f"Json failo klaida: {e}")
    else:
        # Netinkamo formato error
        raise ValueError("Nepalaikomas formatas. Naudokite 'list', 'csv' arba 'json'.")


