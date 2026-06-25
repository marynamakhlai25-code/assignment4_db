import os
import random
from datetime import datetime, date, timedelta
import psycopg2
from psycopg2.extras import execute_values
from faker import Faker

# Налаштування підключення до бази даних
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "dbname": "stores",
    "user": "macbook",
    "password": "1"
}

fake = Faker()


def fill_tennis_club():
    print("Підключення до бази даних")
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        # 1. Генерація кортів
        print("Вставлення даних про корти")
        courts_data = [
            ("Центральний корт", "Grass", True),
            ("Корт №2 (Ґрунт)", "Clay", True),
            ("Корт №3 (Хард)", "Hard", True),
            ("Критий корт №4", "Indoor", False)
        ]
        cursor.executemany(
            "INSERT INTO courts (court_name, surface_type, has_lighting) VALUES (%s, %s, %s);",
            courts_data
        )

        cursor.execute("SELECT court_id FROM courts;")
        court_ids = [row[0] for row in cursor.fetchall()]

        # 2. Генерація 2000 гравців
        print("Генерація 2000 гравців...")
        players_data = []
        levels = ['Beginner', 'Intermediate', 'Advanced', 'Pro']
        for _ in range(2000):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            phone = fake.phone_number()[:20]
            skill_level = random.choice(levels)
            birth_date = fake.date_of_birth(minimum_age=10, maximum_age=70)
            players_data.append((first_name, last_name, email, phone, skill_level, birth_date))

        execute_values(
            cursor,
            "INSERT INTO players (first_name, last_name, email, phone, skill_level, birth_date) VALUES %s;",
            players_data
        )

        cursor.execute("SELECT player_id FROM players;")
        player_ids = [row[0] for row in cursor.fetchall()]

        # 3. Генерація 50 тренерів
        print("Генерація 50 тренерів")
        coaches_data = []
        specs = ['Junior Coaching', 'Tactics & Strategy', 'Physical Conditioning', 'Pro Level Training']
        for _ in range(50):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            specialization = random.choice(specs)
            hourly_rate = random.randint(30, 150)
            coaches_data.append((first_name, last_name, email, specialization, hourly_rate))

        execute_values(
            cursor,
            "INSERT INTO coaches (first_name, last_name, email, specialization, hourly_rate) VALUES %s;",
            coaches_data
        )

        cursor.execute("SELECT coach_id FROM coaches;")
        coach_ids = [row[0] for row in cursor.fetchall()]

        # 4. Генерація 510 000 бронювань (Bookings)
        print("Генерація 510 000 бронювань")
        bookings_data = []
        start_date = date(2023, 1, 1)

        for i in range(510000):
            court_id = random.choice(court_ids)
            player_id = random.choice(player_ids)
            coach_id = random.choice(coach_ids) if random.random() > 0.3 else None

            booking_date = start_date + timedelta(days=random.randint(0, 1000))
            start_hour = random.randint(7, 21)
            start_time = f"{start_hour:02d}:00:00"
            end_time = f"{(start_hour + random.randint(1, 2)):02d}:00:00"
            total_price = random.randint(20, 100)

            bookings_data.append((court_id, player_id, coach_id, booking_date, start_time, end_time, total_price))

            if len(bookings_data) >= 50000:
                execute_values(
                    cursor,
                    "INSERT INTO bookings (court_id, player_id, coach_id, booking_date, start_time, end_time, total_price) VALUES %s;",
                    bookings_data
                )
                bookings_data = []
                print(f"Завантажено {i + 1} рядків...")

        if bookings_data:
            execute_values(
                cursor,
                "INSERT INTO bookings (court_id, player_id, coach_id, booking_date, start_time, end_time, total_price) VALUES %s;",
                bookings_data
            )

        conn.commit()
        print("База даних тенісного клубу повністю заповнена")

    except Exception as e:
        conn.rollback()
        print(f"Виникла помилка: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    fill_tennis_club()
