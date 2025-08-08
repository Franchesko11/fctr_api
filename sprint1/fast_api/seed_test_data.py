import sqlite3


def insert_test_data():
    conn = sqlite3.connect('fstr_db.db')
    cursor = conn.cursor()

    # Очищаем таблицы (если нужно)
    cursor.executescript("""
    DELETE FROM pereval_images;
    DELETE FROM pereval_added;
    DELETE FROM coords;
    DELETE FROM users;
    """)

    # 1. Добавляем тестового пользователя
    cursor.execute("""
    INSERT INTO users (email, fam, name, phone, otc)
    VALUES (?, ?, ?, ?, ?)
    """, (
        'test@example.com',
        'Иванов',
        'Иван',
        '+79991234567',
        'Иванович'
    ))

    # 2. Добавляем координаты
    cursor.execute("""
    INSERT INTO coords (latitude, longitude, height)
    VALUES (?, ?, ?)
    """, (
        45.3842,  # Широта
        7.1525,  # Долгота
        1200  # Высота
    ))

    # 3. Добавляем перевал
    cursor.execute("""
    INSERT INTO pereval_added 
    (user_id, coords_id, beauty_title, title, status, 
     winter_level, summer_level, autumn_level, spring_level)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        1,  # user_id (связь с первым пользователем)
        1,  # coords_id (связь с первыми координатами)
        'пер. ',
        'Тестовый перевал',
        'new',  # Статус
        '1A',  # winter_level
        '1B',  # summer_level
        '1A',  # autumn_level
        '1A'  # spring_level
    ))

    # 4. Добавляем изображение для перевала
    cursor.execute("""
    INSERT INTO pereval_images (pereval_id, image, title)
    VALUES (?, ?, ?)
    """, (
        1,  # pereval_id (связь с первым перевалом)
        'base64_encoded_image_data',  # Пример данных изображения
        'Панорама перевала'
    ))

    conn.commit()
    conn.close()
    print("✅ Тестовые данные успешно добавлены в таблицы:")
    print("- 1 пользователь")
    print("- 1 набор координат")
    print("- 1 перевал")
    print("- 1 изображение")


if __name__ == "__main__":
    insert_test_data()