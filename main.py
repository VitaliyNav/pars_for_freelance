import csv
import requests
from bs4 import BeautifulSoup

updates = input("How many updates? ")

# Validate the input
try:
    updates = int(updates)
    if updates <= 0:
        raise ValueError
except ValueError:
    print("Invalid input. Please enter a positive integer for the number of updates.")
    input("press Enter")
    exit()

# Open the CSV file for writing with UTF-8 encoding
with open("output.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)

    # Write column headers
    writer.writerow(["First Name", "Last Name", "Address", "City", "Postcode", "BIC", "IBAN"])

    # Perform the specified number of updates
    for i in range(updates):
        print(f"Update {i+1}")
        # Send a GET request to the target web page
        url = "https://fakeit.receivefreesms.co.uk/c/de/"
        response = requests.get(url)

        # Check the response status code (200 means a successful request)
        if response.status_code == 200:
            # Create a BeautifulSoup object with the response content
            soup = BeautifulSoup(response.content, "html.parser")

            # Find the necessary elements on the page using CSS selectors
            table = soup.select_one("body > div.content > div:nth-child(1) > div > div.col-xl-12.col-lg-12.col-md-12.col-sm-12.col-12 > div > div.card-body > div > table")
            Name = table.select_one("tbody > tr:nth-child(1) > td:nth-child(4) > span")
            Address = table.select_one(" tbody > tr:nth-child(2) > td.copy > span")
            City = table.select_one(" tbody > tr:nth-child(3) > td:nth-child(2) > span")
            Postcode = table.select_one("tbody > tr:nth-child(3) > td:nth-child(4) > span")
            BIC = soup.select_one("body > div.content > div:nth-child(2) > div > div.col-xl-12.col-lg-12.col-md-12.col-sm-12.col-12 > div > div.card-body > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > span")
            IBAN = soup.select_one("#iban")

            # Extract the text from the found elements
            if Name:
                full_name = Name.text.strip()
                # Split the full name into first name and last name
                first_name, last_name = full_name.split(' ')
            if Address:
                address = Address.text.strip()
            if City:
                city = City.text.strip()
            if Postcode:
                postcode = Postcode.text.strip()
            if BIC:
                bic = BIC.text.strip()
            if IBAN:
                iban = IBAN.text.strip()

            # Write the data to the CSV file
            writer.writerow([first_name, last_name, address, city, postcode, bic, iban])

        else:
            print(f"Error: {response.status_code}")


input("DONE")