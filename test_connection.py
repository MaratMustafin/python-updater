#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Быстрый тест соединения с сервером
"""

import requests

def test_server():
    """Тестирование соединения с сервером"""
    base_url = "http://localhost:8001"
    token = "test-token-123"
    headers = {"Authorization": f"Bearer {token}"}
    
    print("🧪 Тестирование соединения с сервером...")
    print("=" * 50)
    
    # Тест 1: Проверка версии
    try:
        print("📋 Тест 1: Получение версии...")
        response = requests.get(f"{base_url}/version.txt", headers=headers, timeout=5)
        print(f"   Статус: {response.status_code}")
        print(f"   Версия: {response.text}")
        print("   ✅ Успешно!")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 2: Загрузка ZIP
    try:
        print("📦 Тест 2: Загрузка ZIP файла...")
        response = requests.get(f"{base_url}/myfile.zip", headers=headers, timeout=10)
        print(f"   Статус: {response.status_code}")
        print(f"   Размер: {len(response.content)} байт")
        print("   ✅ Успешно!")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 3: Получение хеша
    try:
        print("🔐 Тест 3: Получение хеша...")
        response = requests.get(f"{base_url}/myfile.zip.sha256", headers=headers, timeout=5)
        print(f"   Статус: {response.status_code}")
        print(f"   Хеш: {response.text[:32]}...")
        print("   ✅ Успешно!")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    print("=" * 50)
    print("🎯 Тестирование завершено!")

if __name__ == "__main__":
    test_server()
