
from web_crawling import crawling


def main():

    crawling(time_limit=60, source="camelia.lt", return_format="json")

if __name__ == '__main__':
    main()