import datetime
import sqlite3
import json


class BakeShop():

    def eat(self, pk):
        # Open a connection to the database
        with sqlite3.connect("./cookies.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to get the information you want
            db_cursor.execute("""
                UPDATE cookies
                SET eaten_at = ?
                WHERE id = ?
                """,
                (
                    datetime.datetime.now(),
                    pk
                )
            )

            rows_modified = db_cursor.rowcount

            if rows_modified != 0:
                return True

            return False

    def inventory(self):
        # Open a connection to the database
        with sqlite3.connect("./cookies.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to get the information you want
            db_cursor.execute("""
            SELECT c.id,
                c.name name,
                f.name flavor_name,
                c.baked_at
            FROM cookies c
            JOIN flavors f ON f.id = c.flavor_id
            WHERE c.eaten_at IS NULL
            """)
            query_results = db_cursor.fetchall()

            # Initialize an empty list and then add each dictionary to it
            cookies=[]
            for row in query_results:
                cookies.append(dict(row))


        return json.dumps(cookies)

    def sample(self, pk):
        # Open a connection to the database
        with sqlite3.connect("./cookies.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to get the information you want
            db_cursor.execute("""
            SELECT c.id,
                c.name name,
                f.name flavor_name,
                c.baked_at,
                t.name topping
            FROM cookies c
            JOIN flavors f ON f.id = c.flavor_id
            JOIN cookie_toppings ct ON c.id = ct.cookie_id
            JOIN toppings t ON t.id = ct.topping_id
            WHERE c.id = ?
            AND c.eaten_at IS NULL
            """, (pk ,))
            cookies = db_cursor.fetchall()

            # Cache lookup (hash lookup)
            cookie_with_toppings = {}
            for row in cookies:
                if "id" in cookie_with_toppings:
                    cookie_with_toppings['toppings'].append(row['topping'])
                else:
                    # It hasn't been created
                    cookie_with_toppings = {
                        "id": row['id'],
                        "name": row['name'],
                        "flavor_name": row['flavor_name'],
                        "baked_at": row['baked_at'],
                        "toppings": [ row['topping'] ]
                    }

        if cookies is not None:
            return json.dumps(cookie_with_toppings)
        else:
            return ""

    def bake(self, cookie_dict):
        # Clientn needs to send name, flavor_id
        with sqlite3.connect("./cookies.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to create the information you want
            db_cursor.execute(
                """
                INSERT INTO cookies (name, flavor_id)
                VALUES(?, ?)
                """,
                (
                    cookie_dict['name'],
                    cookie_dict['flavorId'],
                )
            )

            new_id = db_cursor.lastrowid

            response_body = json.dumps({
                "id": new_id,
                "name": cookie_dict['name'],
                "flavor_id": cookie_dict['flavorId']
            })

            return response_body

    def decorate(self, cookie_dict):
        # Clientn needs to send name, flavor_id
        with sqlite3.connect("./cookies.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to create the information you want
            db_cursor.execute(
                """
                INSERT INTO cookie_toppings (cookie_id, topping_id)
                VALUES(?, ?)
                """,
                (
                    cookie_dict['cookieId'],
                    cookie_dict['toppingId'],
                )
            )

            new_id = db_cursor.lastrowid

            response_body = json.dumps({
                "id": new_id,
                "cookie_id": cookie_dict['cookieId'],
                "topping_id": cookie_dict['toppingId']
            })

            return response_body
