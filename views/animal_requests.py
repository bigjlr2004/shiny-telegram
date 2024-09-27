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
    return ANIMALS


def get_single_animal(id):
    requested_animal = None
    for animal in ANIMALS:
        if animal["id"] == id:
            requested_animal = animal
    return requested_animal


def create_animal(animal):
    # Get the id value of the last animal in the list
    max_id = ANIMALS[-1]["id"]
    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an 'id' property to the animal dictionary
    animal["id"] = new_id

    # Add the animal dictionary to the list
    ANIMALS.append(animal)

    # Return the dictionary with 'id' property added
    return animal


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
    # Iterate the ANIMALS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, animal in enumerate(ANIMALS):
        if animal["id"] == id:
            # Found the animal. Update the value.
            ANIMALS[index] = new_animal
            break
