from random_address import real_random_address
import names
import requests
import time
import random

debug = True
url = "http://127.0.0.1:5000"

possible_update_attrs = ["name", "addr", "city", "pin"]

while True:
    # Get all students
    students = requests.get(url + "/students")

    # Select a random student
    selected_student = random.choice(students.json()["student_ids"])

    if debug:
        print(f"Selected student: {selected_student}")

    # Get the data for the selected student
    data = requests.get(url + "/students/" + str(selected_student)).json()

    # Select a random attribute to update from the possible options
    update_attr = random.choice(possible_update_attrs)

    if debug:
        print(f"Updating attr: {update_attr}")

    # Re-use existing fields, unless changed in the following steps
    addr = data["attributes"]["addr"]
    city = data["attributes"]["city"]
    pin = data["attributes"]["pin"]

    if update_attr == "name":
        name = names.get_full_name()

    else:
        # Re-use the name
        name = data["attributes"]["name"]
        p = possible_update_attrs.copy()
        p.remove("name")

        # Generate a new address and select a random field from the address to
        # update
        new_addr = real_random_address()
        update_addr_attr = random.choice(p)

        if update_addr_attr == "addr":
            addr = new_addr["address1"]
        elif update_addr_attr == "city":
            city = new_addr["city"]
        elif update_addr_attr == "pin":
            pin = new_addr["postalCode"]

    try:
        payload = {
            "name": name,
            "addr": addr,
            "city": city,
            "pin": pin,
        }

        r = requests.post(url + "/students/" + str(selected_student), data=payload)
        if debug:
            print(f"Status: {r.status_code}, Message: {r.json()}")
            print("")
    except KeyError as e:
        print(e)

    time.sleep(0.5)
