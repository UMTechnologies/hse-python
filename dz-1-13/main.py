import requests
import json
import os

"""
Для запуска необходимо:
1. Зарегистрироваться на https://www.virustotal.com/ и получить API-ключ в личном кабинете.
2. Задать переменную окружения VIRUS_TOTAL_API_KEY.
4. Запустить скрипт: uv run main.py
"""

def get_file_report(api_key, file_hash):
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    
    headers = {
        "accept": "application/json",
        "x-apikey": api_key
    }

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return data
        elif response.status_code == 401:
            return {"error": "Ошибка авторизации. Проверьте ваш API-ключ."}
        elif response.status_code == 404:
            return {"error": "Файл с таким хешем не найден в базе VirusTotal."}
        else:
            return {"error": f"Произошла ошибка: {response.status_code}", "details": response.text}
            
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    API_KEY = os.getenv("VIRUS_TOTAL_API_KEY") 

    # хеш тестового файла EICAR, который определяется как вирус
    target_hash = "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f"
    
    print(f"Запрос данных для хеша: {target_hash}\n")
    
    result = get_file_report(API_KEY, target_hash)

    print(json.dumps(result, indent=4, ensure_ascii=False))
