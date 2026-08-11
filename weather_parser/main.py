import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_weather(city="moscow"):
    """
    Парсит погоду с Yandex.Погода
    """
    url = f"https://yandex.ru/pogoda/{city}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        temp = soup.find("span", class_="temp__value")
        description = soup.find("div", class_="link__condition")
        
        result = {
            "city": city,
            "temperature": temp.text.strip() if temp else "Нет данных",
            "description": description.text.strip() if description else "Нет данных",
            "time": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return result
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

if __name__ == "__main__":
    print("Начинаю парсинг погоды...")
    weather = get_weather("moscow")
    
    if weather:
        print(f"Погода в Москве: {weather['temperature']}°, {weather['description']}")
        df = pd.DataFrame([weather])
        df.to_csv("weather.csv", index=False, encoding="utf-8-sig")
        print("Результат сохранён в weather.csv")
    else:
        print("Не удалось получить данные")

  Добавил README для парсера погоды
