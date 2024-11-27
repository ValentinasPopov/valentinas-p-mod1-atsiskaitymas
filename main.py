from valentinas_p_mod1_atsiskaitymas.web_crawling import crawling


def main():

    crawling(time_limit=10, source="camelia.lt", return_format="csv")

if __name__ == '__main__':
    main()
