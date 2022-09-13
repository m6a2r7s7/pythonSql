import psycopg2

conn = psycopg2.connect(database="my_db", user="postgres", password="")

with conn.cursor() as cur:

    def create_tables(cursor):
        cursor.execute("""
                    DROP TABLE phone_numbers;
                    DROP TABLE clients
                """)

        cursor.execute("""
            CREATE TABLE clients(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) NOT NULL,
            last_name VARCHAR(40) NOT NULL,
            email VARCHAR(40) NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE phone_numbers(
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL REFERENCES clients(id),
            number INTEGER
            );
        """)

        conn.commit()
        print("Created!")

    def add_new_client(cursor, first_name: str, last_name: str, email: str, phones=None):
        cursor.execute("""
            INSERT INTO clients(first_name, last_name, email) VALUES (%s, %s, %s);
            INSERT INTO phone_numbers(client_id, number) VALUES (1, %s) RETURNING client_id;
        """, (first_name, last_name, email, phones))
        print(cursor.fetchone())
        conn.commit()

    def add_phone_number(cursor, id: int, number: int):
        cursor.execute("""
            INSERT INTO phone_numbers(client_id, number) VALUES(%s, %s) RETURNING client_id, number;
        """, (id, number))
        print(cursor.fetchone())
        conn.commit()

    def change_data(cursor, id: int, first_name=None, last_name=None, email=None, phone=None):
        cursor.execute("""
                UPDATE clients SET first_name=%s, last_name=%s, email=%s, phone=%s WHERE id=%s RETURNING id, name;
            """, (first_name, last_name, email, phone, id))
        print(cursor.fetchone())
        conn.commit()

    def delete_client(cursor, id: int):
        cursor.execute("""
                DELETE FROM clients WHERE id=%s;
            """, (id,))
        conn.commit()

    def search_client(cursor, first_name=None, last_name=None, email=None, phone=None):
        cursor.execute("""
            SELECT * FROM clients
            INNER JOIN phone_numbers on phone_numbers.client_id = clients.id
            WHERE %s OR %s OR %s OR %s IN (clients);
        """, (first_name, last_name, email, phone))
        conn.commit()


    create_tables(cursor=cur)
    add_new_client(cur, first_name='Саша', last_name='Шакиров', email='qwerty@gmail.com')
    add_phone_number(cur, 1, 80006660066)
    search_client(cur, 'Александр')
    change_data(cur, first_name='Александр', last_name='Шакиров', id=1)
    delete_client(cur, 1)
    search_client(cur, first_name='Александр')

conn.close()
