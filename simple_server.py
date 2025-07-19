#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой тестовый сервер без CORS для локального тестирования
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import tempfile
import zipfile
import hashlib
from pathlib import Path


class SimpleUpdateServer(BaseHTTPRequestHandler):
    """Простой обработчик без CORS"""
    
    def do_GET(self):
        """Обработка GET запросов"""
        # Проверка авторизации
        auth_header = self.headers.get('Authorization')
        if auth_header != 'Bearer test-token-123':
            self.send_response(401)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Unauthorized: Invalid token')
            print(f"❌ Неавторизованный запрос: {auth_header}")
            return
        
        print(f"✅ Авторизованный запрос: {self.path}")
        
        if self.path == '/version.txt':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            # Возвращаем версию 1.0.3 (чтобы было обновление)
            self.wfile.write('1.0.3'.encode('utf-8'))
            print("📄 Отправлена версия: 1.0.3")
            
        elif self.path == '/myfile.zip':
            zip_path = self.create_test_zip()
            if zip_path and os.path.exists(zip_path):
                file_size = os.path.getsize(zip_path)
                self.send_response(200)
                self.send_header('Content-Type', 'application/zip')
                self.send_header('Content-Length', str(file_size))
                self.end_headers()
                
                with open(zip_path, 'rb') as f:
                    while True:
                        chunk = f.read(8192)
                        if not chunk:
                            break
                        self.wfile.write(chunk)
                
                print(f"📦 Отправлен ZIP файл: {zip_path} ({file_size} байт)")
            else:
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Error creating test ZIP file')
                print("❌ Ошибка создания ZIP файла")
                
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
                self.end_headers()
                self.wfile.write(file_hash.encode('utf-8'))
                print(f"🔐 Отправлен хеш: {file_hash[:16]}...")
            else:
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Error creating test ZIP file')
                print("❌ Ошибка создания ZIP файла для хеша")
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Not found: {self.path}'.encode('utf-8'))
            print(f"❌ Не найден: {self.path}")
    
    def create_test_zip(self):
        """Создать тестовый ZIP файл"""
        try:
            # Создаем постоянный ZIP файл в папке проекта
            zip_path = Path(__file__).parent / "test_update.zip"
            
            # Если файл уже существует, возвращаем его
            if zip_path.exists():
                return str(zip_path)
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Добавляем тестовые файлы
                zip_file.writestr('update/app.exe', b'Test executable content for version 1.0.3')
                zip_file.writestr('update/config.ini', 
                                 '[Settings]\nversion=1.0.3\nupdate_date=2025-07-19\n')
                zip_file.writestr('update/data/example.txt', 
                                 'Это тестовый файл обновления.\nВерсия: 1.0.3\nДата: 2025-07-19\n')
                zip_file.writestr('update/readme.txt', 
                                 'Тестовый пакет обновления\nСоздан автоматически для тестирования\nВерсия: 1.0.3')
                zip_file.writestr('update/changelog.txt', 
                                 'Список изменений v1.0.3:\n- Исправлены ошибки\n- Улучшена производительность\n- Добавлены новые функции')
                
                # Добавляем тестовый .reg файл
                reg_content = '''Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\\Software\\PythonUpdater]
"Version"="1.0.3"
"LastUpdate"="2025-07-19"
"TestValue"="Registry updated successfully"

[HKEY_CURRENT_USER\\Software\\PythonUpdater\\Settings]
"AutoUpdate"=dword:00000001
"Theme"="default"
'''
                zip_file.writestr('update/registry_update.reg', reg_content.encode('utf-8'))
            
            print(f"📁 Создан тестовый ZIP: {zip_path}")
            return str(zip_path)
            
        except Exception as e:
            print(f"❌ Ошибка создания ZIP файла: {e}")
            return None
    
    def log_message(self, format, *args):
        """Убираем стандартные логи HTTP сервера"""
        pass


def main():
    """Запуск простого тестового сервера"""
    server_address = ('localhost', 8001)
    httpd = HTTPServer(server_address, SimpleUpdateServer)
    
    print("🚀 " + "=" * 48 + " 🚀")
    print("       ПРОСТОЙ ТЕСТОВЫЙ СЕРВЕР ОБНОВЛЕНИЙ")
    print("🚀 " + "=" * 48 + " 🚀")
    print("")
    print(f"🌐 Сервер запущен на http://localhost:8001")
    print("")
    print("⚙️  Настройки для приложения:")
    print("   📝 Токен: test-token-123")
    print("   📋 URL версии: http://localhost:8001/version.txt")
    print("   📦 URL загрузки: http://localhost:8001/myfile.zip")
    print("   🔐 URL хеша: http://localhost:8001/myfile.zip.sha256")
    print("")
    print("📡 Доступные эндпоинты:")
    print("   📄 GET /version.txt → версия 1.0.3")
    print("   📦 GET /myfile.zip → тестовый ZIP архив")
    print("   🔐 GET /myfile.zip.sha256 → SHA256 хеш")
    print("")
    print("🛑 Для остановки сервера нажмите Ctrl+C")
    print("=" * 56)
    print("")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен")
        httpd.server_close()


if __name__ == '__main__':
    main()
