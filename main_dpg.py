#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Updater Application with DearPyGui
Приложение для проверки и загрузки обновлений с DearPyGui интерфейсом
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
    import dearpygui.dearpygui as dpg
    DEARPYGUI_AVAILABLE = True
except ImportError:
    DEARPYGUI_AVAILABLE = False

# Импортируем классы из основного модуля
from main import Config, Translations, AppDataManager, UpdateChecker


class UpdaterAppDPG:
    """Главное приложение с DearPyGui интерфейсом"""
    
    def __init__(self):
        if not DEARPYGUI_AVAILABLE:
            raise ImportError("DearPyGui не установлен. Используйте pip install dearpygui")
        
        self.data_manager = AppDataManager()
        self.settings = self.data_manager.load_settings()
        self.translations = Translations(self.settings.get('language', 'ru'))
        
        # Переменные состояния
        self.current_version = self.data_manager.get_current_version()
        self.latest_version = "Неизвестно"
        self.status = self.translations.get('status_up_to_date')
        self.progress = 0
        
        # Инициализация DearPyGui
        dpg.create_context()
        
        self.setup_ui()
        
        # Автопроверка при запуске
        if self.settings.get('auto_check', True):
            threading.Timer(1.0, self.check_update_async).start()
    
    def setup_ui(self):
        """Создание интерфейса DearPyGui"""
        # Главное окно
        with dpg.window(label=self.translations.get('app_title'), tag="main_window"):
            
            # Вкладки
            with dpg.tab_bar():
                
                # Вкладка обновления
                with dpg.tab(label=self.translations.get('tab_update')):
                    self.setup_update_tab_dpg()
                
                # Вкладка настроек
                with dpg.tab(label=self.translations.get('tab_settings')):
                    self.setup_settings_tab_dpg()
                
                # Вкладка журнала
                with dpg.tab(label=self.translations.get('tab_log')):
                    self.setup_log_tab_dpg()
        
        # Настройка темы
        self.setup_theme()
    
    def setup_update_tab_dpg(self):
        """Настройка вкладки обновления для DearPyGui"""
        with dpg.group():
            # Информация о версии
            with dpg.group():
                dpg.add_text(f"{self.translations.get('current_version')} {self.current_version}", tag="current_version_text")
                dpg.add_text(f"{self.translations.get('latest_version')} {self.latest_version}", tag="latest_version_text")
                dpg.add_text(f"{self.translations.get('status')} {self.status}", tag="status_text")
            
            dpg.add_separator()
            
            # Кнопка проверки
            dpg.add_button(label=self.translations.get('check_update'), 
                          callback=self.check_update_async, tag="check_button")
            
            dpg.add_separator()
            
            # Путь загрузки
            dpg.add_text(self.translations.get('download_path'))
            with dpg.group(horizontal=True):
                dpg.add_input_text(tag="download_path_input", 
                                  default_value=self.settings['download_path'], 
                                  width=400)
                dpg.add_button(label=self.translations.get('browse'), 
                              callback=self.browse_download_path_dpg)
            
            dpg.add_separator()
            
            # Прогресс
            dpg.add_text(self.translations.get('progress'))
            dpg.add_progress_bar(tag="progress_bar", default_value=0.0)
            dpg.add_text("0%", tag="progress_text")
    
    def setup_settings_tab_dpg(self):
        """Настройка вкладки настроек для DearPyGui"""
        with dpg.group():
            # API настройки
            dpg.add_text("API Настройки")
            dpg.add_separator()
            
            dpg.add_text(self.translations.get('settings_token'))
            dpg.add_input_text(tag="token_input", 
                              default_value=self.settings.get('token', ''), 
                              password=True, width=400)
            
            dpg.add_text(self.translations.get('settings_version_url'))
            dpg.add_input_text(tag="version_url_input", 
                              default_value=self.settings.get('version_url', ''), 
                              width=400)
            
            dpg.add_text(self.translations.get('settings_download_url'))
            dpg.add_input_text(tag="download_url_input", 
                              default_value=self.settings.get('download_url', ''), 
                              width=400)
            
            dpg.add_text(self.translations.get('settings_hash_url'))
            dpg.add_input_text(tag="hash_url_input", 
                              default_value=self.settings.get('hash_url', ''), 
                              width=400)
            
            dpg.add_separator()
            
            # Общие настройки
            dpg.add_text("Общие настройки")
            dpg.add_separator()
            
            dpg.add_checkbox(label=self.translations.get('settings_auto_check'), 
                           tag="auto_check_checkbox", 
                           default_value=self.settings.get('auto_check', True))
            
            dpg.add_checkbox(label=self.translations.get('settings_dark_theme'), 
                           tag="dark_theme_checkbox", 
                           default_value=self.settings.get('dark_theme', False),
                           callback=self.toggle_theme_dpg)
            
            dpg.add_text(self.translations.get('settings_language'))
            dpg.add_combo(items=['ru', 'en'], 
                         tag="language_combo", 
                         default_value=self.settings.get('language', 'ru'),
                         callback=self.change_language_dpg)
            
            dpg.add_separator()
            
            # Кнопка сохранения
            dpg.add_button(label=self.translations.get('save_settings'), 
                          callback=self.save_settings_dpg)
    
    def setup_log_tab_dpg(self):
        """Настройка вкладки журнала для DearPyGui"""
        with dpg.group():
            dpg.add_button(label="Обновить журнал", callback=self.refresh_log_dpg)
            dpg.add_separator()
            
            # Поле для лога
            log_content = self.data_manager.get_log_content()
            dpg.add_input_text(tag="log_text", 
                              default_value=log_content,
                              multiline=True, 
                              readonly=True,
                              width=700, 
                              height=400)
    
    def setup_theme(self):
        """Настройка темы DearPyGui"""
        if self.settings.get('dark_theme', False):
            dpg.bind_theme(dpg.create_theme_component(dpg.mvAll))
    
    def toggle_theme_dpg(self):
        """Переключить тему DearPyGui"""
        # Здесь можно добавить переключение темы
        pass
    
    def change_language_dpg(self):
        """Изменить язык DearPyGui"""
        if dpg.does_item_exist("language_combo"):
            new_language = dpg.get_value("language_combo")
            self.translations.set_language(new_language)
            # Показываем сообщение о необходимости перезапуска
            self.show_info_popup("Информация", "Для применения языка перезапустите приложение")
    
    def browse_download_path_dpg(self):
        """Выбрать путь загрузки DearPyGui"""
        # В DearPyGui используется встроенный файловый диалог
        with dpg.file_dialog(directory_selector=True, 
                           callback=self.file_dialog_callback, 
                           tag="file_dialog_id",
                           width=700, height=400):
            dpg.add_file_extension(".*")
    
    def file_dialog_callback(self, sender, app_data):
        """Callback для файлового диалога"""
        if app_data and 'file_path_name' in app_data:
            selected_path = app_data['file_path_name']
            dpg.set_value("download_path_input", selected_path)
    
    def save_settings_dpg(self):
        """Сохранить настройки DearPyGui"""
        try:
            settings = {
                'token': dpg.get_value("token_input"),
                'version_url': dpg.get_value("version_url_input"),
                'download_url': dpg.get_value("download_url_input"),
                'hash_url': dpg.get_value("hash_url_input"),
                'download_path': dpg.get_value("download_path_input"),
                'auto_check': dpg.get_value("auto_check_checkbox"),
                'dark_theme': dpg.get_value("dark_theme_checkbox"),
                'language': dpg.get_value("language_combo")
            }
            
            self.data_manager.save_settings(settings)
            self.settings = settings
            
            self.show_info_popup(self.translations.get('success'), 
                               self.translations.get('settings_saved'))
            
        except Exception as e:
            self.show_error_popup(self.translations.get('error'), str(e))
    
    def refresh_log_dpg(self):
        """Обновить содержимое журнала DearPyGui"""
        try:
            log_content = self.data_manager.get_log_content()
            dpg.set_value("log_text", log_content)
        except Exception as e:
            logging.error(f"Ошибка обновления лога: {e}")
    
    def update_progress_dpg(self, progress: int):
        """Обновить прогресс DearPyGui"""
        dpg.set_value("progress_bar", progress / 100.0)
        dpg.set_value("progress_text", f"{progress}%")
    
    def show_info_popup(self, title: str, message: str):
        """Показать информационное окно"""
        with dpg.window(label=title, modal=True, tag="info_popup"):
            dpg.add_text(message)
            dpg.add_button(label="OK", callback=lambda: dpg.delete_item("info_popup"))
    
    def show_error_popup(self, title: str, message: str):
        """Показать окно ошибки"""
        with dpg.window(label=title, modal=True, tag="error_popup"):
            dpg.add_text(message)
            dpg.add_button(label="OK", callback=lambda: dpg.delete_item("error_popup"))
    
    def check_update_async(self):
        """Асинхронная проверка обновлений DearPyGui"""
        def check_update_thread():
            try:
                dpg.configure_item("check_button", enabled=False)
                self.status = "Проверка обновлений..."
                dpg.set_value("status_text", f"{self.translations.get('status')} {self.status}")
                
                checker = UpdateChecker(self.settings, self.update_progress_dpg)
                has_update, current_version, latest_version = checker.check_version()
                
                self.current_version = current_version
                self.latest_version = latest_version
                
                dpg.set_value("current_version_text", 
                            f"{self.translations.get('current_version')} {current_version}")
                dpg.set_value("latest_version_text", 
                            f"{self.translations.get('latest_version')} {latest_version}")
                
                if has_update:
                    self.status = self.translations.get('status_update_available')
                    dpg.set_value("status_text", f"{self.translations.get('status')} {self.status}")
                    # Запускаем загрузку
                    self.download_update_async_dpg(checker, latest_version)
                else:
                    self.status = self.translations.get('status_up_to_date')
                    dpg.set_value("status_text", f"{self.translations.get('status')} {self.status}")
                    
            except Exception as e:
                self.status = self.translations.get('status_connection_error')
                dpg.set_value("status_text", f"{self.translations.get('status')} {self.status}")
                logging.error(f"Ошибка проверки обновлений: {e}")
            finally:
                dpg.configure_item("check_button", enabled=True)
        
        thread = threading.Thread(target=check_update_thread, daemon=True)
        thread.start()
    
    def download_update_async_dpg(self, checker: UpdateChecker, version: str):
        """Асинхронная загрузка обновления DearPyGui"""
        def download_thread():
            try:
                self.status = self.translations.get('status_downloading')
                dpg.set_value("status_text", f"{self.translations.get('status')} {self.status}")
                
                download_path = dpg.get_value("download_path_input")
                success = checker.download_update(download_path, version)
                
                if success:
                    self.status = self.translations.get('status_downloaded')
                    self.current_version = version
                    dpg.set_value("status_text", f"{self.translations.get('status')} {self.status}")
                    dpg.set_value("current_version_text", 
                                f"{self.translations.get('current_version')} {version}")
                    self.show_info_popup(self.translations.get('success'), 
                                       self.translations.get('download_complete'))
                    self.refresh_log_dpg()  # Обновляем лог
                else:
                    self.status = self.translations.get('status_hash_error')
                    dpg.set_value("status_text", f"{self.translations.get('status')} {self.status}")
                    
            except Exception as e:
                if "hash" in str(e).lower():
                    self.status = self.translations.get('status_hash_error')
                elif "extract" in str(e).lower():
                    self.status = self.translations.get('status_extraction_error')
                else:
                    self.status = self.translations.get('status_connection_error')
                
                dpg.set_value("status_text", f"{self.translations.get('status')} {self.status}")
                logging.error(f"Ошибка загрузки обновления: {e}")
        
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
    
    def run(self):
        """Запустить приложение DearPyGui"""
        dpg.create_viewport(title=self.translations.get('app_title'), width=800, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()


def main_dpg():
    """Главная функция для DearPyGui"""
    try:
        app = UpdaterAppDPG()
        app.run()
    except ImportError as e:
        print(f"Ошибка: {e}")
        print("Установите DearPyGui: pip install dearpygui")
        sys.exit(1)


if __name__ == "__main__":
    # Выбираем интерфейс в зависимости от аргументов командной строки
    if len(sys.argv) > 1 and sys.argv[1] == "--dpg":
        main_dpg()
    else:
        # Используем tkinter по умолчанию
        from main import main
        main()
