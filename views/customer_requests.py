import json
import sqlite3
from models import Customer

# CREATE TABLE `Customer` (
#     `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#     `name`    TEXT NOT NULL,
#     `address`    TEXT NOT NULL,
#     `email`    TEXT NOT NULL,
#     `password`    TEXT NOT NULL
# );
CUSTOMERS = []


def get_all_customers():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Black Box
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """SELECT c.id,c.name, c.address, c.email, c.password FROM customer c"""
        )

        # Initialize an  empty list to hold all the customer representations.
        customers = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate the list of data returned from the database

        for row in dataset:

            # Create a customer instance from the current row.
            # note that the database fields are specified in the
            # exact order of the parameters defined in the
            # Customer class above.

            customer = Customer(
                row["id"], row["name"], row["address"], row["email"], row["password"]
            )

            customers.append(customer.__dict__)
    return customers


def get_single_customer(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Use a parameter to inject a variables value
        # into the SQL statement
        db_cursor.execute(
            """SELECT c.id,c.name, c.address, c.email, c.password FROM customer c
            WHERE c.id = ?""",
            (id,),
        )

        # Load the single result into memory
        data = db_cursor.fetchone()
        customer = Customer(
            data["id"], data["name"], data["address"], data["email"], data["password"]
        )

        return customer.__dict__


def create_customer(customer):
    max_id = CUSTOMERS[-1]["id"]
    new_id = max_id + 1
    customer["id"] = new_id
    CUSTOMERS.append(customer)
    return customer


def delete_customer(id):
    customer_index = -1
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            customer_index = index
    if customer_index >= 0:
        CUSTOMERS.pop(customer_index)


def update_customer(id, new_customer):
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            CUSTOMERS[index] = new_customer
            break
