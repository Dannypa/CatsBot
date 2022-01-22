from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import requests


driver: webdriver


def set_up():
    global driver
    driver = webdriver.Chrome("C:\\Users\\dannu\\Downloads\\chromedriver_win32\\chromedriver.exe")


def get_cute(who="cat"):
    start_link = f"https://www.pinterest.com/search/pins/?q=cute%20{who}"
    driver.get(start_link)
    sleep(2)
    elements = driver.find_elements(By.TAG_NAME, 'a')
    links = []
    for el in elements[2:]:
        links.append(el.get_property('href'))
    for link in links:
        try:
            driver.get(link)
            sleep(2)
            img_link = driver.find_element(By.TAG_NAME, 'img').get_property("src")
            data = requests.get(img_link).content
            img_link_clean = []
            for i in range(len(img_link) - 1, -1, -1):
                if img_link[i] == '/':
                    break
                img_link_clean.append(img_link[i])
                with open(f"{who}_pics\\{''.join(reversed(img_link_clean))}", 'wb') as f:
                    f.write(data)
        except Exception as e:
            print(e)
            continue
    sleep(10)


if __name__ == '__main__':
    set_up()
    get_cute()
    get_cute("hedgehog")
    driver.close()
