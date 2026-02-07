import sqlite3 as sql

import sqlite3

def init_db():
    # Устанавливаем соединение с файлом базы данных
    conn = sql.connect('vet_clinic.db')
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Таблица владельцев
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Owners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')

    # 2. Таблица питомцев (связана с Owners через owner_id)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            species TEXT NOT NULL,
            age INTEGER,
            owner_id INTEGER,
            FOREIGN KEY (owner_id) REFERENCES Owners (id) ON DELETE CASCADE
        )
    ''')

    # 3. Таблица записей на прием
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id INTEGER,
            date_time TEXT NOT NULL,
            reason TEXT,
            status TEXT DEFAULT 'Запланировано',
            FOREIGN KEY (pet_id) REFERENCES Pets (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print("База данных успешно инициализирована")

if __name__ == "__main__":
    init_db()

def add_patient(owner_name, owner_phone, pet_name, pet_species, pet_age):
    conn = sql.connect('vet_clinic.db')
    cursor = conn.cursor()

    try:
        #добавляем владельца
        cursor.execute(
            "INSERT INTO Owners (full_name, phone) VALUES (?, ?)",
            (owner_name, owner_phone)
        )
        owner_id = cursor.lastrowid

        #добавляем питомца
        cursor.execute(
            "INSERT INTO Pets (name, species, age, owner_id) VALUES (?, ?, ?, ?)",
            (pet_name, pet_species, pet_age, owner_id)
        )

        conn.commit()
        print(f"питомец {pet_name} и владелец {owner_name} успешно добавлены")
    except Exception as e:
        print(f"ошибка при добавлении: {e}")
        conn.rollback()
    finally:
        conn.close()

#добавить прием
def add_appointment(pet_id, date_time, reason):
    conn = sql.connect('vet_clinic.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Appointments (pet_id, date_time, reason) VALUES (?, ?, ?)",
            (pet_id, date_time, reason)
        )
        conn.commit()
        print(f"запись на {date_time} создана успешно")
    except Exception as e:
        print(f"ошибка записи {e}")
        conn.rollback()
    finally:
        conn.close()

#получить всеъ пациентов
def get_all_patients():
    conn=sql.connect('vet_clinic.db')
    cursor = conn.cursor()

    query = """
    SELECT Pets.id, Pets.name, Pets.species, Pets.age, Owners.full_name, Owners.phone
    FROM Pets 
    JOIN Owners ON Pets.owner_id = Owners.id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#история приемов по pet_id
def get_pet_history(pet_id):
    conn = sql.connect('vet_clinic.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT date_time, reason, status FROM Appointments WHERE pet_id = ?",
        (pet_id,)
    )
    history = cursor.fetchall()
    conn.close()
    return history

#удалить питомца и его приемы
def delete_pet(pet_id):
    conn = sql.connect('vet_clinic.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Pets WHERE id = ?", (pet_id,))
    conn.commit()
    conn.close()
    print(f"Запись о питомце ID {pet_id} удалена.")

#обновить статус обращения
def update_appointment_status(appointment_id, new_status):
    conn = sql.connect('vet_clinic.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Appointments SET status = ? WHERE id = ?",
            (new_status, appointment_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка при обновлении статуса: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

#изменить номер телефона
def update_owner_phone(owner_id, new_phone):
    conn = sql.connect('vet_clinic.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Owners SET phone = ? WHERE id = ?",
            (new_phone, owner_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка при обновлении телефона: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

#найти питомца по номеру телефона
def get_patients_by_phone(phone):
    conn = sql.connect('vet_clinic.db')
    cursor = conn.cursor()
    # ищем питомцев, объединяя таблицы по ID владельца, фильтруя по телефону
    query = """
    SELECT Pets.id, Pets.name, Pets.species, Owners.full_name
    FROM Pets
    JOIN Owners ON Pets.owner_id = Owners.id
    WHERE Owners.phone LIKE ?
    """
    cursor.execute(query, (f"%{phone}%",))
    rows = cursor.fetchall()
    conn.close()
    return rows

#найти имя и id пользователя по его телефону
def get_owner_by_phone(phone):
    conn = sql.connect('vet_clinic.db')
    cursor = conn.cursor()
    # Ищем владельца по точному совпадению номера
    cursor.execute("SELECT id, full_name FROM Owners WHERE phone = ?", (phone,))
    owner = cursor.fetchone()
    conn.close()
    return owner

def get_all_appointments():
    conn = sql.connect('vet_clinic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, pet_id, date_time, status FROM Appointments")
    rows = cursor.fetchall()
    conn.close()
    return rows
