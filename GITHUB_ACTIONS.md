# 🚀 Python Updater - GitHub Actions Build System

## 📖 Обзор

Этот репозиторий использует GitHub Actions для автоматической сборки Python Updater на всех поддерживаемых платформах.

## 🔧 Настройка

### 1. Подготовка репозитория

```bash
# Клонируйте репозиторий
git clone <your-repo-url>
cd python-updater

# Убедитесь, что все файлы на месте
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Создание релиза

Для создания релиза с автоматической сборкой:

```bash
# Создайте тег версии
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions автоматически:
- 🔨 Соберёт все версии для Windows, macOS и Linux
- 📦 Создаст архивы для каждой платформы
- 🚀 Создаст GitHub Release с прикреплёнными файлами

## 🛠️ Рабочий процесс

### Триггеры сборки

- **Push в main/master** - Сборка для тестирования
- **Создание тега v*** - Сборка релиза
- **Pull Request** - Проверочная сборка
- **Ручной запуск** - Workflow Dispatch

### Этапы сборки

#### 🪟 Windows Build
- Использует `windows-latest`
- Собирает все 3 версии интерфейса
- Создаёт .exe файлы

#### 🍎 macOS Build
- Использует `macos-latest`
- Автоматически создаёт иконку .icns
- Собирает .app bundles

#### 🐧 Linux Build
- Использует `ubuntu-latest`
- Устанавливает системные зависимости
- Создаёт исполняемые файлы

#### 🎉 Release Creation
- Загружает все артефакты
- Создаёт архивы для каждой платформы
- Публикует GitHub Release

#### 🧪 Test Builds
- Проверяет целостность сборок
- Выводит информацию о файлах

## 📦 Артефакты

После сборки доступны следующие файлы:

### Windows
- `PythonUpdater.exe` - Tkinter версия
- `PythonUpdater_CTK.exe` - CustomTkinter версия ⭐
- `PythonUpdater_DPG.exe` - DearPyGui версия

### macOS
- `PythonUpdater_Tkinter.app`
- `PythonUpdater_CustomTkinter.app` ⭐
- `PythonUpdater_DearPyGui.app`

### Linux
- `PythonUpdater_Tkinter_Linux`
- `PythonUpdater_CustomTkinter_Linux` ⭐
- `PythonUpdater_DearPyGui_Linux`

## ⚙️ Настройка workflow

### Переменные окружения

Workflow использует следующие переменные:
- `GITHUB_TOKEN` - Автоматически предоставляется GitHub

### Кастомизация

Для изменения настроек сборки отредактируйте `.github/workflows/build.yml`:

```yaml
# Изменить версию Python
python-version: '3.11'  # или '3.9', '3.10', '3.12'

# Добавить дополнительные флаги PyInstaller
--additional-hooks-dir=hooks/
--runtime-tmpdir=/tmp
```

### Секреты

Если требуется подпись кода или дополнительная аутентификация:

1. Перейдите в Settings → Secrets and variables → Actions
2. Добавьте необходимые секреты:
   - `APPLE_CERTIFICATE` (для подписи macOS)
   - `WINDOWS_CERTIFICATE` (для подписи Windows)

## 🚀 Запуск сборки

### Автоматическая сборка (по тегу)

```bash
# Создайте и отправьте тег
git tag v1.2.3
git push origin v1.2.3

# Сборка запустится автоматически
```

### Ручная сборка

1. Перейдите в GitHub Actions
2. Выберите "🚀 Build Python Updater"
3. Нажмите "Run workflow"
4. Выберите тип сборки (release/debug)

## 📊 Мониторинг

### Статус сборки

Проверить статус можно в разделе Actions вашего репозитория.

### Логи сборки

Каждый этап выводит подробные логи:
- 📦 Установка зависимостей
- 🔨 Процесс сборки
- 📋 Список созданных файлов
- 🧪 Результаты тестов

## ❗ Устранение проблем

### Сборка не запускается
- Проверьте, что файл `.github/workflows/build.yml` существует
- Убедитесь, что репозиторий публичный или у вас есть GitHub Actions на приватном

### Ошибки зависимостей
- Проверьте `requirements.txt`
- Убедитесь, что все зависимости совместимы

### Ошибки PyInstaller
- Проверьте spec файлы
- Убедитесь, что hidden-imports указаны правильно

## 💡 Советы

1. **CustomTkinter версия** - рекомендуется для лучшего UX
2. **Тестируйте локально** перед созданием тега
3. **Используйте семантическое версионирование** (v1.2.3)
4. **Проверяйте логи** при ошибках сборки

## 📝 Примеры команд

```bash
# Быстрое создание релиза
git add . && git commit -m "Release v1.0.1" && git tag v1.0.1 && git push origin main && git push origin v1.0.1

# Проверка статуса последней сборки (с GitHub CLI)
gh run list --workflow=build.yml --limit=1

# Скачивание артефактов последней сборки
gh run download $(gh run list --workflow=build.yml --limit=1 --json databaseId --jq '.[0].databaseId')
```

---

**🎯 Результат**: Полностью автоматизированная система сборки для всех платформ без необходимости владеть macOS машиной!
