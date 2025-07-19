@echo off
echo ========================================
echo     Python Updater - Сборка
echo ========================================

echo Устанавливаем зависимости...
pip install -r requirements.txt

echo.
echo Устанавливаем PyInstaller...
pip install pyinstaller

echo.
echo Создаем папку dist, если не существует...
if not exist "dist" mkdir dist

echo.
echo Сборка Tkinter версии...
pyinstaller build.spec

echo.
echo Сборка CustomTkinter версии...
pyinstaller build_ctk.spec

echo.
echo Сборка DearPyGui версии...
pyinstaller build_dpg.spec

echo.
echo ========================================
echo Сборка завершена!
echo Файлы находятся в папке dist/:
echo - PythonUpdater.exe (Tkinter)
echo - PythonUpdater_CTK.exe (CustomTkinter)
echo - PythonUpdater_DPG.exe (DearPyGui)
echo ========================================
pause
