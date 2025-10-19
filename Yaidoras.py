import os
import re
from pystyle import Colors, Colorate, Center, Write

# Папка с базами
BASE_DIR = "/storage/emulated/0/DataBases"

# Паттерн для поиска телефонов
PHONE_PATTERN = re.compile(r'(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}')

def display_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    
    banner = """
    ██╗   ██╗ █████╗ ██████╗ ██╗██████╗  ██████╗ ██████╗  █████╗ ███████╗
    ╚██╗ ██╔╝██╔══██╗██╔══██╗██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔════╝
     ╚████╔╝ ███████║██████╔╝██║██████╔╝██║   ██║██████╔╝███████║███████╗
      ╚██╔╝  ██╔══██║██╔═══╝ ██║██╔══██╗██║   ██║██╔══██╗██╔══██║╚════██║
       ██║   ██║  ██║██║     ██║██║  ██║╚██████╔╝██║  ██║██║  ██║███████║
       ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
    """
    
    print(Colorate.Horizontal(Colors.red_to_blue, Center.XCenter(banner)))
    print(Center.XCenter("📂 Тул для поиска номеров в базах (.txt, .csv)"))
    print(Center.XCenter("🔥 Бесплатный тул от @vredon0s 🔥"))
    print("\n" + "="*60 + "\n")

def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        Write.Print(f"❌ Ошибка чтения {file_path}: {e}\n", Colors.red, 0.01)
        return ""

def search_specific_phone():
    phone = Write.Input("📱 Введите номер для поиска: ", Colors.blue, 0.01)
    if not phone:
        return
    
    search_digits = re.sub(r"\D", "", phone)
    found_files = []

    for file in os.listdir(BASE_DIR):
        if file.endswith(".txt") or file.endswith(".csv"):
            path = os.path.join(BASE_DIR, file)
            content = read_file(path)
            if search_digits in re.sub(r"\D", "", content):
                Write.Print(f"✅ Найдено в {file}\n", Colors.green, 0.01)
                found_files.append(file)
            else:
                Write.Print(f"❌ Не найдено в {file}\n", Colors.red, 0.01)

    Write.Print(f"\n🎯 Итог: найдено в {len(found_files)} файлах\n", Colors.yellow, 0.01)

def search_all_phones():
    Write.Print("\n🔍 Ищем все номера во всех файлах...\n", Colors.yellow, 0.01)
    all_phones = set()

    for file in os.listdir(BASE_DIR):
        if file.endswith(".txt") or file.endswith(".csv"):
            path = os.path.join(BASE_DIR, file)
            content = read_file(path)
            matches = PHONE_PATTERN.findall(content)
            if matches:
                Write.Print(f"✅ В {file} найдено {len(matches)} номеров\n", Colors.green, 0.01)
                all_phones.update(matches)
            else:
                Write.Print(f"❌ В {file} номера не найдены\n", Colors.red, 0.01)

    if all_phones:
        output_file = os.path.join(BASE_DIR, "найденные_номера.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            for phone in sorted(all_phones):
                f.write(phone + "\n")
        Write.Print(f"\n💾 Все номера сохранены в: {output_file}\n", Colors.green, 0.01)
        Write.Print(f"📊 Всего уникальных номеров: {len(all_phones)}\n", Colors.green, 0.01)
    else:
        Write.Print("❌ Номера не найдены\n", Colors.red, 0.01)

def main():
    display_banner()
    while True:
        Write.Print("Выберите действие:\n", Colors.blue, 0.01)
        Write.Print("1. 🔍 Поиск по номеру телефона\n", Colors.white, 0.01)
        Write.Print("2. 📊 Поиск всех номеров\n", Colors.white, 0.01)
        Write.Print("3. 🚪 Выход\n", Colors.white, 0.01)

        choice = Write.Input("\nВведите номер: ", Colors.blue, 0.01)
        if choice == "1":
            search_specific_phone()
        elif choice == "2":
            search_all_phones()
        elif choice == "3":
            Write.Print("\n👋 До свидания!\n", Colors.green, 0.01)
            break
        else:
            Write.Print("\n❌ Неверный выбор!\n", Colors.red, 0.01)
        
        Write.Input("\nНажмите Enter чтобы продолжить...", Colors.white, 0.01)
        display_banner()

if __name__ == "__main__":
    if not os.path.exists(BASE_DIR):
        print(f"❌ Папка {BASE_DIR} не найдена! Создай её и положи базы.")
    else:
        main()
