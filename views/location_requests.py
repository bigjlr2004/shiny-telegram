import json
import sqlite3
from models import Location, Employee, Animal

LOCATIONS = [
    {"id": 1, "name": "Nashville North", "address": "8422 Johnson Pike"},
    {"id": 2, "name": "Nashville South", "address": "209 Emory Drive"},
]


def get_all_locations():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l
        """
        )

        # Initialize an empty list to hold all location representations
        locations = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an location instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            location = Location(row["id"], row["name"], row["address"])

            locations.append(
                location.__dict__
            )  # see the notes below for an explanation on this line of code.

    return locations


def get_single_location(id):
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l
        WHERE l.id = ?
        """,
            (id,),
        )

        data = db_cursor.fetchone()

        # Create a location instance from the current row
        location = Location(data["id"], data["name"], data["address"])

        db_cursor.execute(
            """
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
            FROM employee e
            WHERE e.location_id = ?
        """,
            (id,),
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
            employees.append(employee.__dict__)

        db_cursor.execute(
            """
            SELECT
                a.id,
                a.name,
                a.breed,
                a.status,
                a.location_id,
                a.customer_id
            FROM animal a
            WHERE a.location_id = ?
            """,
            (id,),
        )
        animals = []

        dataset = db_cursor.fetchall()
        for row in dataset:
            animal = Animal(
                row["id"],
                row["name"],
                row["breed"],
                row["status"],
                row["location_id"],
                row["customer_id"],
            )
            animals.append(animal.__dict__)

    location.animals = animals
    location.employees = employees
    return location.__dict__


def create_location(location):
    max_id = LOCATIONS[-1]["id"]
    new_id = max_id + 1
    location["id"] = new_id
    LOCATIONS.append(location)
    return location


def delete_location(id):
    location_index = -1
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            location_index = index
    if location_index >= 0:
        LOCATIONS.pop(location_index)


def update_location(id, new_location):
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            LOCATIONS[index] = new_location
            break
