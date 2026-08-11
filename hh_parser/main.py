import requests
import pandas as pd
import time

def parse_hh_vacancies(keyword="Python", pages=2):
    """
    Собирает вакансии с hh.ru через API
    """
    all_vacancies = []
    for page in range(pages):
        url = "https://api.hh.ru/vacancies"
        params = {
            "text": keyword,
            "area": 1,  # 1 = Москва, 2 = Санкт-Петербург
            "per_page": 20,
            "page": page
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            for item in data.get("items", []):
                salary = item.get("salary")
                salary_from = salary.get("from") if salary else "Не указана"
                
                all_vacancies.append({
                    "Название": item.get("name", "Не указано"),
                    "Компания": item.get("employer", {}).get("name", "Не указана"),
                    "Зарплата от": salary_from,
                    "Ссылка": item.get("alternate_url", "")
                })
            
            print(f"Страница {page + 1} обработана")
            time.sleep(0.5)
        except Exception as e:
            print(f"Ошибка на странице {page + 1}: {e}")
    
    return all_vacancies

if __name__ == "__main__":
    print("Начинаю сбор вакансий...")
    vacancies = parse_hh_vacancies("Python", pages=2)
    
    if vacancies:
        df = pd.DataFrame(vacancies)
        df.to_excel("hh_vacancies.xlsx", index=False)
        print(f"✅ Собрано {len(vacancies)} вакансий. Файл сохранён.")
    else:
        print("❌ Не удалось собрать данные")
