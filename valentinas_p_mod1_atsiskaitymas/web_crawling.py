import requests
import csv
import json
from lxml import html
from time import time
from typing import Optional


def crawling(time_limit: int = 60, source: str = "https://camelia.lt/c/prekiu-medis/vitaminai-maisto-papildai-mineralai/groziui-903", return_format: str = "list") -> Optional[str]:

    vaistaiList = []
    straipsniaiList = []


    try:
        if source == "camelia.lt":
            url = "https://camelia.lt/c/prekiu-medis/vitaminai-maisto-papildai-mineralai/groziui-903"
        elif source == "lrytas.lt":
            url = "https://www.lrytas.lt"

        #Pradeda skaiciuoti laika
        start_time = time()
        response = requests.get(url, timeout=time_limit)

        #Raise HTTPError
        response.raise_for_status()

        # Parse HTML
        tree = html.fromstring(response.text)

        # Apskaiciuota, per kiek laiko rado paveikslelius ir teksta
        elapsed_time = time() - start_time
        print(elapsed_time)

        if source == "camelia.lt":
            product_nodes = tree.xpath("//div[contains(@class, 'product-card')]")
            for product in product_nodes:
                # Istraukiamas pavadinimas
                text = product.xpath(".//div[contains(@class,'product-name')]/text()")[0].strip()
                #Patikrinama, ar pavadinimas ne tuscias
                if text:
                    text[0].strip()

                # Istraukiama paveiksleliu URL
                image_url = product.xpath(".//div/img[contains(@class,'product-image')]/@src")
                #Patikrinama, ar img_url ne tuscias
                if image_url:
                    image_url[0].strip()


                # Idedame i list
                vaistaiList.append((text,image_url))
        #
        if source == "lrytas.lt":
            article_nodes = tree.xpath("//div[contains(@class, 'col-span-12')]")
            for article in article_nodes:
                #Istraukiamas pavadinimas
                title = article.xpath(".//h2[contains(@class,'text-base')]/a/text()")
                if title:
                    title[0].strip()

                image_url = article.xpath(".//div/a/img[contains(@class,'rounded-t-[4px] object-cover w-full h-full absolute top-0 left-0 right-0 bottom-0 z-10')]/@src")
                #Patikrinama, ar img_url ne tuscias
                if image_url:
                   image_url[0].strip()

                category = article.xpath(".//div[contains(@class,'flex items-center justify-between')]/a/span[contains(@class, 'text-xs ml-1.5')]/text()")
                if category:
                   category[0].strip()

                #idedame i list
                straipsniaiList.append((title, image_url, category))

        #Sukuriama funkcija, kuri issaugoja i faila
        save_to_file(source, vaistaiList, straipsniaiList, return_format)

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def save_to_file(source, vaistaiList, straipsniaiList, return_format):
    currentList = []
    if source == "camelia.lt":
        currentList = vaistaiList
        fileName = "vaistaiList"
    elif source == "lrytas.lt":
        currentList = straipsniaiList
        fileName = "straipsniaiList"
    else:
        print("error")

    if return_format == "list":
        for i in currentList:
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
                for element in currentList:
                    writer.writerow(element)
            print(f"CSV failas sukurtas: {fileName}.csv")
        except Exception as e:
            print(f"CSV failo klaida: {e}")
            return None
    # Jeigu formatas "json", issaugoja faila i json
    elif return_format == "json":
        try:
            with open(f"{fileName}.json", "w", newline='', ) as jsonFile:
                json.dump(currentList, jsonFile, ensure_ascii=False, indent=4)
            print(f"Json failas sukurtas: {fileName}.json")
        except Exception as e:
            print(f"Json failo klaida: {e}")
    else:
        # Netinkamo formato error
        raise ValueError("Nepalaikomas formatas. Naudokite 'list', 'csv' arba 'json'.")


