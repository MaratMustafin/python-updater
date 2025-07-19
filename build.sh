#!/bin/bash
echo "========================================"
echo "     Python Updater - Сборка"
echo "========================================"

echo "Устанавливаем зависимости..."
pip3 install -r requirements.txt

echo ""
echo "Устанавливаем PyInstaller..."
pip3 install pyinstaller

echo ""
echo "Создаем папку dist, если не существует..."
mkdir -p dist

echo ""
echo "Сборка Tkinter версии..."
pyinstaller build.spec

echo ""
echo "Сборка CustomTkinter версии..."
pyinstaller build_ctk.spec

echo ""
echo "Сборка DearPyGui версии..."
pyinstaller build_dpg.spec

echo ""
echo "========================================"
echo "Сборка завершена!"
echo "Файлы находятся в папке dist/:"
echo "- PythonUpdater (Tkinter)"
echo "- PythonUpdater_CTK (CustomTkinter)"
echo "- PythonUpdater_DPG (DearPyGui)"
echo "========================================"
