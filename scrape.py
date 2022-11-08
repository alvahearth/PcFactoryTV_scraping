import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import csv

BASE_DIR = Path(__file__).resolve().parent

def create_file():
    try:
        #data = ["Nombre", "Precio", "Marca"]
        with open('hola.csv', 'w', encoding="uft8") as f1:
            writer = csv.writer(f1)
            #writer.writerow(data)
            f1.close()
    except:
        os.remove(os.path.join(BASE_DIR, "hola.csv"))
        #data = ["Nombre", "Precio", "Marca"]
        with open('hola.csv', 'x') as f1:
            writer = csv.writer(f1)
            #writer.writerow(data)
            f1.close()

def update_file(x, y, z):
    data = [x, y, z]
    with open('hola.csv', 'a', encoding="UTF8") as f1:
        writer = csv.writer(f1)
        writer.writerow([x, y, z])
        f1.close()

def call_url(index=1):
    return f"https://www.pcfactory.cl/smart-tv?categoria=790&papa=789&pagina={index}"

def obtain_pages(obj):
    all_products= obj.findAll("div", {"class": "product-filters__heading"})
    n = all_products[1].find("div", {"class": "link color-primary-1"}).text
    return n.split()

create_file()

url = call_url()
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

remaining_pages = obtain_pages(soup)

count = 1
r_pages = int(remaining_pages[4])
while True:
    url = call_url(count)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    print(url)

    containers = soup.findAll("div", {"class": "product"})
    print(containers[0])
    for container in range(0, len(containers)):
        price = containers[container].find("div", {"class": "product__price"})
        price_fixed = price.find("div", {"class": "title-md color-primary-1"}).text
        price_fixed = price_fixed.replace("$", "")

        name = containers[container].find("div", {"class" :"price color-dark-2 product__card-title"}).text
        name_fixed = name.replace("”", "")

        brand = containers[container].find("div", {"class": "product__heading"}).text
        brand_fixed = "".join(brand.split())
        brand_fixed = brand_fixed.replace("®", " ")

        update_file(name_fixed, price_fixed, brand_fixed)
        print(name_fixed)

    num2 = int(remaining_pages[2])
    
    if r_pages - num2 < 0:
        break
    else:
        count += 1
        r_pages = r_pages - num2