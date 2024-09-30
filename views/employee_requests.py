import json
import sqlite3
from models import Employee, Location


EMPLOYEES = [
    {"id": 1, "name": "Jenna Solis"},
    {"id": 2, "name": "Max Headroom"},
    {"id": 3, "name": "Reid Michaels"},
]

# CREATE TABLE `Employee` (
# 	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
# 	`name`	TEXT NOT NULL,
# 	`address`	TEXT NOT NULL,
# 	`location_id` INTEGER NOT NULL,
# 	FOREIGN KEY(`location_id`) REFERENCES `Location`(`id`)

# );


def get_all_employees():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id,
            l.name location_name,
            l.address location_address
        FROM employee e
        JOIN location l
        ON l.id = e.location_id
        """
        )

        # Initialize an empty list to hold all employee representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an employee instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            employee = Employee(
                row["id"],
                row["name"],
                row["address"],
                row["location_id"],
            )
            location = Location(
                row["id"], row["location_name"], row["location_address"]
            )
            employee.location = location.__dict__

            employees.append(
                employee.__dict__
            )  # see the notes below for an explanation on this line of code.

    return employees


def get_single_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.id = ?
        """,
            (id,),
        )
        data = db_cursor.fetchone()

        employee = Employee(
            data["id"],
            data["name"],
            data["address"],
            data["location_id"],
        )
        return employee.__dict__


def create_employee(employee):
    max_id = EMPLOYEES[-1]["id"]
    new_id = max_id + 1
    employee["id"] = new_id
    EMPLOYEES.append(employee)
    return employee


def delete_employee(id):
    employee_index = -1
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            employee_index = index
    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)


def update_employee(id, new_employee):
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            EMPLOYEES[index] = new_employee
            break


def get_employees_by_location(location_id):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.location_id = ?
        """,
            (location_id,),
        )

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(
                row["id"],
                row["name"],
                row["address"],
                row["location_id"],
            )

            employees.append(
                employee.__dict__
            )  # see the notes below for an explanation on this line of code.

    return employees
