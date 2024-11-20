import requests
import csv
import json
from lxml import html
from time import time
from typing import Optional


def crawling(time_limit: int = 60, source: str = "https://camelia.lt", return_format: str = "list") -> Optional[str]:

    vaistaiList = []
    try:
        #Pradeda skaiciuoti laika
        start_time = time()
        response = requests.get(source, timeout=time_limit)

        #Raise HTTPError
        response.raise_for_status()

        # Parse HTML
        tree = html.fromstring(response.text)

        product_nodes = tree.xpath("//div[contains(@class, 'product-card')]")

        for product in product_nodes:
            # Istraukiamas tekstas
            text = product.xpath(".//div[contains(@class,'product-name')]/text()")[0].strip()

            # Istraukiama paveiksleliu URL
            image_url = product.xpath(".//div/img[contains(@class,'product-image')]/@src")[0].strip()

            # Idedame i list
            vaistaiList.append((text,image_url))

        #Apskaiciuota, per kiek laiko rado paveikslelius ir teksta
        elapsed_time = time() - start_time
        print(elapsed_time)

        # Jeigu formatas "list", isspausdina i console
        if return_format == "list":

            for i in vaistaiList:
                print(i)
        # Jeigu formatas "csv", issaugoja faila i csv
        elif return_format == "csv":
            try:
                with open('Test.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Pavadinimas', 'Nuotraukos URL'])
                    for element in vaistaiList:
                        writer.writerow(element)
                print("CSV failas sukurtas: vaistai.csv")
                return "CSV failas sukurtas"
            except Exception as e:
                print(f"CSV failo klaida: {e}")
                return None
        # Jeigu formatas "json", issaugoja faila i json
        elif return_format == "json":
            with open("Test.json", "w", newline='', ) as jsonFile:
                json.dump(vaistaiList, jsonFile, ensure_ascii=False, indent=4)
        else:
            # Netinkamo formato error
            raise ValueError("Nepalaikomas formatas. Naudokite 'list', 'csv' arba 'json'.")


    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
