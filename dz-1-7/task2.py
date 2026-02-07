import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("Ошибка: API ключ не найден в файле .env")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "ru"
    }
    
    try:
        response = requests.get(url, params=params)
        
        response.raise_for_status()
        
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        
        print(f"--- Погода в городе {data['name']} ---")
        print(f"Температура: {temp}°C")
        print(f"Описание: {desc.capitalize()}")
        
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print("Ошибка: Неверный API ключ. Проверьте .env")
        elif response.status_code == 404:
            print("Ошибка: Город не найден.")
        else:
            print(f"HTTP ошибка: {http_err}")
    except Exception as err:
        print(f"Произошла ошибка: {err}")

if __name__ == "__main__":
    get_weather("Москва")
