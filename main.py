#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Updater Application
Приложение для проверки и загрузки обновлений
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
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import appdirs


class Config:
    """Конфигурация приложения"""
    APP_NAME = "PythonUpdater"
    APP_AUTHOR = "YourCompany"
    VERSION = "1.0.0"
    
    # URLs по умолчанию
    DEFAULT_VERSION_URL = "https://example.com/version.txt"
    DEFAULT_DOWNLOAD_URL = "https://example.com/myfile.zip"
    DEFAULT_HASH_URL = "https://example.com/myfile.zip.sha256"


class Translations:
    """Класс для мультиязычности"""
    
    LANGUAGES = {
        'ru': {
            'app_title': 'Менеджер обновлений',
            'tab_update': 'Обновление',
            'tab_settings': 'Настройки',
            'tab_log': 'Журнал',
            'check_update': 'Проверить обновление',
            'current_version': 'Текущая версия:',
            'latest_version': 'Последняя версия:',
            'status': 'Статус:',
            'download_path': 'Путь загрузки:',
            'browse': 'Обзор...',
            'progress': 'Прогресс:',
            'settings_token': 'Токен авторизации:',
            'settings_version_url': 'URL версии:',
            'settings_download_url': 'URL загрузки:',
            'settings_hash_url': 'URL хеша:',
            'settings_auto_check': 'Автопроверка при запуске',
            'settings_dark_theme': 'Тёмная тема',
            'settings_language': 'Язык:',
            'settings_execute_reg': 'Выполнять .reg файлы',
            'save_settings': 'Сохранить настройки',
            'status_up_to_date': 'Файл актуален',
            'status_update_available': 'Доступно обновление',
            'status_downloading': 'Загрузка...',
            'status_downloaded': 'Загружено',
            'status_connection_error': 'Ошибка соединения',
            'status_hash_error': 'Ошибка контрольной суммы',
            'status_extraction_error': 'Ошибка распаковки',
            'error': 'Ошибка',
            'success': 'Успех',
            'settings_saved': 'Настройки сохранены',
            'download_complete': 'Загрузка завершена',
            'select_download_path': 'Выберите путь для загрузки',
        },
        'en': {
            'app_title': 'Update Manager',
            'tab_update': 'Update',
            'tab_settings': 'Settings',
            'tab_log': 'Log',
            'check_update': 'Check Update',
            'current_version': 'Current Version:',
            'latest_version': 'Latest Version:',
            'status': 'Status:',
            'download_path': 'Download Path:',
            'browse': 'Browse...',
            'progress': 'Progress:',
            'settings_token': 'Authorization Token:',
            'settings_version_url': 'Version URL:',
            'settings_download_url': 'Download URL:',
            'settings_hash_url': 'Hash URL:',
            'settings_auto_check': 'Auto-check on startup',
            'settings_dark_theme': 'Dark Theme',
            'settings_language': 'Language:',
            'settings_execute_reg': 'Execute .reg files',
            'save_settings': 'Save Settings',
            'status_up_to_date': 'File is up to date',
            'status_update_available': 'Update available',
            'status_downloading': 'Downloading...',
            'status_downloaded': 'Downloaded',
            'status_connection_error': 'Connection error',
            'status_hash_error': 'Hash verification error',
            'status_extraction_error': 'Extraction error',
            'error': 'Error',
            'success': 'Success',
            'settings_saved': 'Settings saved',
            'download_complete': 'Download complete',
            'select_download_path': 'Select download path',
        }
    }
    
    def __init__(self, language='ru'):
        self.current_language = language
    
    def get(self, key: str) -> str:
        """Получить перевод по ключу"""
        return self.LANGUAGES.get(self.current_language, {}).get(key, key)
    
    def set_language(self, language: str):
        """Установить язык"""
        if language in self.LANGUAGES:
            self.current_language = language


class AppDataManager:
    """Менеджер данных приложения"""
    
    def __init__(self):
        self.app_dir = Path(appdirs.user_data_dir(Config.APP_NAME, Config.APP_AUTHOR))
        self.app_dir.mkdir(parents=True, exist_ok=True)
        
        self.settings_file = self.app_dir / "settings.json"
        self.version_file = self.app_dir / "version.txt"
        self.log_file = self.app_dir / "log.txt"
        
        self._setup_logging()
    
    def _setup_logging(self):
        """Настройка логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    
    def load_settings(self) -> Dict[str, Any]:
        """Загрузить настройки"""
        default_settings = {
            'token': '',
            'version_url': Config.DEFAULT_VERSION_URL,
            'download_url': Config.DEFAULT_DOWNLOAD_URL,
            'hash_url': Config.DEFAULT_HASH_URL,
            'download_path': str(Path.home() / "Downloads"),
            'auto_check': True,
            'dark_theme': False,
            'language': 'ru',
            'execute_reg_files': True  # Новая настройка для выполнения .reg файлов
        }
        
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    # Обновляем настройки по умолчанию загруженными
                    default_settings.update(settings)
            except Exception as e:
                logging.error(f"Ошибка загрузки настроек: {e}")
        
        return default_settings
    
    def save_settings(self, settings: Dict[str, Any]):
        """Сохранить настройки"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            logging.info("Настройки сохранены")
        except Exception as e:
            logging.error(f"Ошибка сохранения настроек: {e}")
            raise
    
    def get_current_version(self) -> str:
        """Получить текущую версию"""
        if self.version_file.exists():
            try:
                return self.version_file.read_text(encoding='utf-8').strip()
            except Exception as e:
                logging.error(f"Ошибка чтения версии: {e}")
        return Config.VERSION
    
    def save_version(self, version: str):
        """Сохранить версию"""
        try:
            self.version_file.write_text(version, encoding='utf-8')
            logging.info(f"Версия обновлена до {version}")
        except Exception as e:
            logging.error(f"Ошибка сохранения версии: {e}")
            raise
    
    def get_log_content(self) -> str:
        """Получить содержимое лога"""
        if self.log_file.exists():
            try:
                return self.log_file.read_text(encoding='utf-8')
            except Exception as e:
                logging.error(f"Ошибка чтения лога: {e}")
                return f"Ошибка чтения лога: {e}"
        return "Лог пуст"


class UpdateChecker:
    """Класс для проверки и загрузки обновлений"""
    
    def __init__(self, settings: Dict[str, Any], progress_callback: Optional[Callable] = None):
        self.settings = settings
        self.progress_callback = progress_callback
        self.session = requests.Session()
        
        # Настройка авторизации
        if settings.get('token'):
            self.session.headers.update({
                'Authorization': f"Bearer {settings['token']}"
            })
    
    def check_version(self) -> tuple[bool, str, str]:
        """
        Проверить версию
        Возвращает: (есть_обновление, текущая_версия, последняя_версия)
        """
        try:
            response = self.session.get(self.settings['version_url'], timeout=10)
            response.raise_for_status()
            
            latest_version = response.text.strip()
            current_version = AppDataManager().get_current_version()
            
            has_update = latest_version != current_version
            logging.info(f"Проверка версии: текущая={current_version}, последняя={latest_version}")
            
            return has_update, current_version, latest_version
            
        except Exception as e:
            logging.error(f"Ошибка проверки версии: {e}")
            raise
    
    def download_file(self, url: str, filepath: Path) -> bool:
        """Загрузить файл с прогрессом"""
        try:
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if self.progress_callback and total_size > 0:
                            progress = int((downloaded / total_size) * 100)
                            self.progress_callback(progress)
            
            logging.info(f"Файл загружен: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Ошибка загрузки файла {url}: {e}")
            raise
    
    def verify_hash(self, filepath: Path, hash_url: str) -> bool:
        """Проверить SHA256 хеш файла"""
        try:
            # Загружаем хеш
            response = self.session.get(hash_url, timeout=10)
            response.raise_for_status()
            expected_hash = response.text.strip().lower()
            
            # Вычисляем хеш файла
            sha256_hash = hashlib.sha256()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            
            actual_hash = sha256_hash.hexdigest().lower()
            
            is_valid = expected_hash == actual_hash
            logging.info(f"Проверка хеша: ожидаемый={expected_hash}, фактический={actual_hash}, валидный={is_valid}")
            
            return is_valid
            
        except Exception as e:
            logging.error(f"Ошибка проверки хеша: {e}")
            raise
    
    def extract_archive(self, archive_path: Path, extract_path: Path) -> bool:
        """Распаковать архив"""
        try:
            extract_path.mkdir(parents=True, exist_ok=True)
            
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            
            logging.info(f"Архив распакован в: {extract_path}")
            return True
            
        except Exception as e:
            logging.error(f"Ошибка распаковки архива: {e}")
            raise
    
    def execute_reg_files(self, extract_path: Path) -> bool:
        """Выполнить .reg файлы из распакованного архива"""
        import subprocess
        import sys
        
        # Проверяем настройку выполнения .reg файлов
        if not self.settings.get('execute_reg_files', True):
            logging.info("Выполнение REG файлов отключено в настройках")
            return True
        
        try:
            # Ищем все .reg файлы в распакованной папке
            reg_files = list(extract_path.rglob("*.reg"))
            
            if not reg_files:
                logging.info("REG файлы не найдены")
                return True
            
            logging.info(f"Найдено REG файлов: {len(reg_files)}")
            
            # Выполняем каждый .reg файл
            for reg_file in reg_files:
                try:
                    logging.info(f"Выполнение REG файла: {reg_file}")
                    
                    if sys.platform == "win32":
                        # Windows: используем regedit
                        result = subprocess.run([
                            "regedit", "/s", str(reg_file)
                        ], capture_output=True, text=True, timeout=30)
                        
                        if result.returncode == 0:
                            logging.info(f"REG файл успешно выполнен: {reg_file.name}")
                        else:
                            logging.error(f"Ошибка выполнения REG файла {reg_file.name}: {result.stderr}")
                            return False
                    else:
                        # На macOS/Linux .reg файлы не поддерживаются
                        logging.warning(f"REG файлы не поддерживаются на {sys.platform}: {reg_file.name}")
                        
                except subprocess.TimeoutExpired:
                    logging.error(f"Таймаут выполнения REG файла: {reg_file.name}")
                    return False
                except Exception as e:
                    logging.error(f"Ошибка выполнения REG файла {reg_file.name}: {e}")
                    return False
            
            return True
            
        except Exception as e:
            logging.error(f"Ошибка обработки REG файлов: {e}")
            return False
    
    def download_update(self, download_path: str, version: str) -> bool:
        """Загрузить и установить обновление"""
        try:
            download_dir = Path(download_path)
            archive_path = download_dir / "myfile.zip"
            
            # Загружаем архив
            if self.progress_callback:
                self.progress_callback(0)
            
            self.download_file(self.settings['download_url'], archive_path)
            
            # Проверяем хеш
            if not self.verify_hash(archive_path, self.settings['hash_url']):
                archive_path.unlink()
                return False
            
            # Распаковываем
            extract_path = download_dir / "update"
            if not self.extract_archive(archive_path, extract_path):
                return False
            
            # Выполняем .reg файлы, если они есть
            if not self.execute_reg_files(extract_path):
                logging.warning("Некоторые REG файлы не были выполнены, но обновление продолжается")
            
            # Обновляем версию
            AppDataManager().save_version(version)
            
            # Удаляем архив
            archive_path.unlink()
            
            if self.progress_callback:
                self.progress_callback(100)
            
            logging.info(f"Обновление успешно загружено и установлено: версия {version}")
            return True
            
        except Exception as e:
            logging.error(f"Ошибка загрузки обновления: {e}")
            raise


class UpdaterApp:
    """Главное приложение"""
    
    def __init__(self):
        self.data_manager = AppDataManager()
        self.settings = self.data_manager.load_settings()
        self.translations = Translations(self.settings.get('language', 'ru'))
        
        self.root = tk.Tk()
        self.root.title(self.translations.get('app_title'))
        self.root.geometry("600x500")
        
        # Переменные для интерфейса
        self.current_version_var = tk.StringVar(value=self.data_manager.get_current_version())
        self.latest_version_var = tk.StringVar(value="Неизвестно")
        self.status_var = tk.StringVar(value=self.translations.get('status_up_to_date'))
        self.download_path_var = tk.StringVar(value=self.settings['download_path'])
        self.progress_var = tk.IntVar()
        
        # Настройки UI
        self.token_var = tk.StringVar(value=self.settings.get('token', ''))
        self.version_url_var = tk.StringVar(value=self.settings.get('version_url', ''))
        self.download_url_var = tk.StringVar(value=self.settings.get('download_url', ''))
        self.hash_url_var = tk.StringVar(value=self.settings.get('hash_url', ''))
        self.auto_check_var = tk.BooleanVar(value=self.settings.get('auto_check', True))
        self.dark_theme_var = tk.BooleanVar(value=self.settings.get('dark_theme', False))
        self.language_var = tk.StringVar(value=self.settings.get('language', 'ru'))
        self.execute_reg_var = tk.BooleanVar(value=self.settings.get('execute_reg_files', True))
        
        self.setup_ui()
        self.apply_theme()
        
        # Автопроверка при запуске
        if self.settings.get('auto_check', True):
            self.root.after(1000, self.check_update_async)
    
    def setup_ui(self):
        """Создание интерфейса"""
        # Создаем notebook для вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка "Обновление"
        self.update_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.update_frame, text=self.translations.get('tab_update'))
        self.setup_update_tab()
        
        # Вкладка "Настройки"
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text=self.translations.get('tab_settings'))
        self.setup_settings_tab()
        
        # Вкладка "Журнал"
        self.log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.log_frame, text=self.translations.get('tab_log'))
        self.setup_log_tab()
    
    def setup_update_tab(self):
        """Настройка вкладки обновления"""
        # Информация о версии
        version_frame = ttk.LabelFrame(self.update_frame, text="Информация о версии")
        version_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(version_frame, text=self.translations.get('current_version')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(version_frame, textvariable=self.current_version_var).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(version_frame, text=self.translations.get('latest_version')).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(version_frame, textvariable=self.latest_version_var).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(version_frame, text=self.translations.get('status')).grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.status_label = ttk.Label(version_frame, textvariable=self.status_var)
        self.status_label.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Кнопка проверки обновлений
        self.check_button = ttk.Button(self.update_frame, text=self.translations.get('check_update'), 
                                      command=self.check_update_async)
        self.check_button.pack(pady=10)
        
        # Путь загрузки
        path_frame = ttk.LabelFrame(self.update_frame, text=self.translations.get('download_path'))
        path_frame.pack(fill=tk.X, padx=10, pady=5)
        
        path_entry_frame = ttk.Frame(path_frame)
        path_entry_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.path_entry = ttk.Entry(path_entry_frame, textvariable=self.download_path_var)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(path_entry_frame, text=self.translations.get('browse'), 
                  command=self.browse_download_path).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Прогресс
        progress_frame = ttk.LabelFrame(self.update_frame, text=self.translations.get('progress'))
        progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="0%")
        self.progress_label.pack(pady=2)
    
    def setup_settings_tab(self):
        """Настройка вкладки настроек"""
        # Создаем прокручиваемый фрейм
        canvas = tk.Canvas(self.settings_frame)
        scrollbar = ttk.Scrollbar(self.settings_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # API настройки
        api_frame = ttk.LabelFrame(scrollable_frame, text="API Настройки")
        api_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(api_frame, text=self.translations.get('settings_token')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        token_entry = ttk.Entry(api_frame, textvariable=self.token_var, show="*", width=50)
        token_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(api_frame, text=self.translations.get('settings_version_url')).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(api_frame, textvariable=self.version_url_var, width=50).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(api_frame, text=self.translations.get('settings_download_url')).grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(api_frame, textvariable=self.download_url_var, width=50).grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(api_frame, text=self.translations.get('settings_hash_url')).grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(api_frame, textvariable=self.hash_url_var, width=50).grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Общие настройки
        general_frame = ttk.LabelFrame(scrollable_frame, text="Общие настройки")
        general_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Checkbutton(general_frame, text=self.translations.get('settings_auto_check'), 
                       variable=self.auto_check_var).pack(anchor=tk.W, padx=5, pady=2)
        
        ttk.Checkbutton(general_frame, text=self.translations.get('settings_dark_theme'), 
                       variable=self.dark_theme_var, command=self.toggle_theme).pack(anchor=tk.W, padx=5, pady=2)
        
        ttk.Checkbutton(general_frame, text=self.translations.get('settings_execute_reg'), 
                       variable=self.execute_reg_var).pack(anchor=tk.W, padx=5, pady=2)
        
        # Язык
        lang_frame = ttk.Frame(general_frame)
        lang_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(lang_frame, text=self.translations.get('settings_language')).pack(side=tk.LEFT)
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.language_var, 
                                 values=['ru', 'en'], state="readonly", width=10)
        lang_combo.pack(side=tk.LEFT, padx=(5, 0))
        lang_combo.bind('<<ComboboxSelected>>', self.change_language)
        
        # Кнопка сохранения
        ttk.Button(scrollable_frame, text=self.translations.get('save_settings'), 
                  command=self.save_settings).pack(pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_log_tab(self):
        """Настройка вкладки журнала"""
        # Текстовое поле для лога
        text_frame = ttk.Frame(self.log_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.log_text = tk.Text(text_frame, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar_log = ttk.Scrollbar(text_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar_log.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_log.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопка обновления лога
        ttk.Button(self.log_frame, text="Обновить журнал", command=self.refresh_log).pack(pady=5)
        
        # Загружаем лог при запуске
        self.refresh_log()
    
    def apply_theme(self):
        """Применить тему"""
        if self.dark_theme_var.get():
            # Тёмная тема (упрощенная реализация)
            style = ttk.Style()
            style.theme_use('clam')  # Используем тему, которая поддерживает настройку цветов
            
            # Настройка цветов для тёмной темы
            style.configure('TLabel', background='#2b2b2b', foreground='white')
            style.configure('TFrame', background='#2b2b2b')
            style.configure('TLabelFrame', background='#2b2b2b', foreground='white')
            style.configure('TNotebook', background='#2b2b2b')
            style.configure('TNotebook.Tab', background='#404040', foreground='white')
            
            self.root.configure(bg='#2b2b2b')
        else:
            # Светлая тема
            style = ttk.Style()
            style.theme_use('winnative' if sys.platform == 'win32' else 'default')
            self.root.configure(bg='SystemButtonFace')
    
    def toggle_theme(self):
        """Переключить тему"""
        self.apply_theme()
    
    def change_language(self, event=None):
        """Изменить язык"""
        new_language = self.language_var.get()
        self.translations.set_language(new_language)
        # Здесь должно быть обновление всех текстов в интерфейсе
        # Для простоты показываем сообщение о необходимости перезапуска
        messagebox.showinfo("Информация", "Для применения языка перезапустите приложение")
    
    def browse_download_path(self):
        """Выбрать путь загрузки"""
        path = filedialog.askdirectory(title=self.translations.get('select_download_path'))
        if path:
            self.download_path_var.set(path)
    
    def save_settings(self):
        """Сохранить настройки"""
        try:
            settings = {
                'token': self.token_var.get(),
                'version_url': self.version_url_var.get(),
                'download_url': self.download_url_var.get(),
                'hash_url': self.hash_url_var.get(),
                'download_path': self.download_path_var.get(),
                'auto_check': self.auto_check_var.get(),
                'dark_theme': self.dark_theme_var.get(),
                'language': self.language_var.get(),
                'execute_reg_files': self.execute_reg_var.get()
            }
            
            self.data_manager.save_settings(settings)
            self.settings = settings
            
            messagebox.showinfo(self.translations.get('success'), 
                               self.translations.get('settings_saved'))
            
        except Exception as e:
            messagebox.showerror(self.translations.get('error'), str(e))
    
    def refresh_log(self):
        """Обновить содержимое журнала"""
        try:
            log_content = self.data_manager.get_log_content()
            
            self.log_text.configure(state=tk.NORMAL)
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, log_content)
            self.log_text.configure(state=tk.DISABLED)
            
            # Прокрутка в конец
            self.log_text.see(tk.END)
            
        except Exception as e:
            logging.error(f"Ошибка обновления лога: {e}")
    
    def update_progress(self, progress: int):
        """Обновить прогресс"""
        self.progress_var.set(progress)
        self.progress_label.configure(text=f"{progress}%")
        self.root.update_idletasks()
    
    def check_update_async(self):
        """Асинхронная проверка обновлений"""
        def check_update_thread():
            try:
                self.check_button.configure(state=tk.DISABLED)
                self.status_var.set("Проверка обновлений...")
                
                checker = UpdateChecker(self.settings, self.update_progress)
                has_update, current_version, latest_version = checker.check_version()
                
                self.current_version_var.set(current_version)
                self.latest_version_var.set(latest_version)
                
                if has_update:
                    self.status_var.set(self.translations.get('status_update_available'))
                    # Запускаем загрузку
                    self.download_update_async(checker, latest_version)
                else:
                    self.status_var.set(self.translations.get('status_up_to_date'))
                    
            except Exception as e:
                self.status_var.set(self.translations.get('status_connection_error'))
                logging.error(f"Ошибка проверки обновлений: {e}")
            finally:
                self.check_button.configure(state=tk.NORMAL)
        
        thread = threading.Thread(target=check_update_thread, daemon=True)
        thread.start()
    
    def download_update_async(self, checker: UpdateChecker, version: str):
        """Асинхронная загрузка обновления"""
        def download_thread():
            try:
                self.status_var.set(self.translations.get('status_downloading'))
                
                success = checker.download_update(self.download_path_var.get(), version)
                
                if success:
                    self.status_var.set(self.translations.get('status_downloaded'))
                    self.current_version_var.set(version)
                    messagebox.showinfo(self.translations.get('success'), 
                                       self.translations.get('download_complete'))
                    self.refresh_log()  # Обновляем лог
                else:
                    self.status_var.set(self.translations.get('status_hash_error'))
                    
            except Exception as e:
                if "hash" in str(e).lower():
                    self.status_var.set(self.translations.get('status_hash_error'))
                elif "extract" in str(e).lower():
                    self.status_var.set(self.translations.get('status_extraction_error'))
                else:
                    self.status_var.set(self.translations.get('status_connection_error'))
                
                logging.error(f"Ошибка загрузки обновления: {e}")
        
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
    
    def run(self):
        """Запустить приложение"""
        self.root.mainloop()


def main():
    """Главная функция"""
    app = UpdaterApp()
    app.run()


if __name__ == "__main__":
    main()
