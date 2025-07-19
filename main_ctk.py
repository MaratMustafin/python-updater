#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Updater Application with CustomTkinter
Приложение для проверки и загрузки обновлений с современным интерфейсом CustomTkinter
"""

import sys
import os
import json
import hashlib
import zipfile
import threading
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Callable
import requests
import appdirs

try:
    import customtkinter as ctk
    from tkinter import messagebox, filedialog
    CUSTOMTKINTER_AVAILABLE = True
except ImportError:
    CUSTOMTKINTER_AVAILABLE = False

# Импортируем классы из основного модуля
from main import Config, Translations, AppDataManager, UpdateChecker


class UpdaterAppCTK:
    """Главное приложение с CustomTkinter интерфейсом"""
    
    def __init__(self):
        if not CUSTOMTKINTER_AVAILABLE:
            raise ImportError("CustomTkinter не установлен. Используйте pip install customtkinter")
        
        # Настройка CustomTkinter
        ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
        ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
        
        self.data_manager = AppDataManager()
        self.settings = self.data_manager.load_settings()
        self.translations = Translations(self.settings.get('language', 'ru'))
        
        # Переменные состояния
        self.current_version = self.data_manager.get_current_version()
        self.latest_version = "Неизвестно"
        self.status = self.translations.get('status_up_to_date')
        self.progress_value = 0
        
        # Создание главного окна
        self.root = ctk.CTk()
        self.root.title(self.translations.get('app_title'))
        self.root.geometry("800x700")
        
        # Настройка темы из настроек
        if self.settings.get('dark_theme', False):
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
        
        self.setup_ui()
        
        # Автопроверка при запуске
        if self.settings.get('auto_check', True):
            self.root.after(1000, self.check_update_async)
    
    def setup_ui(self):
        """Создание интерфейса CustomTkinter"""
        # Создаем главный контейнер
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Заголовок приложения
        title_label = ctk.CTkLabel(
            main_frame, 
            text=self.translations.get('app_title'),
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Создаем вкладки
        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.pack(fill="both", expand=True)
        
        # Добавляем вкладки
        self.tab_update = self.tabview.add(self.translations.get('tab_update'))
        self.tab_settings = self.tabview.add(self.translations.get('tab_settings'))
        self.tab_log = self.tabview.add(self.translations.get('tab_log'))
        
        # Настройка вкладок
        self.setup_update_tab()
        self.setup_settings_tab()
        self.setup_log_tab()
    
    def setup_update_tab(self):
        """Настройка вкладки обновления"""
        # Информация о версии
        version_frame = ctk.CTkFrame(self.tab_update)
        version_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        version_title = ctk.CTkLabel(
            version_frame, 
            text="Информация о версии",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        version_title.pack(pady=(15, 10))
        
        # Текущая версия
        self.current_version_label = ctk.CTkLabel(
            version_frame,
            text=f"{self.translations.get('current_version')} {self.current_version}",
            font=ctk.CTkFont(size=14)
        )
        self.current_version_label.pack(pady=5)
        
        # Последняя версия
        self.latest_version_label = ctk.CTkLabel(
            version_frame,
            text=f"{self.translations.get('latest_version')} {self.latest_version}",
            font=ctk.CTkFont(size=14)
        )
        self.latest_version_label.pack(pady=5)
        
        # Статус
        self.status_label = ctk.CTkLabel(
            version_frame,
            text=f"{self.translations.get('status')} {self.status}",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(pady=(5, 15))
        
        # Кнопка проверки обновлений
        self.check_button = ctk.CTkButton(
            self.tab_update,
            text=self.translations.get('check_update'),
            command=self.check_update_async,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=200
        )
        self.check_button.pack(pady=20)
        
        # Путь загрузки
        path_frame = ctk.CTkFrame(self.tab_update)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        path_title = ctk.CTkLabel(
            path_frame,
            text=self.translations.get('download_path'),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        path_title.pack(pady=(15, 10))
        
        path_input_frame = ctk.CTkFrame(path_frame)
        path_input_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.path_entry = ctk.CTkEntry(
            path_input_frame,
            placeholder_text="Выберите папку для загрузки",
            font=ctk.CTkFont(size=12),
            height=35
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        self.path_entry.insert(0, self.settings['download_path'])
        
        browse_button = ctk.CTkButton(
            path_input_frame,
            text=self.translations.get('browse'),
            command=self.browse_download_path,
            width=100,
            height=35
        )
        browse_button.pack(side="right", padx=(5, 10), pady=10)
        
        # Прогресс
        progress_frame = ctk.CTkFrame(self.tab_update)
        progress_frame.pack(fill="x", padx=20, pady=10)
        
        progress_title = ctk.CTkLabel(
            progress_frame,
            text=self.translations.get('progress'),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        progress_title.pack(pady=(15, 10))
        
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            width=400,
            height=20
        )
        self.progress_bar.pack(pady=(0, 10), padx=15)
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="0%",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.pack(pady=(0, 15))
    
    def setup_settings_tab(self):
        """Настройка вкладки настроек"""
        # Создаем прокручиваемый фрейм
        scrollable_frame = ctk.CTkScrollableFrame(self.tab_settings)
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # API настройки
        api_frame = ctk.CTkFrame(scrollable_frame)
        api_frame.pack(fill="x", pady=(0, 20))
        
        api_title = ctk.CTkLabel(
            api_frame,
            text="API Настройки",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        api_title.pack(pady=(15, 20))
        
        # Токен
        token_label = ctk.CTkLabel(api_frame, text=self.translations.get('settings_token'))
        token_label.pack(pady=(0, 5))
        
        self.token_entry = ctk.CTkEntry(
            api_frame,
            placeholder_text="Введите токен авторизации",
            show="*",
            width=500,
            height=35
        )
        self.token_entry.pack(pady=(0, 15), padx=15)
        self.token_entry.insert(0, self.settings.get('token', ''))
        
        # URL версии
        version_url_label = ctk.CTkLabel(api_frame, text=self.translations.get('settings_version_url'))
        version_url_label.pack(pady=(0, 5))
        
        self.version_url_entry = ctk.CTkEntry(
            api_frame,
            placeholder_text="http://localhost:8001/version.txt",
            width=500,
            height=35
        )
        self.version_url_entry.pack(pady=(0, 15), padx=15)
        self.version_url_entry.insert(0, self.settings.get('version_url', ''))
        
        # URL загрузки
        download_url_label = ctk.CTkLabel(api_frame, text=self.translations.get('settings_download_url'))
        download_url_label.pack(pady=(0, 5))
        
        self.download_url_entry = ctk.CTkEntry(
            api_frame,
            placeholder_text="http://localhost:8001/myfile.zip",
            width=500,
            height=35
        )
        self.download_url_entry.pack(pady=(0, 15), padx=15)
        self.download_url_entry.insert(0, self.settings.get('download_url', ''))
        
        # URL хеша
        hash_url_label = ctk.CTkLabel(api_frame, text=self.translations.get('settings_hash_url'))
        hash_url_label.pack(pady=(0, 5))
        
        self.hash_url_entry = ctk.CTkEntry(
            api_frame,
            placeholder_text="http://localhost:8001/myfile.zip.sha256",
            width=500,
            height=35
        )
        self.hash_url_entry.pack(pady=(0, 20), padx=15)
        self.hash_url_entry.insert(0, self.settings.get('hash_url', ''))
        
        # Общие настройки
        general_frame = ctk.CTkFrame(scrollable_frame)
        general_frame.pack(fill="x", pady=(0, 20))
        
        general_title = ctk.CTkLabel(
            general_frame,
            text="Общие настройки",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        general_title.pack(pady=(15, 20))
        
        # Автопроверка
        self.auto_check_var = ctk.BooleanVar(value=self.settings.get('auto_check', True))
        auto_check_checkbox = ctk.CTkCheckBox(
            general_frame,
            text=self.translations.get('settings_auto_check'),
            variable=self.auto_check_var,
            font=ctk.CTkFont(size=14)
        )
        auto_check_checkbox.pack(pady=10, padx=15, anchor="w")
        
        # Тёмная тема
        self.dark_theme_var = ctk.BooleanVar(value=self.settings.get('dark_theme', False))
        dark_theme_checkbox = ctk.CTkCheckBox(
            general_frame,
            text=self.translations.get('settings_dark_theme'),
            variable=self.dark_theme_var,
            command=self.toggle_theme,
            font=ctk.CTkFont(size=14)
        )
        dark_theme_checkbox.pack(pady=10, padx=15, anchor="w")
        
        # Выполнение .reg файлов
        self.execute_reg_var = ctk.BooleanVar(value=self.settings.get('execute_reg_files', True))
        execute_reg_checkbox = ctk.CTkCheckBox(
            general_frame,
            text=self.translations.get('settings_execute_reg'),
            variable=self.execute_reg_var,
            font=ctk.CTkFont(size=14)
        )
        execute_reg_checkbox.pack(pady=10, padx=15, anchor="w")
        
        # Язык
        language_label = ctk.CTkLabel(general_frame, text=self.translations.get('settings_language'))
        language_label.pack(pady=(15, 5), padx=15, anchor="w")
        
        self.language_combo = ctk.CTkComboBox(
            general_frame,
            values=['ru', 'en'],
            width=150,
            height=35,
            command=self.change_language
        )
        self.language_combo.pack(pady=(0, 20), padx=15, anchor="w")
        self.language_combo.set(self.settings.get('language', 'ru'))
        
        # Кнопка сохранения
        save_button = ctk.CTkButton(
            scrollable_frame,
            text=self.translations.get('save_settings'),
            command=self.save_settings,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40,
            width=200
        )
        save_button.pack(pady=20)
    
    def setup_log_tab(self):
        """Настройка вкладки журнала"""
        # Заголовок
        log_title = ctk.CTkLabel(
            self.tab_log,
            text="Журнал операций",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        log_title.pack(pady=(20, 10))
        
        # Кнопка обновления
        refresh_button = ctk.CTkButton(
            self.tab_log,
            text="Обновить журнал",
            command=self.refresh_log,
            width=150,
            height=35
        )
        refresh_button.pack(pady=(0, 15))
        
        # Текстовое поле для лога
        self.log_textbox = ctk.CTkTextbox(
            self.tab_log,
            width=700,
            height=400,
            font=ctk.CTkFont(family="Consolas", size=11),
            wrap="word"
        )
        self.log_textbox.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Загружаем лог
        self.refresh_log()
    
    def toggle_theme(self):
        """Переключить тему"""
        if self.dark_theme_var.get():
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
    
    def change_language(self, choice):
        """Изменить язык"""
        self.translations.set_language(choice)
        messagebox.showinfo("Информация", "Для применения языка перезапустите приложение")
    
    def browse_download_path(self):
        """Выбрать путь загрузки"""
        path = filedialog.askdirectory(title=self.translations.get('select_download_path'))
        if path:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, path)
    
    def save_settings(self):
        """Сохранить настройки"""
        try:
            settings = {
                'token': self.token_entry.get(),
                'version_url': self.version_url_entry.get(),
                'download_url': self.download_url_entry.get(),
                'hash_url': self.hash_url_entry.get(),
                'download_path': self.path_entry.get(),
                'auto_check': self.auto_check_var.get(),
                'dark_theme': self.dark_theme_var.get(),
                'language': self.language_combo.get(),
                'execute_reg_files': self.execute_reg_var.get()
            }
            
            self.data_manager.save_settings(settings)
            self.settings = settings
            
            messagebox.showinfo(
                self.translations.get('success'), 
                self.translations.get('settings_saved')
            )
            
        except Exception as e:
            messagebox.showerror(self.translations.get('error'), str(e))
    
    def refresh_log(self):
        """Обновить содержимое журнала"""
        try:
            log_content = self.data_manager.get_log_content()
            
            self.log_textbox.delete("1.0", "end")
            self.log_textbox.insert("1.0", log_content)
            
            # Прокрутка в конец
            self.log_textbox.see("end")
            
        except Exception as e:
            logging.error(f"Ошибка обновления лога: {e}")
    
    def update_progress(self, progress: int):
        """Обновить прогресс"""
        self.progress_value = progress
        self.progress_bar.set(progress / 100.0)
        self.progress_label.configure(text=f"{progress}%")
        self.root.update_idletasks()
    
    def update_status(self, status: str):
        """Обновить статус"""
        self.status = status
        self.status_label.configure(text=f"{self.translations.get('status')} {status}")
    
    def update_versions(self, current: str, latest: str):
        """Обновить информацию о версиях"""
        self.current_version = current
        self.latest_version = latest
        
        self.current_version_label.configure(
            text=f"{self.translations.get('current_version')} {current}"
        )
        self.latest_version_label.configure(
            text=f"{self.translations.get('latest_version')} {latest}"
        )
    
    def check_update_async(self):
        """Асинхронная проверка обновлений"""
        def check_update_thread():
            try:
                self.check_button.configure(state="disabled")
                self.update_status("Проверка обновлений...")
                
                checker = UpdateChecker(self.settings, self.update_progress)
                has_update, current_version, latest_version = checker.check_version()
                
                self.update_versions(current_version, latest_version)
                
                if has_update:
                    self.update_status(self.translations.get('status_update_available'))
                    # Запускаем загрузку
                    self.download_update_async(checker, latest_version)
                else:
                    self.update_status(self.translations.get('status_up_to_date'))
                    
            except Exception as e:
                self.update_status(self.translations.get('status_connection_error'))
                logging.error(f"Ошибка проверки обновлений: {e}")
            finally:
                self.check_button.configure(state="normal")
        
        thread = threading.Thread(target=check_update_thread, daemon=True)
        thread.start()
    
    def download_update_async(self, checker: UpdateChecker, version: str):
        """Асинхронная загрузка обновления"""
        def download_thread():
            try:
                self.update_status(self.translations.get('status_downloading'))
                
                download_path = self.path_entry.get()
                success = checker.download_update(download_path, version)
                
                if success:
                    self.update_status(self.translations.get('status_downloaded'))
                    self.current_version = version
                    self.current_version_label.configure(
                        text=f"{self.translations.get('current_version')} {version}"
                    )
                    
                    messagebox.showinfo(
                        self.translations.get('success'),
                        self.translations.get('download_complete')
                    )
                    self.refresh_log()  # Обновляем лог
                else:
                    self.update_status(self.translations.get('status_hash_error'))
                    
            except Exception as e:
                if "hash" in str(e).lower():
                    self.update_status(self.translations.get('status_hash_error'))
                elif "extract" in str(e).lower():
                    self.update_status(self.translations.get('status_extraction_error'))
                else:
                    self.update_status(self.translations.get('status_connection_error'))
                
                logging.error(f"Ошибка загрузки обновления: {e}")
        
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
    
    def run(self):
        """Запустить приложение"""
        self.root.mainloop()


def main_ctk():
    """Главная функция для CustomTkinter"""
    try:
        app = UpdaterAppCTK()
        app.run()
    except ImportError as e:
        print(f"Ошибка: {e}")
        print("Установите CustomTkinter: pip install customtkinter")
        sys.exit(1)


if __name__ == "__main__":
    # Выбираем интерфейс в зависимости от аргументов командной строки
    if len(sys.argv) > 1 and sys.argv[1] == "--ctk":
        main_ctk()
    else:
        # Используем tkinter по умолчанию
        from main import main
        main()
