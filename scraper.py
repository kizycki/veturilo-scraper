import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
import time

url = 'https://veturilo.waw.pl/mapa-stacji/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def scrape_stations():
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Szukamy tabeli stacji (dostosowane do struktury strony)
    stations = []
    rows = soup.select('table tr')  # Dostosuj selektor jeśli potrzeba
    for row in rows[1:10]:  # Test pierwszych 10 dla bezpieczeństwa
        cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
        if len(cells) >= 3:
            stations.append(cells[:3])  # nazwa, numer, rowery
    
    return stations

def append_to_csv(stations):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = []
    for stacja in stations:
        data.append({
            'timestamp': now,
            'nazwa': stacja[0],
            'numer': stacja[1],
            'rowery': stacja[2]
        })
    
    df_new = pd.DataFrame(data)
    
    if os.path.exists('stations.csv'):
        df_old = pd.read_csv('stations.csv')
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new
    
    df.to_csv('stations.csv', index=False)
    print(f'Zapisano {len(stations)} stacji o {now}')

if __name__ == '__main__':
    stations = scrape_stations()
    append_to_csv(stations)
