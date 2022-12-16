import csv
import urllib3

import requests
from bs4 import BeautifulSoup


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://uz.post/uz/otdeleniya"

def clear_string(s: str):
    return " ".join(s.split())

def main():
    postal_codes = []

    res = requests.get(URL, verify=False)

    soup = BeautifulSoup(res.content, 'html.parser')

    table = soup.find(id="myTable")

    if not table:
        print("Postal codes not found!")
        return -1
    
    items = table.find_all("tr", class_="shop-item")


    for item in items:
        # Name
        name = item.find(class_="balun_header").get_text().strip()
        name = clear_string(name)
        
        info_box = item.find(class_="balun_body")

        # Address
        address = info_box.select_one("div").extract()
        address.select_one("strong").extract()
        address = address.get_text().strip()
        address = clear_string(address)

        # Phone number
        phone_number = info_box.select_one('div').extract()
        phone_number.select_one("strong").extract()
        phone_number = phone_number.get_text().strip()

        # Region
        region = info_box.select_one('div').extract()
        region.select_one("strong").extract()
        region = region.get_text().strip()
        
        # ! Working time
        info_box.select_one('div').extract() 

        # Postal code
        info_box.select_one("strong").extract()
        code = info_box.get_text().strip()

        # Location
        location_box = item.find("input")
        lat = location_box["data-coor1"]
        lng = location_box["data-coor2"]


        postal_codes.append({
            "name": name,
            "code": code,
            "address": address,
            "phone_number": phone_number,
            "region": region,
            "lat": lat,
            "lng": lng,
        })


        # Save to csv
        fieldnames = ["name", "code", "address", 
                "phone_number", "region", 
                "lat", "lng"]
        with open("postal_codes.csv", 'w', encoding='UTF8', newline='') as file:

            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='|')
            writer.writeheader()
            writer.writerows(postal_codes)




if __name__ == "__main__":
    main()