
from web_crawling import crawling


def main():

    crawling(time_limit=20, source="lrytas.lt", return_format="json")

if __name__ == '__main__':
    main()
