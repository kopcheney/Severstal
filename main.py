import db_manager
from prettytable import PrettyTable


def show_menu():
    print("\n--- ВЕТЕРИНАРНАЯ КЛИНИКА ---")
    print("1. Новый пациент (Регистрация)")
    print("2. Записать на прием")
    print("3. Список всех пациентов")
    print("4. Медицинская карта (История приемов)")
    print("5. Редактировать данные")
    print("6. Удалить питомца")
    print("0. Выход")
    return input("\nВыберите действие: ")


def main():
    db_manager.init_db()

    while True:
        choice = show_menu()

        if choice == "1":
            print("\n--- Регистрация нового пациента ---")
            o_name = input("ФИО владельца: ")
            o_phone = input("Телефон: ")
            p_name = input("Кличка питомца: ")
            p_species = input("Вид питомца (собака/кот/котопес/...): ")
            p_age = input("Возраст питомца: ")

            if db_manager.add_patient(o_name, o_phone, p_name, p_species, p_age):
                print(">>> Пациент успешно добавлен!")


        elif choice == "2":

            print("\n--- Запись к врачу ---")
            search_phone = input("Введите номер телефона владельца для поиска питомца: ")
            found_patients = db_manager.get_patients_by_phone(search_phone)

            if not found_patients:
                print(">>> Пациенты с таким номером не найдены.")
                continue
            print("\nНайденные питомцы:")

            helper_table = PrettyTable(["ID", "Кличка", "Вид", "Владелец"])

            for p in found_patients:
                helper_table.add_row(p)
            print(helper_table)

            p_id = input("\nВведите ID питомца из таблицы выше: ")
            valid_ids = [str(p[0]) for p in found_patients]

            if p_id not in valid_ids:
                print(">>> Ошибка: выберите ID только из списка найденных!")
                continue

            dt = input("Дата и время приема: ")
            reason = input("Причина визита: ")

            if db_manager.add_appointment(p_id, dt, reason):
                print(">>> Запись успешно создана!")

        elif choice == "3":
            print("\n--- Список всех пациентов ---")
            patients = db_manager.get_all_patients()
            table = PrettyTable(["ID", "Кличка", "Вид", "Возраст", "Владелец", "Телефон"])
            for p in patients:
                table.add_row(p)
            print(table)

        elif choice == "4":
            print("\n--- Медицинская карта (История приемов) ---")
            search_phone = input("Введите номер телефона владельца для поиска питомца: ")
            found_patients = db_manager.get_patients_by_phone(search_phone)

            if not found_patients:
                print(">>> Пациенты с таким номером не найдены.")
                continue
            print("\nНайденные питомцы:")

            helper_table = PrettyTable(["ID", "Кличка", "Вид", "Владелец"])

            for p in found_patients:
                helper_table.add_row(p)
            print(helper_table)

            p_id = input("\nВведите ID питомца из таблицы выше: ")
            valid_ids = [str(p[0]) for p in found_patients]

            if p_id not in valid_ids:
                print(">>> Ошибка: выберите ID только из списка найденных!")
                continue
            history = db_manager.get_pet_history(p_id)
            if history:
                table = PrettyTable(["Дата/Время", "Причина", "Статус"])
                for h in history:
                    table.add_row(h)
                print(table)
            else:
                print(">>> Истории болезни пока нет.")


        elif choice == "5":

            print("\n--- Редактировать данные ---")
            print("1. Изменить телефон владельца (по старому номеру)")
            print("2. Изменить статус приема (поиск по телефону)")
            sub_choice = input("Выбор: ")

            if sub_choice == "1":
                old_phone = input("Введите старый номер телефона: ")
                owner = db_manager.get_owner_by_phone(old_phone)
                if owner:
                    owner_id, owner_name = owner
                    print(f"Нашли владельца: {owner_name}")
                    new_phone = input("Введите новый номер телефона: ")
                    if db_manager.update_owner_phone(owner_id, new_phone):
                        print(">>> Телефон успешно обновлен!")
                else:
                    print(">>> Владелец с таким номером не найден.")

            elif sub_choice == "2":
                phone = input("Введите номер телефона владельца для поиска его записей: ")
                patients = db_manager.get_patients_by_phone(phone)
                if patients:
                    print("\nЗаписи на прием для ваших питомцев:")
                    table = PrettyTable(["ID Записи", "Кличка", "Дата", "Причина", "Статус"])
                    has_appointments = False
                    for p in patients:
                        pet_id, pet_name = p[0], p[1]
                        history = db_manager.get_pet_history(pet_id)
                        for h in history:
                            table.add_row(["Нужен ID", pet_name, h[0], h[1], h[2]])
                            has_appointments = True
                    if has_appointments:
                        print("Внимание: Чтобы менять статус, нам нужно видеть ID записи.")
                        print("Давайте сначала выведем ВСЕ приемы для выбора:")
                        all_apps = db_manager.get_all_appointments()
                        app_table = PrettyTable(["ID Записи", "ID Питомца", "Дата", "Статус"])
                        for a in all_apps:
                            app_table.add_row(a)
                        print(app_table)
                        app_id = input("\nВведите ID записи (из первой колонки): ")
                        new_status = input("Новый статус (например, Завершено): ")
                        if db_manager.update_appointment_status(app_id, new_status):
                            print(">>> Статус обновлен!")
                    else:
                        print(">>> У ваших питомцев пока нет записей на прием.")
                else:
                    print(">>> По этому номеру питомцы не найдены.")

        elif choice == "6":
            print("\n--- Удалить питомца ---")
            search_phone = input("Введите номер телефона владельца для поиска питомца: ")
            found_patients = db_manager.get_patients_by_phone(search_phone)

            if not found_patients:
                print(">>> Пациенты с таким номером не найдены.")
                continue
            print("\nНайденные питомцы:")

            helper_table = PrettyTable(["ID", "Кличка", "Вид", "Владелец"])

            for p in found_patients:
                helper_table.add_row(p)
            print(helper_table)

            p_id = input("\nВведите ID питомца из таблицы выше: ")
            valid_ids = [str(p[0]) for p in found_patients]

            if p_id not in valid_ids:
                print(">>> Ошибка: выберите ID только из списка найденных!")
                continue
            confirm = input(f"Вы уверены, что хотите удалить питомца ID {p_id}? (y/n): ")
            if confirm.lower() == 'y':
                db_manager.delete_pet(p_id)

        elif choice == "0":
            print("Программа завершена. До свидания!")
            break
        else:
            print("Неверный ввод, попробуйте снова.")


if __name__ == "__main__":
    main()

