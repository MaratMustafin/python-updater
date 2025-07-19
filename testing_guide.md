# Пример файлов для тестирования приложения

## 1. Создайте файл version.txt на вашем сервере:
```
1.0.2
```

## 2. Создайте тестовый ZIP файл myfile.zip со структурой:
```
myfile.zip
├── update/
│   ├── app.exe
│   ├── config.ini
│   └── data/
│       └── example.txt
```

## 3. Вычислите SHA256 хеш файла:

### Windows (PowerShell):
```powershell
Get-FileHash -Path "myfile.zip" -Algorithm SHA256
```

### Windows (Command Prompt):
```cmd
certutil -hashfile myfile.zip SHA256
```

### macOS/Linux:
```bash
sha256sum myfile.zip
```

### Python скрипт:
```python
import hashlib

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

print(calculate_sha256("myfile.zip"))
```

## 4. Создайте файл myfile.zip.sha256 с хешем:
```
a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3
```

## 5. Настройте веб-сервер для размещения файлов:

### Nginx конфигурация:
```nginx
server {
    listen 80;
    server_name example.com;
    
    location /version.txt {
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'Authorization';
        
        # Проверка токена
        if ($http_authorization != "Bearer your-secret-token") {
            return 401;
        }
        
        root /var/www/updates;
        try_files $uri =404;
    }
    
    location ~ \.(zip|sha256)$ {
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'Authorization';
        
        # Проверка токена
        if ($http_authorization != "Bearer your-secret-token") {
            return 401;
        }
        
        root /var/www/updates;
        try_files $uri =404;
    }
}
```

### Apache конфигурация:
```apache
<VirtualHost *:80>
    ServerName example.com
    DocumentRoot /var/www/updates
    
    <Directory "/var/www/updates">
        Header always set Access-Control-Allow-Origin "*"
        Header always set Access-Control-Allow-Methods "GET, OPTIONS"
        Header always set Access-Control-Allow-Headers "Authorization"
        
        # Проверка токена через mod_rewrite
        RewriteEngine On
        RewriteCond %{HTTP:Authorization} !^Bearer\ your-secret-token$
        RewriteRule .* - [R=401,L]
    </Directory>
</VirtualHost>
```

## 6. Простой Python сервер для тестирования:

```python
# test_server.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json

class UpdateHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Проверка авторизации
        auth_header = self.headers.get('Authorization')
        if auth_header != 'Bearer your-test-token':
            self.send_response(401)
            self.end_headers()
            return
        
        if self.path == '/version.txt':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'1.0.2')
            
        elif self.path == '/myfile.zip':
            if os.path.exists('myfile.zip'):
                self.send_response(200)
                self.send_header('Content-Type', 'application/zip')
                self.end_headers()
                with open('myfile.zip', 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                
        elif self.path == '/myfile.zip.sha256':
            if os.path.exists('myfile.zip.sha256'):
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                with open('myfile.zip.sha256', 'r') as f:
                    self.wfile.write(f.read().encode())
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), UpdateHandler)
    print("Сервер запущен на http://localhost:8000")
    print("Токен для тестирования: your-test-token")
    server.serve_forever()
```

## 7. Настройки для тестирования в приложении:

- **Токен**: your-test-token
- **URL версии**: http://localhost:8000/version.txt
- **URL загрузки**: http://localhost:8000/myfile.zip
- **URL хеша**: http://localhost:8000/myfile.zip.sha256
