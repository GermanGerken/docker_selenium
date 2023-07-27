import csv
import time
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver

# set up Chrome driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

# navigate to amazon homepage
driver.get('https://www.amazon.com/')

# find searchbar and input
title_element = driver.find_element("id", "twotabsearchtextbox")
title_element.send_keys("apple macbook")
driver.find_element("id", "nav-search-submit-button").click()
time.sleep(10)

response = driver.page_source
soup = BeautifulSoup(response, 'html.parser')

products = soup.findAll("div", class_="s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis s-latency-cf-section s-card-border")

# scrape results
for product in products:
    try:
        name = product.find("span", class_="a-size-medium a-color-base a-text-normal").text
    except Exception as ex:
        name = ""
    try:
        price = product.find("span", class_="a-price-whole").text
    except Exception as ex:
        price = ""

    exist = Path('/amazon_scrape/amazon.csv').is_file()
    if not exist:
        with open('/amazon_scrape/amazon.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["name", "price"])
    print(name, price)
    with open('amazon.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([name, price])




# quit driver
driver.quit()