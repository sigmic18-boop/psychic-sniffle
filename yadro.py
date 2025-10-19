import os
import re
from pystyle import Colors, Colorate, Center, Write

BASE_DIR = "/storage/emulated/0/DataBases"
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
    print(Center.XCenter("тул для поиска номеров и слов в базах"))
    print(Center.XCenter("бесплатный тул от vredon0s"))
    print("\n" + "="*60 + "\n")

def read_file_lines(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                yield line.strip()
    except:
        return

def search_specific_phone():
    phone = Write.Input("введите номер для поиска ", Colors.blue, 0.01)
    if not phone:
        return
    search_digits = re.sub(r"\D", "", phone)
    for file in os.listdir(BASE_DIR):
        if file.startswith("vred") and (file.endswith(".txt") or file.endswith(".csv")):
            path = os.path.join(BASE_DIR, file)
            for i in range(2):
                found = False
                for line in read_file_lines(path):
                    if search_digits in re.sub(r"\D", "", line):
                        print(f"{file} {line}")
                        found = True
                if i == 0:
                    print("первая база данных прочищена")
                if found:
                    break

def search_all_phones():
    all_phones = set()
    for file in os.listdir(BASE_DIR):
        if file.startswith("vred") and (file.endswith(".txt") or file.endswith(".csv")):
            path = os.path.join(BASE_DIR, file)
            for i in range(2):
                found_in_file = False
                for line in read_file_lines(path):
                    matches = PHONE_PATTERN.findall(line)
                    if matches:
                        for m in matches:
                            all_phones.add(m)
                        found_in_file = True
                if i == 0:
                    print("первая база данных прочищена")
                if found_in_file:
                    print(f"{file} найдено {len(all_phones)} номеров")
                    break
    if all_phones:
        output_file = os.path.join(BASE_DIR, "найденные_номера.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            for phone in sorted(all_phones):
                f.write(phone + "\n")
        print(f"все номера сохранены в {output_file}")

def search_words():
    word = Write.Input("введите слово для поиска ", Colors.blue, 0.01)
    if not word:
        return
    for file in os.listdir(BASE_DIR):
        if file.startswith("vred") and (file.endswith(".txt") or file.endswith(".csv")):
            path = os.path.join(BASE_DIR, file)
            for i in range(2):
                found = False
                for line in read_file_lines(path):
                    if word.lower() in line.lower():
                        print(f"{file} {line}")
                        found = True
                if i == 0:
                    print("первая база данных прочищена")
                if found:
                    break

def main():
    display_banner()
    while True:
        Write.Print("выберите действие\n", Colors.blue, 0.01)
        Write.Print("1 поиск по номеру\n", Colors.white, 0.01)
        Write.Print("2 поиск всех номеров\n", Colors.white, 0.01)
        Write.Print("3 поиск по словам\n", Colors.white, 0.01)
        Write.Print("4 выход\n", Colors.white, 0.01)

        choice = Write.Input("введите номер ", Colors.blue, 0.01)
        if choice == "1":
            search_specific_phone()
        elif choice == "2":
            search_all_phones()
        elif choice == "3":
            search_words()
        elif choice == "4":
            break
        else:
            print("неверный выбор")

        Write.Input("нажмите enter чтобы продолжить", Colors.white, 0.01)
        display_banner()

if __name__ == "__main__":
    if not os.path.exists(BASE_DIR):
        print(f"папка {BASE_DIR} не найдена создайте и положите базы")
    else:
        main()
