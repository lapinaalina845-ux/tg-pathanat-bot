import os
import re

# === 1. Папка с файлами ===
FOLDER = "preparats"

# === 2. Считываем реальные файлы ===
real_files = set(os.listdir(FOLDER))

# === 3. Извлекаем список файлов из основного bot.py ===
bot_file = "bot.py"

with open(bot_file, encoding="utf-8") as f:
    text = f.read()

# Ищем строки типа "xxxxx_1.jpeg"
files_in_code = set(re.findall(r'[a-zA-Z0-9_]+\.jpe?g', text))

# === 4. Сравнение ===
missing_in_folder = files_in_code - real_files
missing_in_code = real_files - files_in_code

print("\n======= ФАЙЛЫ ЕСТЬ В КОДЕ, НО НЕТ В ПАПКЕ =======")
for f in sorted(missing_in_folder):
    print("❌", f)

print("\n======= ФАЙЛЫ ЕСТЬ В ПАПКЕ, НО НЕТ В КОДЕ =======")
for f in sorted(missing_in_code):
    print("⚠️", f)

print("\n======= ВСЕ ОК, ЕСЛИ ОБА СПИСКА ПУСТЫ =======")