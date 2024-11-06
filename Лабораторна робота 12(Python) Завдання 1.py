import json

FILE_PATH = 'train_schedule.json'
OUTPUT_FILE_PATH = 'search_result.json'

def load_schedule():
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {FILE_PATH} не знайдено. Будь ласка, додайте дані про поїзди.")
        return {}

def save_schedule(schedule):
    with open(FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(schedule, file, ensure_ascii=False, indent=4)

def save_search_results(results):
    try:
        with open(OUTPUT_FILE_PATH, 'r', encoding='utf-8') as file:
            existing_results = json.load(file)
    except FileNotFoundError:
        existing_results = {}

    existing_results.update(results)

    with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(existing_results, file, ensure_ascii=False, indent=4)

    print(f"Результати пошуку записані у файл {OUTPUT_FILE_PATH}")

def print_all_trains(schedule):
    if not schedule:
        print("Розклад поїздів порожній.")
    else:
        for train_num, details in schedule.items():
            print(f"Поїзд №{train_num}: {details['destination']}, Прибуття: {details['arrival'][0]:02d}:{details['arrival'][1]:02d}, Відправлення: {details['departure'][0]:02d}:{details['departure'][1]:02d}")

def add_train(schedule, train_num, destination, arrival, departure):
    if len(schedule) >= 10:
        print("Не можна додати більше 10 поїздів.")
        return
    if train_num in schedule:
        print(f"Поїзд з номером {train_num} вже існує!")
        return
    schedule[train_num] = {
        "destination": destination,
        "arrival": arrival,
        "departure": departure
    }
    save_schedule(schedule)
    print(f"Поїзд №{train_num} додано успішно.")

def remove_train(schedule, train_num):
    if train_num in schedule:
        del schedule[train_num]
        save_schedule(schedule)
        print(f"Поїзд №{train_num} видалено.")
    else:
        print(f"Поїзд з номером {train_num} не знайдено!")

def trains_at_station(schedule, current_time):
    current_hour, current_minute = current_time
    trains_on_station = []
    for train_num, details in schedule.items():
        arrival_hour, arrival_minute = details['arrival']
        departure_hour, departure_minute = details['departure']
        if (arrival_hour < current_hour or (arrival_hour == current_hour and arrival_minute <= current_minute)) and \
           (departure_hour > current_hour or (departure_hour == current_hour and departure_minute >= current_minute)):
            trains_on_station.append((train_num, details['destination']))
    return trains_on_station

def search_train_by_field(schedule, field, value):
    results = {}
    for train_num, details in schedule.items():
        if field == "arrival" or field == "departure":
            try:
                hour, minute = map(int, value.split(":"))
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    print("Помилка! Час має бути у форматі 'години:хвилини' в межах 0-23 годин і 0-59 хвилин.")
                    return
                if details[field] == [hour, minute]:
                    results[train_num] = details
            except ValueError:
                print("Помилка! Формат часу має бути 'години:хвилини'.")
                return
        else:
            if str(details.get(field, '')).lower() == value.lower():
                results[train_num] = details
    
    if results:
        save_search_results(results)
    else:
        print("Поїздів з такими параметрами не знайдено.")

def run_schedule_program():
    schedule = load_schedule()

    while True:
        print("\nМеню:")
        print("1. Вивести всі поїзди")
        print("2. Додати новий поїзд")
        print("3. Видалити поїзд")
        print("4. Знайти поїзди, що стоять на станції в заданий час")
        print("5. Пошук поїзда за полем")
        print("6. Вийти")
        choice = input("Оберіть дію: ")

        if choice == "1":
            print_all_trains(schedule)
        elif choice == "2":
            try:
                train_num = input("Введіть номер поїзда: ")
                destination = input("Введіть маршрут (наприклад, Київ - Львів): ")

                # Введення і перевірка часу прибуття
                arrival_hour = int(input("Час прибуття (години): "))
                arrival_minute = int(input("Час прибуття (хвилини): "))
                if not (0 <= arrival_hour <= 23 and 0 <= arrival_minute <= 59):
                    print("Помилка! Години мають бути в межах 0-23, а хвилини – 0-59.")
                    continue

                # Введення і перевірка часу відправлення
                departure_hour = int(input("Час відправлення (години): "))
                departure_minute = int(input("Час відправлення (хвилини): "))
                if not (0 <= departure_hour <= 23 and 0 <= departure_minute <= 59):
                    print("Помилка! Години мають бути в межах 0-23, а хвилини – 0-59.")
                    continue

                add_train(schedule, train_num, destination, [arrival_hour, arrival_minute], [departure_hour, departure_minute])
            except ValueError:
                print("Помилка введення! Невірний формат даних.")
        elif choice == "3":
            train_num = input("Введіть номер поїзда для видалення: ")
            remove_train(schedule, train_num)
        elif choice == "4":
            try:
                current_hour = int(input("Введіть поточний час (години): "))
                current_minute = int(input("Введіть поточний час (хвилини): "))
                if not (0 <= current_hour <= 23 and 0 <= current_minute <= 59):
                    print("Помилка! Години мають бути в межах 0-23, а хвилини – 0-59.")
                    continue

                trains = trains_at_station(schedule, (current_hour, current_minute))
                if trains:
                    print("Поїзди, що стоять на станції:")
                    for train_num, destination in trains:
                        print(f"Поїзд №{train_num}: {destination}")
                else:
                    print("На станції немає поїздів у цей час.")
            except ValueError:
                print("Помилка введення! Невірний формат часу.")
        elif choice == "5":
            field = input("Введіть поле для пошуку (destination, arrival, departure): ")
            value = input("Введіть значення для пошуку: ")
            search_train_by_field(schedule, field, value)
        elif choice == "6":
            print("Вихід з програми.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

#
run_schedule_program()
