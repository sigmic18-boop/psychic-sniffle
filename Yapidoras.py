import pandas as pd
import glob
import re
import os
from pystyle import Colors, Colorate, Center, Box, Write

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
    print(Center.XCenter("тул бесплатный, от @vredon0s"))
    print("\n" + "="*60 + "\n")

def find_phones_in_csv(file_path, phone_pattern):
    """Быстрый поиск номеров в CSV файле"""
    found = []
    try:
        # Читаем файл чанками для больших файлов
        chunk_size = 10000
        for chunk in pd.read_csv(file_path, chunksize=chunk_size, low_memory=False, encoding_errors='ignore'):
            # Преобразуем весь чанк в строку для быстрого поиска
            chunk_str = chunk.to_string()
            matches = phone_pattern.findall(chunk_str)
            for match in matches:
                found.append(match)
                
    except Exception as e:
        Write.Print(f"❌ Ошибка при обработке {file_path}: {str(e)}", Colors.red, interval=0.01)
    
    return found

def search_specific_phone():
    """Поиск конкретного номера во всех базах"""
    phone = Write.Input("📱 Введите номер для поиска: ", Colors.blue, interval=0.01)
    if not phone:
        return
    
    Write.Print(f"\n🔍 Ищем номер: {phone}", Colors.yellow, interval=0.01)
    print()
    
    # Нормализуем номер для поиска
    search_digits = re.sub(r'\D', '', phone)
    
    csv_files = glob.glob("*.csv")
    if not csv_files:
        Write.Print("❌ CSV файлы не найдены в текущей папке!", Colors.red, interval=0.01)
        return
    
    total_found = 0
    
    for csv_file in csv_files:
        Write.Print(f"📁 Проверяем: {csv_file}", Colors.cyan, interval=0.01)
        
        try:
            file_size = os.path.getsize(csv_file)
            size_str = f"{file_size/1024/1024:.1f} MB" if file_size > 1024*1024 else f"{file_size/1024:.1f} KB"
            Write.Print(f"   Размер: {size_str}", Colors.white, interval=0.01)
            
            found_in_file = 0
            chunk_size = 50000
            
            for chunk in pd.read_csv(csv_file, chunksize=chunk_size, low_memory=False, encoding_errors='ignore'):
                # Быстрый поиск по всему чанку
                chunk_str = chunk.to_string()
                if search_digits in chunk_str:
                    Write.Print(f"   ✅ НАЙДЕНО В {csv_file}!", Colors.green, interval=0.01)
                    found_in_file += 1
                    total_found += 1
                    break
            
            if found_in_file == 0:
                Write.Print("   ❌ Не найдено", Colors.red, interval=0.01)
                
        except Exception as e:
            Write.Print(f"   💥 Ошибка: {str(e)}", Colors.red, interval=0.01)
    
    Write.Print(f"\n🎯 Итого найдено в {total_found} файлах", Colors.green, interval=0.01)

def search_all_phones():
    """Поиск всех номеров во всех базах"""
    Write.Print("\n🔍 Ищем все номера телефонов...", Colors.yellow, interval=0.01)
    print()
    
    # Паттерн для российских номеров
    phone_pattern = re.compile(r'(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}')
    
    csv_files = glob.glob("*.csv")
    if not csv_files:
        Write.Print("❌ CSV файлы не найдены в текущей папке!", Colors.red, interval=0.01)
        return
    
    all_phones = []
    
    for csv_file in csv_files:
        Write.Print(f"📁 Обрабатываем: {csv_file}", Colors.cyan, interval=0.01)
        
        try:
            file_size = os.path.getsize(csv_file)
            size_str = f"{file_size/1024/1024:.1f} MB" if file_size > 1024*1024 else f"{file_size/1024:.1f} KB"
            Write.Print(f"   Размер: {size_str}", Colors.white, interval=0.01)
            
            # Быстрый поиск номеров в файле
            found_phones = find_phones_in_csv(csv_file, phone_pattern)
            
            if found_phones:
                Write.Print(f"   ✅ Найдено номеров: {len(found_phones)}", Colors.green, interval=0.01)
                all_phones.extend(found_phones)
                
                # Показываем первые 5 найденных номеров
                for phone in found_phones[:5]:
                    Write.Print(f"      📞 {phone}", Colors.white, interval=0.01)
                if len(found_phones) > 5:
                    Write.Print(f"      ... и еще {len(found_phones) - 5} номеров", Colors.white, interval=0.01)
            else:
                Write.Print("   ❌ Номера не найдены", Colors.red, interval=0.01)
                
        except Exception as e:
            Write.Print(f"   💥 Ошибка: {str(e)}", Colors.red, interval=0.01)
    
    # Сохраняем все найденные номера в файл
    if all_phones:
        output_file = "найденные_номера.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            for phone in set(all_phones):  # Убираем дубликаты
                f.write(phone + '\n')
        
        Write.Print(f"\n💾 Все номера сохранены в: {output_file}", Colors.green, interval=0.01)
        Write.Print(f"📊 Всего уникальных номеров: {len(set(all_phones))}", Colors.green, interval=0.01)

def main():
    display_banner()
    
    while True:
        Write.Print("Выберите действие:\n", Colors.blue, interval=0.01)
        Write.Print("1. 🔍 Поиск по номеру телефона в базе данных\n", Colors.white, interval=0.01)
        Write.Print("2. 📊 Поиск по базе данных (все номера)\n", Colors.white, interval=0.01)
        Write.Print("3. 🚪 Выход\n", Colors.white, interval=0.01)
        
        choice = Write.Input("\nВведите номер: ", Colors.blue, interval=0.01)
        
        if choice == '1':
            search_specific_phone()
        elif choice == '2':
            search_all_phones()
        elif choice == '3':
            Write.Print("\n👋 До свидания!", Colors.green, interval=0.01)
            break
        else:
            Write.Print("\n❌ Неверный выбор!", Colors.red, interval=0.01)
        
        Write.Input("\nНажмите Enter чтобы продолжить...", Colors.white, interval=0.01)
        display_banner()

if __name__ == "__main__":
    # Проверяем наличие необходимых библиотек
    try:
        import pandas
        from pystyle import Colors, Colorate, Center, Box, Write
    except ImportError:
        print("Установите необходимые библиотеки:")
        print("pip install pandas pystyle")
        exit(1)
    
    main()
