import sqlite3
import os


def init_database():
    # Удаляем старый файл если существует
    if os.path.exists('fstr_db.db'):
        os.remove('fstr_db.db')

    conn = sqlite3.connect('fstr_db.db')
    cursor = conn.cursor()

    # Включаем поддержку внешних ключей
    cursor.execute("PRAGMA foreign_keys = ON")

    # Создаем таблицы в правильном порядке
    cursor.executescript("""
        -- Пользователи
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(255) UNIQUE NOT NULL,
            fam VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            otc VARCHAR(255),
            phone VARCHAR(20) NOT NULL
        );

        -- Координаты
        CREATE TABLE IF NOT EXISTS coords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude FLOAT NOT NULL,
            longitude FLOAT NOT NULL,
            height INTEGER NOT NULL
        );

        -- Перевалы
        CREATE TABLE IF NOT EXISTS pereval_added (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            coords_id INTEGER NOT NULL,
            beauty_title VARCHAR(255) NOT NULL,
            title VARCHAR(255) NOT NULL,
            other_titles VARCHAR(255),
            connect VARCHAR(255),
            add_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(20) NOT NULL DEFAULT 'new',
            winter_level VARCHAR(20),
            summer_level VARCHAR(20),
            autumn_level VARCHAR(20),
            spring_level VARCHAR(20),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (coords_id) REFERENCES coords(id) ON DELETE CASCADE
        );

        -- Изображения
        CREATE TABLE IF NOT EXISTS pereval_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pereval_id INTEGER NOT NULL,
            image TEXT NOT NULL,
            title VARCHAR(255) NOT NULL,
            FOREIGN KEY (pereval_id) REFERENCES pereval_added(id) ON DELETE CASCADE
        );
    """)

    print("Все таблицы успешно созданы")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_database()