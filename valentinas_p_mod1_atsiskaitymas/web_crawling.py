import csv
import json

from requests import get
from lxml.etree import HTML
from time import time


class WebCrawling:
    def __init__(self):
        self.vaistaiList = []
        self.straipsniaiList = []

    def read_from_website(self, selected_site, timeout_duration):
        start_time = time()

        if selected_site == "camelia.lt":
            url = "https://camelia.lt/c/prekiu-medis/vitaminai-maisto-papildai-mineralai/groziui/plaukams-1-1522"
        elif selected_site == "lrytas.lt":
            url = "https://lrytas.lt"
        else:
            raise ValueError("The website is not in the list.")

        response = get(url)
        text = response.text
        tree = HTML(text)

        # Jeigu pasirinktas "camelia.lt"
        if selected_site == "camelia.lt":
            elements = tree.xpath("//div[contains(@class, 'product-card')]")
            for element in elements:
                if time() - start_time > timeout_duration:
                    break
                try:
                    pavadinimas_text = element.xpath(".//div[contains(@class,'product-name')]/text()")
                    paveikslai_text = element.xpath(".//div/img[contains(@class,'product-image')]/@src")

                    if pavadinimas_text and paveikslai_text:
                        self.vaistaiList.append((
                            pavadinimas_text[0].strip(),
                            paveikslai_text[0].strip()
                        ))
                except IndexError:
                    print("Nerasta elementu")
                return self.vaistaiList

        #Jeigu pasirinktas "lrytas.lt"
        if selected_site == "lrytas.lt":
            return self.straipsniaiList

    def save_file(self, selected_site, filename = " ", format = " "):

        currentList = []

        if selected_site == "camelia.lt":
            currentList = self.vaistaiList
        elif selected_site == "lrytas.lt":
            currentList = self.straipsniaiList
        else:
            raise ValueError("Nera tokios svetainės sąraše")

        #issaugojama i csv faila
        if format == "list":
            return currentList
        elif format == "csv":
            with open(filename, "w", newline='', ) as cswFile:
                writer = csv.writer(cswFile)
                writer.writerows(currentList)  # Writing data
            print(f"Issaugojama i  {filename} . {format}")

        elif format == "csv":
            with open(filename, "w", newline='', ) as cswFile:
                writer = csv.writer(cswFile)
                writer.writerows(currentList)  # Writing data
            print(f"Issaugojama i  {filename} . {format}")
        elif format == "json":
            with open(filename, "w", newline='', ) as jsonFile:
                json.dump(currentList, jsonFile)
        else:
            raise ValueError("Netinkamas formatas, pasirinkite list, csv arba json")
