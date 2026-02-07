import requests

def fetch_posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        posts = response.json()
        
        for i, post in enumerate(posts[:5], 1):
            print(f"{i}. ЗАГОЛОВОК: {post['title']}")
            print(f"   ТЕЛО: {post['body']}\n")
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")

if __name__ == "__main__":
    fetch_posts()
