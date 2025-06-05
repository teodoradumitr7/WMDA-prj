import requests
from bs4 import BeautifulSoup
import pandas as pd

toate_masinile = []

for page_number in range(2, 8):  
    url = f"https://www.tiriacauto.ro/auto-rulate?page={page_number}"
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'lxml')

    model_list = soup.find_all(class_='title')
    pret_list = soup.find_all(class_='orangeText')
    ul_list = soup.find_all('ul', class_='specs list-unstyled d-flex flex-wrap darkGrayText')

    for i in range(min(len(model_list), len(pret_list), len(ul_list))):
        model = model_list[i].get_text(strip=True)
        pret = pret_list[i].get_text(strip=True)
        
        li_items = ul_list[i].find_all('li')
        if len(li_items) == 3:
            fuel = li_items[0].get_text(strip=True)
            km = li_items[1].get_text(strip=True)
            year = li_items[2].get_text(strip=True)

            toate_masinile.append({
                'name': model,
                'price': pret,
                'fuel': fuel,
                'km_driven': km,
                'year': year
            })

df = pd.DataFrame(toate_masinile)
df.to_csv('data/masini_tiriac_multi.csv', index=False, encoding='utf-8-sig')

print(f"Am salvat {len(toate_masinile)} mașini în CSV.")
