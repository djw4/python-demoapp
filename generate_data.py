from random_address import real_random_address
import names
import requests

url = "http://127.0.0.1:5000/new"
create_addresses = 1000

for r in range(create_addresses):
  _name = names.get_full_name()
  addr = real_random_address()
  
  try:
    payload = {
      'name': _name,
      'city': addr["city"],
      'addr': addr["address1"],
      'pin': addr["postalCode"]
    }
    
    r = requests.post(url, data=payload)
    print(r.status_code)
  except KeyError as e:
    print(e)
