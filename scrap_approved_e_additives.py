import requests
from bs4 import BeautifulSoup


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
                continue  # Passer à l

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
                    'Examples of Use': examples_of_use
                })

base_detail_url = "https://proe.info/additives/"


def fetch_additive_details(e_number):
    detail_url = f"{base_detail_url}{e_number.lower()}"  # Construire l'URL de la page de détail
    response = requests.get(detail_url)
    detail_soup = BeautifulSoup(response.content, 'html.parser')

    # Récupération et traitement de l'origine
    origin_element = detail_soup.find(class_="addprop addprop--origin")
    if origin_element:
        origin_text = origin_element.text.strip().replace('\n', ', ')
        origin = origin_text.replace('origin', '').replace('  ', ' ')  # Supprime 'origin' et les doubles espaces
    else:
        origin = "Details unavailable"

    # Récupération et traitement du danger
    danger_element = detail_soup.find(class_="addprop addprop--danger")
    if danger_element:
        danger_text = danger_element.text.strip().replace('\n', ', ')
        danger = danger_text.replace('danger', '').replace('  ', ' ')  # Supprime 'danger' et les doubles espaces
    else:
        danger = "Details unavailable"

    # Récupération de la catégorie
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
            bio = "no"
            break
        elif "Autorisé Bio." in img['alt']:
            bio = "yes"
            break

    return bio

for additive in food_additives_info:
    bio_status = fetch_additive_details_bio(additive['E-Number'])
    additive['Bio'] = bio_status

product_names = []

def fetch_products_using_additive(e_number):
    url = f"https://fr.openfoodfacts.org/additif/{e_number.lower()}"
    print("url de base=="+url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }


    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    spans = soup.select("ul.products a > span", limit=2)

    for span in spans:
        product_names.append(span.text.strip())
    return product_names




for additive in food_additives_info:
    product_names = fetch_products_using_additive(additive['E-Number'])

    if len(product_names) > 0:
        additive['Product1'] = product_names[0]
    else:
        additive['Product1'] = "Non disponible"

    if len(product_names) > 1:
        additive['Product2'] = product_names[1]
    else:
        additive['Product2'] = "Non disponible"

for additive in food_additives_info:
    print(
        f"E-Number: {additive['E-Number']} || Name: {additive['Name']} || Description: {additive['Description']} || Examples of Use: {additive['Examples of Use']} || Origin: {additive['Origin']} || Danger: {additive['Danger']} || Category: {additive['Category']} || Bio: {additive['Bio']} || Product1: {additive['Product1']}|| Product2: {additive['Product2']}")


##Verify
# file_path = 'authorized.txt'
#
# with open(file_path, 'w') as file:
#     for additive in food_additives_info:
#         file.write(f"{additive['E-Number']}\n")
