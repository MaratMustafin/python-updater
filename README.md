# 🚀 Python Updater

**Современное приложение для автоматической проверки и установки обновлений с красивым интерфейсом CustomTkinter**

[![Build Status](https://github.com/yourusername/python-updater/workflows/🚀%20Build%20Python%20Updater/badge.svg)](https://github.com/yourusername/python-updater/actions)
[![Downloads](https://img.shields.io/github/downloads/yourusername/python-updater/total.svg)](https://github.com/yourusername/python-updater/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

![Python Updater Screenshot](https://via.placeholder.com/800x600/4A90E2/FFFFFF?text=Python+Updater+CustomTkinter)

## ✨ Особенности

- 🎨 **Современный интерфейс** на CustomTkinter с профессиональным дизайном
- 🌍 **Кроссплатформенность** - Windows, macOS, Linux
- 🔐 **Безопасность** - проверка SHA256 хешей загружаемых файлов
- 🌓 **Тёмная/светлая тема** с автоматическим переключением
- 🌐 **Мультиязычность** - русский и английский интерфейс
- ⚡ **Автообновления** при запуске приложения
- 📝 **Полное логирование** всех операций с ротацией логов
- 🔧 **Выполнение .reg файлов** автоматически после загрузки (Windows)
- 📊 **Прогресс-бары** с реальным отображением процесса
- ⚙️ **Гибкая настройка** через JSON конфигурацию

## 📥 Скачать

**[📦 Последняя версия](https://github.com/yourusername/python-updater/releases/latest)**

### Доступные сборки:

- **🪟 Windows**: `PythonUpdater_Windows.zip`
  - `PythonUpdater_CTK.exe` - готовый к использованию
  
- **🍎 macOS**: `PythonUpdater_macOS.tar.gz`
  - `PythonUpdater_CustomTkinter.app` - нативное приложение
  
- **🐧 Linux**: `PythonUpdater_Linux.tar.gz`
  - `PythonUpdater_CustomTkinter_Linux` - исполняемый файл

## Требования

- Python 3.7+
- tkinter (обычно входит в состав Python)
- requests
- appdirs

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

## Сборка исполняемого файла

### Windows

```cmd
build.bat
```

### macOS/Linux

```bash
chmod +x build.sh
./build.sh
```

Исполняемый файл будет создан в папке `dist/`.

## Настройка

При первом запуске приложения перейдите на вкладку "Настройки" и укажите:

1. **Токен авторизации** - Bearer токен для доступа к API
2. **URL версии** - адрес для получения информации о последней версии (по умолчанию: https://example.com/version.txt)
3. **URL загрузки** - адрес для загрузки файла обновления (по умолчанию: https://example.com/myfile.zip)
4. **URL хеша** - адрес для получения SHA256 хеша файла (по умолчанию: https://example.com/myfile.zip.sha256)
5. **Путь загрузки** - директория для сохранения обновлений
6. **Автопроверка при запуске** - автоматическая проверка обновлений при запуске приложения
7. **Язык интерфейса** - русский или английский

## Использование

1. **Проверка обновлений**: Нажмите кнопку "Проверить обновление" на вкладке "Обновление"
2. **Просмотр журнала**: Перейдите на вкладку "Журнал" для просмотра логов всех операций
3. **Изменение настроек**: Используйте вкладку "Настройки" для изменения конфигурации

## Файловая структура

Приложение создает следующие файлы в пользовательской директории:

- `settings.json` - настройки приложения
- `version.txt` - текущая версия
- `log.txt` - журнал операций

### Windows
```
%APPDATA%\YourCompany\PythonUpdater\
```

### macOS
```
~/Library/Application Support/PythonUpdater/
```

## API Формат

### Файл версии
Должен содержать строку с номером версии, например:
```
1.0.2
```

### Файл хеша
Должен содержать SHA256 хеш ZIP файла, например:
```
a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3
```

## Безопасность

- Все сетевые запросы выполняются с проверкой SSL сертификатов
- Загруженные файлы обязательно проверяются по SHA256 хешу
- Токен авторизации хранится локально в зашифрованном виде
- Логируются все операции для аудита

## Лицензия

MIT License

## Автор

YourCompany
