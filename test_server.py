#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой тестовый сервер для демонстрации работы приложения обновлений
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json
import tempfile
import zipfile
import hashlib
from pathlib import Path


class UpdateTestServer(BaseHTTPRequestHandler):
    """Обработчик запросов тестового сервера"""
    
    def do_OPTIONS(self):
        """Обработка preflight запросов"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Authorization')
        self.end_headers()
    
    def do_GET(self):
        """Обработка GET запросов"""
        # Проверка авторизации
        auth_header = self.headers.get('Authorization')
        if auth_header != 'Bearer test-token-123':
            self.send_response(401)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Authorization')
            self.end_headers()
            self.wfile.write(b'Unauthorized: Invalid token')
            print(f"Unauthorized access attempt: {auth_header}")
            return
        
        print(f"Authorized request: {self.path}")
        
        if self.path == '/version.txt':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Authorization')
            self.end_headers()
            # Возвращаем версию 1.0.2
            self.wfile.write('1.0.2'.encode('utf-8'))
            print("Returned version: 1.0.2")
            
        elif self.path == '/myfile.zip':
            zip_path = self.create_test_zip()
            if zip_path and os.path.exists(zip_path):
                self.send_response(200)
                self.send_header('Content-Type', 'application/zip')
                self.send_header('Content-Length', str(os.path.getsize(zip_path)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Authorization')
                self.end_headers()
                
                with open(zip_path, 'rb') as f:
                    while True:
                        chunk = f.read(8192)
                        if not chunk:
                            break
                        self.wfile.write(chunk)
                
                print(f"Sent ZIP file: {zip_path}")
            else:
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'Error creating test ZIP file')
                
        elif self.path == '/myfile.zip.sha256':
            zip_path = self.create_test_zip()
            if zip_path and os.path.exists(zip_path):
                # Вычисляем хеш
                sha256_hash = hashlib.sha256()
                with open(zip_path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        sha256_hash.update(chunk)
                
                file_hash = sha256_hash.hexdigest()
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Authorization')
                self.end_headers()
                self.wfile.write(file_hash.encode('utf-8'))
                print(f"Sent hash: {file_hash}")
            else:
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'Error creating test ZIP file')
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(f'Not found: {self.path}'.encode('utf-8'))
    
    def create_test_zip(self):
        """Создать тестовый ZIP файл"""
        try:
            # Создаем временный ZIP файл
            temp_dir = Path(tempfile.gettempdir())
            zip_path = temp_dir / "myfile_test.zip"
            
            # Если файл уже существует, возвращаем его
            if zip_path.exists():
                return str(zip_path)
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Добавляем тестовые файлы
                zip_file.writestr('update/app.exe', b'Test executable content')
                zip_file.writestr('update/config.ini', 
                                 '[Settings]\nversion=1.0.2\nupdate_date=' + 
                                 str(os.urandom(16).hex()))
                zip_file.writestr('update/data/example.txt', 
                                 'This is a test update file.\nVersion: 1.0.2\n')
                zip_file.writestr('update/readme.txt', 
                                 'Test update package\nGenerated automatically for testing')
            
            print(f"Created test ZIP: {zip_path}")
            return str(zip_path)
            
        except Exception as e:
            print(f"Error creating test ZIP: {e}")
            return None
    
    def log_message(self, format, *args):
        """Переопределяем логирование для более читаемого вывода"""
        print(f"{self.address_string()} - {format % args}")


def main():
    """Запуск тестового сервера"""
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, UpdateTestServer)
    
    print("=" * 50)
    print("   ТЕСТОВЫЙ СЕРВЕР ОБНОВЛЕНИЙ")
    print("=" * 50)
    print(f"Сервер запущен на http://localhost:8000")
    print("")
    print("Настройки для приложения:")
    print("  Токен: test-token-123")
    print("  URL версии: http://localhost:8000/version.txt")
    print("  URL загрузки: http://localhost:8000/myfile.zip")
    print("  URL хеша: http://localhost:8000/myfile.zip.sha256")
    print("")
    print("Доступные эндпоинты:")
    print("  GET /version.txt - возвращает версию 1.0.2")
    print("  GET /myfile.zip - возвращает тестовый ZIP архив")
    print("  GET /myfile.zip.sha256 - возвращает SHA256 хеш архива")
    print("")
    print("Для остановки сервера нажмите Ctrl+C")
    print("=" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
        httpd.server_close()


if __name__ == '__main__':
    main()
