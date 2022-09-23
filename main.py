import psycopg2

# conn = psycopg2.connect(database="my_db", user="postgres", password="")
# cursor = conn.cursor()

with psycopg2.connect(database="my_db", user="postgres", password="") as conn:

# with conn.cursor() as cur:
    cursor = conn.cursor()
    def create_tables():
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
            number BIGINT UNIQUE
            );
        """)
        # conn.commit()
        print("Created tables!")

    def add_new_client(id : int, first_name: str, last_name: str, email: str, phone_num=None):
        res = "~ "
        cursor.execute("""
            INSERT INTO clients( first_name, last_name, email) VALUES (%s, %s, %s);
        """, (first_name, last_name, email))
        res += f"created client with id = {id}"
        if phone_num != None:
            cursor.execute("""
                INSERT INTO phone_numbers(client_id, number) VALUES (%s, %s);
            """,  (id, phone_num))
            res += f" and phone number {phone_num}"
        print(res)
        # conn.commit()

    def add_phone_number(id: int, number):
        cursor.execute("""
            INSERT INTO phone_numbers(client_id, number) VALUES(%s, %s);
        """, (id, number))
        print(f"~ added a new phone number {number} to client {id}")
        # conn.commit()

    def change_data(id: int, first_name=None, last_name=None, email=None, phone=None):
        res = "~ "
        if first_name != None:
            cursor.execute("""
                UPDATE clients SET first_name=%s WHERE id=%s;
            """, (first_name, id))
            res += f"first name changed to {first_name}. "
        if last_name != None:
            cursor.execute("""
                UPDATE clients SET last_name=%s WHERE id=%s;
            """, (last_name, id))
            res += f"last name changed to {last_name}. "
        if email != None:
            cursor.execute("""
                UPDATE clients SET email=%s WHERE id=%s;
            """, (email, id))
            res += f"email changed to {email}. "
        if phone != None:
            cursor.execute("""
                UPDATE phone_numbers SET phone=%s WHERE client_id=%s;
            """, (phone, id))
            res += f"phone number changed to {phone}. "
        print(res)
        # conn.commit()

    def delete_client(id: int):
        cursor.execute("""
                DELETE FROM phone_numbers WHERE client_id=%s;
                DELETE FROM clients WHERE id=%s;
            """, (id, id))
        print(f"~ client {id} successfully deleted")
        # conn.commit()

    def search_client(first_name=None, last_name=None, email=None, phone=None):
        cursor.execute("""
            SELECT clients.id FROM clients
            INNER JOIN phone_numbers on phone_numbers.client_id = clients.id
            WHERE (first_name =%s) OR (last_name =%s) OR (email =%s) OR (number =%s);
        """, (first_name, last_name, email, phone))
        print(f"~ client {cursor.fetchone()}")
        # conn.commit()

create_tables()
add_new_client(id=1, first_name='Питер', last_name='Паркер', email='parker@pauk.com', phone_num=80000000000)
add_phone_number(id=1, number=80006660066)
change_data(first_name='Peter', last_name='Parker', id=1, email="myemail@pauk.com")
search_client(first_name='Peter')
delete_client(1)

# conn.close()
