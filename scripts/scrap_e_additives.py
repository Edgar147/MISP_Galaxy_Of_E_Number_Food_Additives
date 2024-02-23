import requests
from bs4 import BeautifulSoup
import uuid
import json
import re

url = "https://dermnetnz.org/topics/food-additives-and-e-numbers"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

tables = soup.find_all('table')

food_additives_info = []

# Banned
ignored_additives = ['E161g', 'E171', 'E128']


def process_cell_content(cell):
    content = ""
    if cell.find('ul'):
        lists = cell.find_all('li')
        for index, item in enumerate(lists):
            content += item.text.strip()
            if index == 0 and len(
                    lists) > 1:
                content += ", "
            elif index < len(lists) - 1:
                content += " "
    else:
        content = cell.text.strip()

    if not content:
        content = "Examples not specified"
    return content


for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 4:
            e_number = cells[0].text.strip()
            if e_number in ignored_additives:
                continue

            if '-' in e_number:
                continue
            if e_number.startswith('E') and any(char.isdigit() for char in e_number):
                name = cells[1].text.strip()
                description = process_cell_content(cells[2])
                examples_of_use = process_cell_content(cells[3])

                food_additives_info.append({
                    'E-Number': e_number,
                    'Name': name,
                    'Description': description,
                    'UsedIn': examples_of_use
                })

base_detail_url = "https://proe.info/additives/"


def fetch_additive_details(e_number):
    detail_url = f"{base_detail_url}{e_number.lower()}"
    response = requests.get(detail_url)
    detail_soup = BeautifulSoup(response.content, 'html.parser')

    origin_element = detail_soup.find(class_="addprop addprop--origin")
    if origin_element:
        origin_text = origin_element.text.strip().replace('\n', ', ')
        origin = origin_text.replace('origin', '').replace('  ', ' ')
    else:
        origin = "Details unavailable"

    danger_element = detail_soup.find(class_="addprop addprop--danger")
    if danger_element:
        danger_text = danger_element.text.strip().replace('\n', ', ')
        danger = danger_text.replace('danger', '').replace('  ', ' ')
    else:
        danger = "Details unavailable"

    category_element = detail_soup.find(class_="addprop addprop--category")
    if category_element:
        category = category_element.text.strip().replace('\n', ', ')
    else:
        category = "Details unavailable"

    return origin, danger, category


for additive in food_additives_info:
    origin, danger, category = fetch_additive_details(additive['E-Number'])
    additive['Origin'] = origin
    additive['Danger'] = danger
    additive['Category'] = category

base_detail_url = "https://www.additifs-alimentaires.net/"


def fetch_additive_details_bio(e_number):
    detail_url = f"https://www.additifs-alimentaires.net/{e_number}.php"
    response = requests.get(detail_url)
    detail_soup = BeautifulSoup(response.content, 'html.parser')

    bio_status_element = detail_soup.find_all('img', alt=True)
    bio = "Not specified"
    for img in bio_status_element:
        if "Exclu du Bio." in img['alt']:
            bio = "No"
            break
        elif "Autorisé Bio." in img['alt']:
            bio = "Yes"
            break

    return bio


for additive in food_additives_info:
    bio_status = fetch_additive_details_bio(additive['E-Number'])
    additive['Bio'] = bio_status


def fetch_products_using_additive(e_number):
    product_name = ""
    url = f"https://uk.openfoodfacts.org/additive/{e_number.lower()}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    spans = soup.select("ul.products a > span")

    for span in spans:
        text = span.text.strip()
        if re.search("[a-zA-Z].*[a-zA-Z]", text):
            product_name = text
            break

    return product_name


for additive in food_additives_info:
    product_name = fetch_products_using_additive(additive['E-Number'])
    additive['Product'] = product_name if product_name else "Not available"


def generate_uuid():
    return str(uuid.uuid4())


url = "https://en.wikipedia.org/wiki/E_number"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

ignored_additives = ['e161g', 'e171', 'e128']
tables = soup.find_all('table', {'class': 'wikitable'})
icolour = 1
for table in tables:
    headers = [th.get_text(strip=True) for th in table.find_all('th')]
    if 'Code' in headers:
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) > 0:
                e_number = cols[0].text.strip()

                # Exclude
                if e_number in ['E392', 'E427', 'E554', 'E555', 'E907', 'E1517', 'E444', 'E1105']:
                    continue
                icolour = icolour + 1
                name = cols[1].text.strip() if len(cols) > 1 else "Unknown"
                if icolour <= 67:
                    category = "Colour"
                elif cols[2].text.strip():
                    category = cols[2].text.strip()
                else:
                    category = "Unknown"

                status = "Unknown"
                if len(cols) > 3:
                    status = cols[3].text.strip()

                if status == "" or "Unknown" in status or \
                        any(s in status for s in ["Not approved in the EU", "Forbidden in the EU", "Banned in the EU",
                                                  "Previously approved in the EU", "No longer approved in the EU"]):
                    food_additives_info.append({
                        'E-Number': e_number,
                        'Origin': 'Details unavailable',
                        'Name': name,
                        'Category': category,
                        'Bio': 'No',
                        'Danger': 'Details unavailable',
                        'UsedIn': 'Not specified',
                        'Product': 'Not available',
                        'Description': 'Banned in the EU'
                    })

uuid_galaxy = generate_uuid()
misp_galaxy = {
    "description": "E number food additives",
    "icon": "additive",
    "authors": [
        "Edgar Karapetyan, Jawad El Amraoui"
    ],
    "type": "e-additives",
    "uuid": uuid_galaxy,
    "version": 1
}

json_data = json.dumps(misp_galaxy, indent=4)

try:
    with open("../galaxies/e-additives-galaxy.json", "w") as file:
        file.write(json_data)
except FileNotFoundError:
    with open("galaxies/e-additives-galaxy.json", "w") as file:
        file.write(json_data)

clusters = []

for additive in food_additives_info:
    cluster = {
        "meta": {
            "category": additive.get('Category', "Unknown"),
            "origin": additive.get('Origin', "Unknown"),
            "name": additive.get('Name', "Unknown"),
            "danger": additive.get('Danger', "Unknown"),
            "allowed_in_bio": additive.get('Bio', "Not specified"),
            "used_in": additive.get('UsedIn', "Not specified"),
            "product": additive.get('Product', "Not available"),
        },
        "description": additive.get('Description', ""),
        "value": additive.get('E-Number', ""),
        "uuid": generate_uuid()
    }
    clusters.append(cluster)

final_structure = {
    "authors": [
        "Edgar Karapetyan, Jawad El Amraoui"
    ],
    "category": "food additives",
    "description": "E number food additives",
    "name": "E additives",
    "sources": ["OpenFoodFacts", "Wikipedia", "Dermnetnz","Proe","additifs-alimentaires"],
    "type": "e-additives",
    "uuid": uuid_galaxy,
    "values": clusters
}

json_data = json.dumps(final_structure, ensure_ascii=False, indent=4)

try:
    with open("../clusters/e-additives-cluster.json", "w", encoding="utf-8") as file:
        file.write(json_data)
except FileNotFoundError:
    with open("clusters/e-additives-cluster.json", "w", encoding="utf-8") as file:
        file.write(json_data)
