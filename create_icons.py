#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Создание иконок для приложения Python Updater
"""

import os
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

def create_app_icon():
    """Создание иконки приложения"""
    
    if not PIL_AVAILABLE:
        print("❌ PIL не установлен. Установите: pip install Pillow")
        return False
    
    print("🎨 Создание иконки приложения...")
    
    # Создаем изображение 1024x1024 для высокого качества
    size = 1024
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Создаем градиентный фон
    for y in range(size):
        # Градиент от синего к голубому
        blue_value = int(70 + (180 - 70) * y / size)
        color = (70, 130, blue_value, 255)
        draw.line([(0, y), (size, y)], fill=color)
    
    # Рисуем внешний круг
    margin = 80
    draw.ellipse([margin, margin, size-margin, size-margin], 
                fill=(100, 149, 237, 255), outline=(255, 255, 255, 255), width=12)
    
    # Рисуем внутренний круг для объема
    inner_margin = 140
    draw.ellipse([inner_margin, inner_margin, size-inner_margin, size-inner_margin], 
                fill=(135, 206, 250, 200), outline=(255, 255, 255, 150), width=6)
    
    # Добавляем текст PU
    try:
        if os.name == 'nt':
            # Windows
            font_paths = [
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/calibri.ttf",
                "C:/Windows/Fonts/segoeui.ttf"
            ]
            font = None
            for font_path in font_paths:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, 200)
                    break
        else:
            # Linux/macOS
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "/usr/share/fonts/TTF/arial.ttf"
            ]
            font = None
            for font_path in font_paths:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, 200)
                    break
        
        if font is None:
            font = ImageFont.load_default()
            
    except Exception as e:
        print(f"⚠️ Не удалось загрузить шрифт: {e}")
        font = ImageFont.load_default()
    
    text = "PU"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 30
    
    # Тень текста для объема
    shadow_offset = 8
    draw.text((x + shadow_offset, y + shadow_offset), text, fill=(0, 0, 0, 180), font=font)
    
    # Основной текст
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # Добавляем небольшой значок обновления (стрелка вниз)
    arrow_size = 60
    arrow_x = size - 150
    arrow_y = size - 150
    
    # Рисуем стрелку вниз
    arrow_points = [
        (arrow_x, arrow_y),
        (arrow_x + arrow_size, arrow_y),
        (arrow_x + arrow_size//2, arrow_y + arrow_size)
    ]
    draw.polygon(arrow_points, fill=(255, 255, 255, 200))
    
    # Сохраняем основную иконку
    img.save('icon.png', 'PNG')
    
    # Создаем ICO для Windows (несколько размеров)
    icon_sizes = [16, 24, 32, 48, 64, 128, 256]
    icons = []
    
    for icon_size in icon_sizes:
        icon_img = img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        icons.append(icon_img)
    
    # Сохраняем как ICO
    icons[0].save('icon.ico', format='ICO', sizes=[(s, s) for s in icon_sizes])
    
    print("✅ Созданы иконки:")
    print("  📱 icon.png (1024x1024)")
    print("  🪟 icon.ico (мульти-размер для Windows)")
    
    # Показываем размеры файлов
    png_size = os.path.getsize('icon.png') / 1024
    ico_size = os.path.getsize('icon.ico') / 1024
    print(f"  📊 Размеры: PNG {png_size:.1f}KB, ICO {ico_size:.1f}KB")
    
    return True

def create_macos_icns():
    """Создание ICNS иконки для macOS (будет выполнено в GitHub Actions)"""
    print("ℹ️  ICNS иконка для macOS будет создана автоматически в GitHub Actions")
    return True

if __name__ == "__main__":
    print("🎨 Python Updater - Создание иконок")
    print("=" * 50)
    
    success = create_app_icon()
    create_macos_icns()
    
    if success:
        print("\n🎉 Иконки успешно созданы!")
        print("📋 Готовые файлы:")
        
        files = ['icon.png', 'icon.ico']
        for file in files:
            if os.path.exists(file):
                size = os.path.getsize(file) / 1024
                print(f"  ✅ {file} ({size:.1f}KB)")
            else:
                print(f"  ❌ {file} не найден")
                
        print("\n🚀 Теперь можно собирать приложение!")
    else:
        print("\n❌ Ошибка при создании иконок")
        print("💡 Установите Pillow: pip install Pillow")
