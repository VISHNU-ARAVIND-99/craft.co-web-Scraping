from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd


def scroll_down():
    start = time.time()
    initial_scroll = 0
    finals_sroll = 1000

    while True:
        driver.execute_script(f"window.scrollTo({initial_scroll},{finals_sroll})")

        initial_scroll = finals_sroll
        finals_sroll += 1000
        time.sleep(1)
        end = time.time()
        if round(end - start) > 20:
            break


def craft_scraping(company_name):
    driver.get("https://www.google.com/")
    driver.maximize_window()
    time.sleep(1)
    search1 = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
    search1.send_keys(f"{company_name} ceo and key executive team + craft.co")
    search1.send_keys(Keys.RETURN)
    time.sleep(1)
    first_link1 = driver.find_element(By.CLASS_NAME, 'byrV5b')
    first_link1.click()
    time.sleep(3)

    scroll_down()

    time.sleep(1)

    source = BeautifulSoup(driver.page_source, "html.parser")
    info1 = source.find_all('div', class_='KeyPersonStyled__InfoWrapper-sc-rgxd4k-6 jRvgDf')

    for x in info1:
        a = "nil"
        b = "nil"
        c = "nil"
        d = "nil"
        links12 = x.find_all("a")
        if len(links12) > 0:
            g = links12[0].get("href")
            if "linkedin" in g:
                a = g
            else:
                d = g
            if len(links12) == 2:
                d = links12[1].get("href")

        name = x.find('h3', class_='KeyPersonStyled__KeyPersonName-sc-rgxd4k-9 gfAFIs')
        if name:
            b = name.text.strip()

        title = x.find('div', class_='KeyPersonStyled__KeyPersonJobPosition-sc-rgxd4k-10 kLbvmG')
        if title:
            c = title.text.strip()

        list_of_list.append([company_name, b, c, a, d])


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

list_of_list = []
with open('company.txt', 'r') as file:
    links = file.readlines()
name_list = [x.strip() for x in links]


for k in name_list:
    craft_scraping(company_name=k)

df = pd.DataFrame(list_of_list, columns=['Company Name', 'NAME', 'Title', 'Linkedin_Link', 'Twitter_Link'])
df.to_excel('Craft.Co_output1.xlsx', index=False)
