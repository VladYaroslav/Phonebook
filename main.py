import os
import re

DATA_FILE = "phonebook.txt"


def validate_num(value: str) -> str:
    if not value:
        return print('Запись отсутствует')

    match = re.findall(r'(\+7|8|7).*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2})', value)

    if len(match) == 0:
        return print(f"Ошибка! Номер введён в неферном формате")

    return value


def validate_text(value: str) -> str:
    if not value:
        return print('Запись отсутствует')

    match = re.findall(r'[^\s\w]|_', value)

    if len(match) > 0:
        return print(f"Ошибка! Запись содержит спец. символы")

    return value


def load_data() -> list:
    """
    Функция для получения данных из файла
    :return:
    """
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                entry = line.strip().split(",")
                data.append(entry)
    return data


def display_page(chunked_list: list, page_number: int, total_pages: int) -> str:
    """
    Функция для обработки запроса пользователя
    :param chunked_list:
    :param page_number:
    :param total_pages:
    :return:
    """
    if not chunked_list:
        while True:
            print('Нет записей. Добавить y/n?')
            choice = input("Выберете действие: ")
            if choice == 'y':
                add_entry(load_data())
                main()
            elif choice == 'n':
                main()

    current_chunk = chunked_list[page_number]
    options = []
    if page_number > 0:
        options.append("1 Предыдущая страница")
    if page_number < total_pages - 1:
        options.append("2 Следущая страница")
    options.append("3 Выход")

    print(f"Страница {page_number + 1}/{total_pages}:")
    for idx, item in enumerate(current_chunk, start=1):
        print((
            f"{idx}. {item[0]} {item[1]} {item[2]}. Название организации:{item[3]} Рабочий номер:{item[4]} Личный номер:{item[5]}"))

    for option in options:
        print(option)

    choice = input("Выберете действие: ")
    return choice


def save_data(data: list) -> None:
    """
    Функция для добавления данных в фаил
    :param data:
    :return:
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for entry in data:
            f.write(",".join(entry) + "\n")


def display_entries(entries: list) -> None:
    """
    Функция для вывода данных
    :param entries:
    :return:
    """
    chunked_list = [entries[i:i + 5] for i in range(0, len(entries), 5)]
    current_page = 0
    total_pages = len(chunked_list)

    while True:
        result = display_page(chunked_list, current_page, total_pages)

        if result == "1" and current_page > 0:
            current_page -= 1
        elif result == "2" and current_page < total_pages - 1:
            current_page += 1
        elif result == "3":
            break


def add_entry(data: list) -> None:
    """
    Функция для предварительного полцчения данных для последующей записи в фаил
    :param data:
    :return:
    """
    new_entry = []
    while True:
        first_name = input("Введите фамилию: ")
        if first_name == validate_text(first_name):
            new_entry.append(first_name)
            break
    while True:
        last_name = input("Введите имя: ")
        if last_name == validate_text(last_name):
            new_entry.append(last_name)
            break
    while True:
        surname = input("Введите отчество: ")
        if surname == validate_text(surname):
            new_entry.append(surname)
            break
    while True:
        orgname = input("Введите название организации: ")
        if orgname == validate_text(orgname):
            new_entry.append(orgname)
            break
    while True:
        job_num = input("Введите рабочий телефон: ")
        if len(validate_num(job_num)) > 0:
            new_entry.append(job_num)
            break
    while True:
        home_num = input("Введите личный телефон: ")
        if len(validate_num(home_num)) > 0:
            new_entry.append(home_num)
            break
    data.append(new_entry)
    save_data(data)
    print("Запись добавлена.")


def edit_entry(data: list, idx: int) -> None:
    """
    Функция для редоктирования данных в файле
    :param data:
    :param idx:
    :return:
    """
    if 0 <= idx < len(data):
        entry = data[idx]
        print("Редактирование записи:")
        entry[0] = input("Введите новую фамилию: ")
        entry[1] = input("Введите новое имя: ")
        entry[2] = input("Введите новое отчество: ")
        entry[3] = input("Введите новое название организации: ")
        entry[4] = input("Введите новый рабочий телефон: ")
        entry[5] = input("Введите новый личный телефон: ")
        save_data(data)
        print("Запись отредактирована.")
    else:
        print("Некорректный индекс записи.")


def search_entries(entries: list, query: str) -> list:
    """
    Функция для поиска данных по запросу
    :param entries:
    :param query:
    :return:
    """
    results = []
    for entry in entries:
        if any(query.lower() in field.lower() for field in entry):
            results.append(entry)
    return results


def main() -> None:
    """
    Точка входа в приложение
    :return:
    """
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            pass
    data = load_data()
    while True:
        print("\nМеню:")
        print("1. Вывести записи")
        print("2. Добавить запись")
        print("3. Редактировать запись")
        print("4. Поиск записей")
        print("5. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            display_entries(data)
        elif choice == '2':
            add_entry(data)
        elif choice == '3':
            display_entries(data)
            idx = int(input("Выберите индекс записи для редактирования: ")) - 1
            edit_entry(data, idx)
        elif choice == '4':
            query = input("Введите текст для поиска: ")
            results = search_entries(data, query)
            if results:
                display_entries(results)
            else:
                print("Ничего не найдено.")
        elif choice == '5':
            break
        else:
            print("Некорректный выбор. Пожалуйста, выберите снова.")


if __name__ == "__main__":
    main()
