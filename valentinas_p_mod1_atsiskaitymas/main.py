
from web_crawling import crawling


def main():

    crawling(time_limit=10, source="https://camelia.lt/c/prekiu-medis/vitaminai-maisto-papildai-mineralai/groziui-903", return_format="list")

if __name__ == '__main__':
    main()