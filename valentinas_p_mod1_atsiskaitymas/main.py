
from web_crawling import WebCrawling

def main():
    crawling = WebCrawling()
    crawling.read_from_website("camelia.lt", 5)
    crawling.save_file("camelia.lt", "vaistuPavadinimai", "json")

if __name__ == '__main__':
    main()