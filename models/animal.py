class Animal:

    # Class initializer. It has five custom parameters,  with the
    # special self parameter that every method on a class
    # needs as it's first parameter.
    def __init__(self, id, name, breed, status, location_id, customer_id):
        self.id = id
        self.name = name
        self.breed = breed
        self.status = status
        self.location_id = location_id
        self.customer_id = customer_id
        self.location = None
        self.customer = None
