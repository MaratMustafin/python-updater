#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Лаунчер для выбора версии интерфейса Python Updater
"""

import subprocess
import sys
from pathlib import Path

def check_dependencies():
    """Проверка установленных зависимостей"""
    dependencies = {
        'tkinter': True,  # Встроен в Python
        'customtkinter': False,
        'dearpygui': False
    }
    
    try:
        import customtkinter
        dependencies['customtkinter'] = True
    except ImportError:
        pass
    
    try:
        import dearpygui
        dependencies['dearpygui'] = True
    except ImportError:
        pass
    
    return dependencies

def main():
    """Главная функция лаунчера"""
    print("🚀 " + "=" * 50 + " 🚀")
    print("      PYTHON UPDATER - ВЫБОР ИНТЕРФЕЙСА")
    print("🚀 " + "=" * 50 + " 🚀")
    print()
    
    # Проверяем зависимости
    deps = check_dependencies()
    
    print("📋 Доступные версии интерфейса:")
    print()
    
    options = []
    
    # Tkinter (всегда доступен)
    print("1. 🔶 Tkinter (Классический)")
    print("   ✅ Готов к использованию")
    options.append(('tkinter', 'python main.py'))
    
    # CustomTkinter
    if deps['customtkinter']:
        print("2. 🔷 CustomTkinter (Современный) ⭐ Рекомендуется")
        print("   ✅ Готов к использованию")
        options.append(('customtkinter', 'python main_ctk.py --ctk'))
    else:
        print("2. 🔷 CustomTkinter (Современный)")
        print("   ❌ Не установлен (pip install customtkinter)")
    
    # DearPyGui
    if deps['dearpygui']:
        print("3. 🔵 DearPyGui (Игровой)")
        print("   ✅ Готов к использованию")
        options.append(('dearpygui', 'python main_dpg.py --dpg'))
    else:
        print("3. 🔵 DearPyGui (Игровой)")
        print("   ❌ Не установлен (pip install dearpygui)")
    
    print()
    print("4. 🧪 Запустить тестовый сервер")
    print("5. 🔧 Установить все зависимости")
    print("0. ❌ Выход")
    print()
    
    try:
        choice = input("Выберите опцию (0-5): ").strip()
        
        if choice == "0":
            print("👋 До свидания!")
            return
        
        elif choice == "1" and len(options) >= 1:
            print(f"🚀 Запуск {options[0][0]}...")
            subprocess.run(options[0][1], shell=True)
        
        elif choice == "2":
            if deps['customtkinter'] and len(options) >= 2:
                print(f"🚀 Запуск CustomTkinter...")
                subprocess.run('python main_ctk.py --ctk', shell=True)
            else:
                print("❌ CustomTkinter не установлен!")
                print("Выполните: pip install customtkinter")
        
        elif choice == "3":
            if deps['dearpygui']:
                print(f"🚀 Запуск DearPyGui...")
                subprocess.run('python main_dpg.py --dpg', shell=True)
            else:
                print("❌ DearPyGui не установлен!")
                print("Выполните: pip install dearpygui")
        
        elif choice == "4":
            print("🧪 Запуск тестового сервера...")
            subprocess.run('python simple_server.py', shell=True)
        
        elif choice == "5":
            print("🔧 Установка всех зависимостей...")
            subprocess.run('pip install -r requirements.txt', shell=True)
            print("✅ Готово! Запустите лаунчер снова.")
        
        else:
            print("❌ Неверный выбор!")
    
    except KeyboardInterrupt:
        print("\n👋 До свидания!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
