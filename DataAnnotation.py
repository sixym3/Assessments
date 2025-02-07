# url = "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub"
url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"

import requests
from bs4 import BeautifulSoup

def get_table(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        contents_div = soup.find('div', {'id': 'contents'})
        if contents_div:
            table = contents_div.find('table')
            if table:
                return table
        return None
    except Exception as e:
        return f"Error: {e}\nSoup: {soup.prettify()}"

def parse_table(table):
    result = {}
    rows = table.find_all('tr')
    x, y = 0, 0
    for row in rows:
        cells = row.find_all('td')
        try:
            curr_x = int(cells[0].text)
            curr_y = int(cells[2].text)
            result[(curr_x, curr_y)] = cells[1].text
            x = max(x, curr_x)
            y = max(y, curr_y)
        except ValueError:
            continue
        except Exception as e:
            print(f"Error: {e}\nRow: {row.prettify()}")
    return result, x + 1, y
            
def decode_doc(url):
    table_soup = get_table(url)
    characters, x, y = parse_table(table_soup)
    for j in range(y, -1, -1):
        for i in range(x):
            if (i, j) in characters:
                print(characters[(i, j)], end="")
            else:
                print(" ", end="")
        print()

if __name__ == "__main__":
    decode_doc(url)