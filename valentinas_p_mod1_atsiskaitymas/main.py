
from web_crawling import WebCrawling

def main():
    crawling = WebCrawling()
    crawling.read_from_website("eurovaistine.lt", 5)
    crawling.save_file()

if __name__ == '__main__':
    main()