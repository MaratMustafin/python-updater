# Инструкция по использованию Python Updater

## Быстрый старт

### 1. Запуск тестового сервера

Откройте новый терминал и запустите тестовый сервер:

```bash
python test_server.py
```

Сервер будет доступен на `http://localhost:8000` с токеном `test-token-123`.

### 2. Запуск приложения

#### Tkinter версия (рекомендуется):
```bash
python main.py
```

#### DearPyGui версия:
```bash
python main_dpg.py --dpg
```

### 3. Настройка приложения

1. Перейдите на вкладку "Настройки"
2. Введите следующие данные:
   - **Токен авторизации**: `test-token-123`
   - **URL версии**: `http://localhost:8000/version.txt`
   - **URL загрузки**: `http://localhost:8000/myfile.zip`
   - **URL хеша**: `http://localhost:8000/myfile.zip.sha256`
   - **Путь загрузки**: выберите любую папку на компьютере
3. Нажмите "Сохранить настройки"

### 4. Тестирование обновлений

1. Перейдите на вкладку "Обновление"
2. Нажмите "Проверить обновление"
3. Приложение автоматически:
   - Проверит версию на сервере
   - Загрузит ZIP файл
   - Проверит контрольную сумму
   - Распакует файлы
   - Обновит локальную версию

## Структура проекта

```
python-updater/
├── main.py              # Основное приложение (Tkinter)
├── main_dpg.py          # Альтернативная версия (DearPyGui)
├── test_server.py       # Тестовый HTTP сервер
├── requirements.txt     # Python зависимости
├── build.spec          # Конфигурация PyInstaller (Tkinter)
├── build_dpg.spec      # Конфигурация PyInstaller (DearPyGui)
├── build.bat           # Скрипт сборки для Windows
├── build.sh            # Скрипт сборки для macOS/Linux
├── README.md           # Документация
├── testing_guide.md    # Руководство по тестированию
└── usage_guide.md      # Данный файл
```

## Функции приложения

### Вкладка "Обновление"
- Отображение текущей и последней версии
- Статус проверки обновлений
- Кнопка "Проверить обновление"
- Выбор пути для загрузки
- Прогресс загрузки

### Вкладка "Настройки"
- Токен авторизации
- URL адреса для API
- Автопроверка при запуске
- Тёмная тема
- Выбор языка (русский/английский)

### Вкладка "Журнал"
- Просмотр всех операций
- Кнопка обновления журнала

## Статусы обновления

- **Файл актуален** - обновление не требуется
- **Доступно обновление** - найдена новая версия
- **Загрузка...** - процесс загрузки файла
- **Загружено** - обновление успешно установлено
- **Ошибка соединения** - проблемы с сетью или сервером
- **Ошибка контрольной суммы** - файл поврежден
- **Ошибка распаковки** - проблемы с архивом

## Автоматические функции

1. **Автопроверка при запуске** - если включена в настройках
2. **Автоматическая загрузка** - если найдено обновление
3. **Проверка целостности** - SHA256 хеш каждого файла
4. **Логирование** - все операции записываются в журнал

## Файлы данных

Приложение создает следующие файлы в пользовательской директории:

### Windows:
```
%APPDATA%\YourCompany\PythonUpdater\
├── settings.json    # Настройки приложения
├── version.txt      # Текущая версия
└── log.txt         # Журнал операций
```

### macOS:
```
~/Library/Application Support/PythonUpdater/
├── settings.json    # Настройки приложения
├── version.txt      # Текущая версия
└── log.txt         # Журнал операций
```

## Сборка исполняемых файлов

### Windows:
```cmd
build.bat
```

### macOS/Linux:
```bash
chmod +x build.sh
./build.sh
```

Будут созданы два исполняемых файла:
- `PythonUpdater.exe` - версия с Tkinter
- `PythonUpdater_DPG.exe` - версия с DearPyGui

## Устранение неполадок

### Ошибка "Модуль не найден"
```bash
pip install -r requirements.txt
```

### Ошибка соединения с сервером
1. Проверьте, запущен ли тестовый сервер
2. Убедитесь, что URL корректный
3. Проверьте токен авторизации

### Ошибка контрольной суммы
1. Проверьте, что файл не поврежден
2. Убедитесь, что хеш файл соответствует ZIP архиву

### Проблемы с интерфейсом
- Для Tkinter: обычно работает "из коробки"
- Для DearPyGui: убедитесь, что установлен `dearpygui>=1.10.1`

## Кастомизация

### Изменение URL по умолчанию
Отредактируйте класс `Config` в файле `main.py`:

```python
class Config:
    DEFAULT_VERSION_URL = "https://your-domain.com/version.txt"
    DEFAULT_DOWNLOAD_URL = "https://your-domain.com/update.zip"
    DEFAULT_HASH_URL = "https://your-domain.com/update.zip.sha256"
```

### Добавление нового языка
Отредактируйте класс `Translations` в файле `main.py`:

```python
LANGUAGES = {
    'ru': { ... },
    'en': { ... },
    'fr': {  # Новый язык
        'app_title': 'Gestionnaire de mises à jour',
        # ... другие переводы
    }
}
```

### Изменение темы
Для Tkinter: отредактируйте метод `apply_theme()` в классе `UpdaterApp`
Для DearPyGui: отредактируйте метод `setup_theme()` в классе `UpdaterAppDPG`

## Безопасность

1. **Токен**: храните в безопасном месте
2. **HTTPS**: используйте в продакшене
3. **Валидация**: всегда проверяйте хеши файлов
4. **Логи**: регулярно проверяйте журнал операций

## Поддержка

Если у вас возникли проблемы:

1. Проверьте журнал в приложении
2. Посмотрите файл `log.txt` в пользовательской директории
3. Убедитесь, что все зависимости установлены
4. Проверьте настройки сети и файрвола
