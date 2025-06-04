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









#detalii_text = [d.get_text(strip=True) for d in detalii]
# li=soup.find_all('li')
# print(li)
# for tag in soup.find_all(class_='specs'):
#     for i,li in tag.find_next('ul').find_all('li'):
#         print(li)

    
# for element in pret:
#     text = element.get_text()
#     res = ''.join(filter(str.isdigit,text))
#     print(str(res))
    
# for detaliu in detalii_text:
#     det1=detaliu[0]
#     an=detaliu[3]
#     km=detaliu[2]
#     onlyKm=''.join(filter(str.isdigit,km))
#     print(an +"    "+ onlyKm)

# for li in soup.find_all('ul',class_="specs list-unstyled d-flex flex-wrap darkGrayText"):
#     detalii = li.select_one('[class="specs list-unstyled d-flex flex-wrap darkGrayText"] li:nth-child(1) > span').get_text()
#     km = li.select_one('[class="specs list-unstyled d-flex flex-wrap darkGrayText"] li:nth-child(2) > span').get_text()
#     an = li.select_one('[class="specs list-unstyled d-flex flex-wrap darkGrayText"] li:nth-child(3) > span').get_text()
#     onlyKm=''.join(filter(str.isdigit,km))
#     print(an +"    "+ onlyKm)


