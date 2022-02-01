from selenium import webdriver
import time, requests
import numpy as np
import pandas as pd
import pickle
import time


# (fonte) -- https://clutchpoints.com/updating-and-ranking-the-50-greatest-nfl-players-of-all-time/


def load_best():
    open_file = open("mlb_best.pkl", "rb")
    lista_retorno = pickle.load(open_file)
    open_file.close()
    return lista_retorno


def search_player(search_query):
    browser = webdriver.Chrome("/home/temp/Downloads/chromedriver")
    search_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search_query}"
    images_url = []

    # open browser and begin search
    browser.get(search_url)
    elements = browser.find_elements_by_class_name("rg_i")

    count = 0
    for e in elements:
        # get images source url
        e.click()
        time.sleep(1)
        element = browser.find_elements_by_class_name("v4dQwb")

        # Google image web site logic
        if count == 0:
            big_img = element[0].find_element_by_class_name("n3VNCb")
        else:
            big_img = element[1].find_element_by_class_name("n3VNCb")

        images_url.append(big_img.get_attribute("src"))

        # write image to file
        try:
            reponse = requests.get(images_url[count])
            if reponse.status_code == 200:
                with open(f"{search_query[:9]}{count+1}.jpg", "wb") as file:
                    file.write(reponse.content)

            count += 1

            # Stop get and save after 5
            if count > 3:
                break
        except:
            count += 1
        else:
            count += 5
    return images_url


def search_google(search_query):
    browser = webdriver.Chrome("/home/temp/Downloads/chromedriver")
    search_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search_query}"
    images_url = []

    # open browser and begin search
    browser.get(search_url)
    elements = browser.find_elements_by_class_name("rg_i")

    count = 0
    for e in elements:
        # get images source url
        e.click()
        time.sleep(1)
        element = browser.find_elements_by_class_name("v4dQwb")

        # Google image web site logic
        if count == 0:
            big_img = element[0].find_element_by_class_name("n3VNCb")
        else:
            big_img = element[1].find_element_by_class_name("n3VNCb")

        images_url.append(big_img.get_attribute("src"))

        # write image to file
        try:
            reponse = requests.get(images_url[count])
            if reponse.status_code == 200:
                with open(f"center{count+1}.jpg", "wb") as file:
                    file.write(reponse.content)

            count += 1

            # Stop get and save after 5
            if count > 30:
                break
        except:
            count += 1
    return images_url


search_google("baseball player Center fielder")
