import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import time
import json
import csv
import pandas as pd

s  = Service("/home/temp/Downloads/chromedriver")
wd = webdriver.Chrome(service=s)


def fetch_image_urls(
    query: str,
    max_links_to_fetch: int,
    wd: webdriver,
    sleep_between_interactions: int = 0.1,
):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #time.sleep(sleep_between_interactions)

    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)

        print(
            f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}"
        )

        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                #time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls
            actual_images = wd.find_elements_by_css_selector("img.n3VNCb")
            for actual_image in actual_images:
                if actual_image.get_attribute(
                    "src"
                ) and "http" in actual_image.get_attribute("src"):
                    image_urls.add(actual_image.get_attribute("src"))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            #time.sleep(30)
            return
            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls


if __name__ == "__main__":
    #TODO: onde vc le
    df = pd.read_csv("nfl_rest.csv")
    #FIXME: onde vc escreve
    data_file = open("nfl_jogadores_url2.csv", "w")

    books_list = df["Players"].unique()

    # FIXME: salvar dictionary as json file
    writer = csv.writer(data_file)
    for books in books_list:
        url = str(fetch_image_urls(books + " NFL player", 1, wd))
        writer.writerow([books, url])

    # FIXME: scrapping
    # losta = fetch_image_urls("Gone Girl book cover", 1, wd)
    wd.quit()
