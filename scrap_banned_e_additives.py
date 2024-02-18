import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/E_number"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

additives_info = []

# Approved, but in the list
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
                    additives_info.append({
                        'E-Number': e_number,
                        'Name': name,
                        'Category': category,
                        # 'Status': status if status else "Unknown"
                    })

for additive in additives_info:
    print(f"E-Number: {additive['E-Number']}, Name: {additive['Name']}, Category: {additive['Category']}")

# Verify
# file_path = 'banned.txt'
#
# with open(file_path, 'w') as file:
#     for additive in additives_info:
#         file.write(f"{additive['E-Number']}\n")
