class Customer:

    # CREATE TABLE `Customer` (
    #     `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    #     `name`    TEXT NOT NULL,
    #     `address`    TEXT NOT NULL,
    #     `email`    TEXT NOT NULL,
    #     `password`    TEXT NOT NULL
    # );

    def __init__(self, id, name, address, email, password):
        self.id = id
        self.name = name
        self.address = address
        self.email = email
        self.password = password
