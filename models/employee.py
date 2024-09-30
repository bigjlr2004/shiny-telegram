# CREATE TABLE `Employee` (
# 	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
# 	`name`	TEXT NOT NULL,
# 	`address`	TEXT NOT NULL,
# 	`location_id` INTEGER NOT NULL,
# 	FOREIGN KEY(`location_id`) REFERENCES `Location`(`id`)

# );


class Employee:
    def __init__(self, id, name, address, location_id):
        self.id = id
        self.name = name
        self.address = address
        self.location_id = location_id
        self.location = None
