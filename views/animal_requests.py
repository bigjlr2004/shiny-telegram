import sqlite3
import json
from models import Animal, Location, Customer


ANIMALS = [
    {
        "id": 1,
        "name": "Snickers",
        "species": "Dog",
        "locationId": 1,
        "customerId": 4,
        "status": "Admitted",
    },
    {
        "id": 2,
        "name": "Roman",
        "species": "Dog",
        "locationId": 1,
        "customerId": 2,
        "status": "",
    },
    {
        "id": 3,
        "name": "Blue",
        "species": "Cat",
        "locationId": 2,
        "customerId": 1,
        "status": "",
    },
    {
        "id": 4,
        "name": "Eleanor",
        "species": "Dog",
        "location": 1,
        "customerId": 2,
        "status": "",
    },
]


def get_all_animals():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a black box
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL Query to get the information you want
        db_cursor.execute(
            """
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name location_name,
            l.address location_address,
            c.id customer_id,
            c.name customer_name,
            c.address customer_address
            
        FROM Animal a
        JOIN Location l
        ON l.id = a.location_id
        JOIN Customer c
        ON c.id = a.customer_id
            """
        )

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order if the parameters defined in the
            # Animal class above.
            animal = Animal(
                row["id"],
                row["name"],
                row["breed"],
                row["status"],
                row["location_id"],
                row["customer_id"],
            )

            # Create a location instance from the current row
            location = Location(
                row["id"], row["location_name"], row["location_address"]
            )

            # Create a location instance from the current row
            customer = Customer(
                row["customer_id"], row["customer_name"], row["customer_address"]
            )

            # Add the dictionary representation of the location to the animal
            animal.location = location.__dict__

            # Add the dictionary representation of the customer to the animal
            animal.customer = customer.__dict__

            animals.append(animal.__dict__)

    return animals


def get_single_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # USE a ? parameter to inject a variables value
        # into the SQL statement
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
                          WHERE a.id = ?
        """,
            (id,),
        )

        # load the single result into memory
        data = db_cursor.fetchone()

        # create an animal instance from the current row
        animal = Animal(
            data["id"],
            data["name"],
            data["breed"],
            data["status"],
            data["location_id"],
            data["customer_id"],
        )

        return animal.__dict__


def create_animal(new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
         INSERT INTO animal 
            (name, breed, status, location_id, customer_id )
        VALUES
            (?,?,?,?,?);
        """,
            (
                new_animal["name"],
                new_animal["breed"],
                new_animal["status"],
                new_animal["location_id"],
                new_animal["customer_id"],
            ),
        )

        # The lastrowid property on the cursor will return
        # the primary key of the last thing that added to the
        # database.
        id = db_cursor.lastrowid
        new_animal["id"] = id
    return new_animal


def delete_animal(id):
    # Initialize animal_index as -1 in case one isn't found
    animal_index = -1

    # Iterate the animals list, but use enumerate() so that you can access
    # the index of each item

    for index, animal in enumerate(ANIMALS):
        if animal["id"] == id:
            animal_index = index
    # If the animal was found, use pop(int) to remove it from the list
    if animal_index >= 0:
        ANIMALS.pop(animal_index)


def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        UPDATE Animal
        SET 
            name = ?,
            breed = ?,
            status = ?,
            location_id = ?,
            customer_id = ?
        WHERE id = ?
        """,
            (
                new_animal["name"],
                new_animal["breed"],
                new_animal["status"],
                new_animal["location_id"],
                new_animal["customer_id"],
                id,
            ),
        )

        # Where any rows affected?
        # Did the client send an id that exists?
        rows_affected = db_cursor.rowcount

    # Return value of this function
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def get_animals_by_location(location_id):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
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
            (location_id,),
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
    return animals


def get_animals_by_status(status):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
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
                          WHERE a.status = ?
        """,
            (status,),
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
    return animals
