import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def parse_avito(query="iphone", pages=2):
    """
    Парсит объявления Avito (учебный пример)
    """
    items = []
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    ]
    
    for page in range(1, pages + 1):
        url = f"https://www.avito.ru/moskva?q={query}&p={page}"
        headers = {
            "User-Agent": random.choice(user_agents)
        }
        
        try:
            print(f"Страница {page}/{pages}...")
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"Ошибка {response.status_code}")
                continue
                
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.find_all("div", class_="iva-item-content")
            
            for card in cards:
                title = card.find("h3")
                price = card.find("span", class_="price")
                
                items.append({
                    "Название": title.text.strip() if title else "Нет названия",
                    "Цена": price.text.strip() if price else "Нет цены"
                })
            
            print(f"Найдено {len(cards)} объявлений")
            time.sleep(random.uniform(1.5, 3.0))  # Случайная задержка
            
        except Exception as e:
            print(f"Ошибка на странице {page}: {e}")
    
    return items

if __name__ == "__main__":
    print("Начинаю парсинг Avito (учебный режим)...")
    data = parse_avito("iphone", pages=2)
    
    if data:
        df = pd.DataFrame(data)
        df.to_csv("avito_items.csv", index=False, encoding="utf-8-sig")
        print(f"✅ Собрано {len(data)} объявлений")
    else:
        print("❌ Данные не получены")
