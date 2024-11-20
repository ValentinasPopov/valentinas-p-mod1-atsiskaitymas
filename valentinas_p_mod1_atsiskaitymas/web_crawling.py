from requests import get
from lxml.etree import HTML

class WebCrawling:
    def __init__(self):
        pass
    def read_from_website(self, selected_site):


        if selected_site == "eurovaistine.lt":
            url = "https://camelia.lt/c/prekiu-medis/vitaminai-maisto-papildai-mineralai/groziui/plaukams-1-1522"
        elif selected_site == "lrytas.lt":
            url = "https://lrytas.lt"
        else:
            raise ValueError("svetaine nera sarase")

        response = get(url)
        text = response.text
        tree = HTML(text)
        pavadinimasList = []
        paveikslaiList = []

        match selected_site:
            case "eurovaistine.lt":
                elements = tree.xpath("//div[contains(@class, 'product-card')]")
                for element in elements:
                    try:
                        pavadinimas_text = element.xpath(".//div[contains(@class,'product-name')]/text()")
                        if pavadinimas_text:
                            pavadinimasList.append(pavadinimas_text[0].strip())

                        paveikslai_text = element.xpath(".//div/img[contains(@class,'product-image')]/@src")
                        if paveikslai_text:
                            paveikslaiList.append(paveikslai_text[0].strip())
                    except IndexError:
                        print("Elementai nerasti")


        #print("Produktu pavadinimai: ")
        #for name in pavadinimasList:
           #print(name)

        #print("\n Nuotraukos:")
        #for img_url in paveikslaiList:
            #print(img_url)



    def save_from_website(self, format):
        pass