class Customer:

    # CREATE TABLE `Customer` (
    #     `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    #     `name`    TEXT NOT NULL,
    #     `address`    TEXT NOT NULL,
    #     `email`    TEXT NOT NULL,
    #     `password`    TEXT NOT NULL
    # );

    # Email and password have default values of "" because
    # The reason for this is because when create some Customer instances
    # to send back the client, sending the password in the response is a bad idea.
    # Also, there's no reason to send the email in the case since the
    # client obviously already has the email address to reference.
    # Allows for the creation of a Customer instance with only three positional
    # arguments instead of needing all five.

    def __init__(self, id, name, address, email="", password=""):
        self.id = id
        self.name = name
        self.address = address
        self.email = email
        self.password = password
