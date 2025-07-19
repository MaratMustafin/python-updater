@echo off
echo 🚀 Создание портативной версии Python Updater для Windows
echo.

REM Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python 3.8+ и попробуйте снова.
    pause
    exit /b 1
)

echo 📦 Установка зависимостей...
pip install -r requirements.txt
pip install pyinstaller

echo 🎨 Создание иконки...
python create_icons.py

echo 🔨 Сборка портативной версии (без UPX)...
pyinstaller --name "PythonUpdater_Portable" ^
    --onefile ^
    --noconsole ^
    --noconfirm ^
    --clean ^
    --icon="icon.ico" ^
    --add-data "translations.json;." ^
    --add-data "README.md;." ^
    --hidden-import="customtkinter" ^
    --collect-data="customtkinter" ^
    --version-file="version_info.txt" ^
    --distpath="dist_portable" ^
    --workpath="build_portable" ^
    --specpath="." ^
    main_ctk.py

if exist "dist_portable\PythonUpdater_Portable.exe" (
    echo.
    echo ✅ Портативная версия создана успешно!
    echo 📁 Файл: dist_portable\PythonUpdater_Portable.exe
    echo 📊 Размер:
    dir "dist_portable\PythonUpdater_Portable.exe" | findstr PythonUpdater_Portable.exe
    echo.
    echo 🛡️ Рекомендации для антивируса:
    echo - Добавьте dist_portable\ в исключения антивируса
    echo - Запускайте от имени администратора если нужно
    echo - Используйте "Разрешить в Windows Defender"
    echo.
    echo 🎯 Готово! Портативная версия не требует установки.
    pause
) else (
    echo ❌ Ошибка при создании портативной версии!
    pause
    exit /b 1
)
