from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from views import (
    get_all_animals,
    get_single_animal,
    get_animals_by_location,
    get_animals_by_status,
    create_animal,
    delete_animal,
    update_animal,
    get_all_locations,
    get_single_location,
    create_location,
    delete_location,
    update_location,
    get_single_employee,
    get_all_employees,
    get_employees_by_location,
    create_employee,
    delete_employee,
    update_employee,
    get_all_customers,
    get_single_customer,
    create_customer,
    delete_customer,
    update_customer,
    get_customer_by_email,
)
import json

# Here's a class. It inherits from another class.
# For now think ofa class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.


class HandleRequests(BaseHTTPRequestHandler):
    # This is a docstring it should be at the beginning if all classes and functions.
    # IT gives a description of the class or function.
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""

    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split("/")  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        # Try to get the item at index 2
        pk = None
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            pk = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, pk)  # This is a tuple

    # Here's a class function
    def _set_headers(self, status):
        # Notice this DocString also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status(number): the status code to return to the front end"""
        self.send_response(status)
        self.send_header("Content-type", "application-json")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept"
        )
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        """Handles GET requests to the server"""

        # Set the response code to OK
        self._set_headers(200)
        response = {}  # Default response

        parsed = self.parse_url(self.path)
        # Parse the URL and capture the tuple that is returned
        if "?" not in self.path:
            (resource, id) = parsed

            # It's an if else statement
            if resource == "animals":
                if id is not None:
                    response = get_single_animal(id)
                else:
                    response = get_all_animals()
            elif resource == "locations":
                if id is not None:
                    response = get_single_location(id)
                else:
                    response = get_all_locations()
            elif resource == "employees":
                if id is not None:
                    response = get_single_employee(id)
                else:
                    response = get_all_employees()
            elif resource == "customers":
                if id is not None:
                    response = get_single_customer(id)
                else:
                    response = get_all_customers()
        else:  # there is a ? in the path, run the query param functions
            (resource, query) = parsed

            # see if the query dictionary has an email key
            if query.get("email") and resource == "customers":
                response = get_customer_by_email(query["email"][0])
            if query.get("location_id") and resource == "animals":
                response = get_animals_by_location(query["location_id"][0])
            if query.get("location_id") and resource == "employees":
                response = get_employees_by_location(query["location_id"][0])
            if query.get("status") and resource == "animals":
                response = get_animals_by_status(query["status"][0])

        # This weird code sends a response back to the client
        self.wfile.write(json.dumps(response).encode())

        # Here's a method on the class that overrides the parent's default
        # It handles any POST Request

    def do_POST(self):
        """Handles POST requests to the server"""
        self._set_headers(201)

        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new object to return
        new_object = None

        # Add anew animal to the list. Don't worry about the orange squiggle
        # you'll define the create animal function next.
        if resource == "animals":
            new_object = create_animal(post_body)
        elif resource == "locations":
            new_object = create_location(post_body)
        elif resource == "employees":
            new_object = create_employee(post_body)
        elif resource == "customers":
            new_object = create_customer(post_body)

        # Encode the new animal and send in response
        self.wfile.write(json.dumps(new_object).encode())

    def do_DELETE(self):
        # Set a 204 Response Code
        self._set_headers(204)
        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
        elif resource == "employees":
            delete_employee(id)
        elif resource == "customers":
            delete_customer(id)
        elif resource == "locations":
            delete_location(id)
        self.wfile.write("".encode())

    def do_PUT(self):

        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        # Delete a single animal from the list
        if resource == "animals":
            # will return either True or False from 'update_animal'
            success = update_animal(id, post_body)
        elif resource == "locations":
            update_location(id, post_body)
        elif resource == "customers":
            update_customer(id, post_body)
        elif resource == "employees":
            update_employee(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        # Encode the new animal and send in response
        self.wfile.write("".encode())


def main():
    """Starts the server on port 8080 using the HandleRequests class"""
    host = ""
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
