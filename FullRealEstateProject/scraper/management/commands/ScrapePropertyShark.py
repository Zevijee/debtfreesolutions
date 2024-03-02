from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pynput import mouse
import os
import traceback
import time
import sys
from scraper.models import PropertyData, OwnerData, PreviousFilings
from selenium.webdriver.common.by import By

class Command(BaseCommand):
    
    help = 'Description of your command'
    def add_arguments(self, parser):
        parser.add_argument('zip_code', type=str, help='Zip code to scrape')

    def handle(self, *args, **options):
        if 'zip_code' in options:
            self.zip_code = options['zip_code']
        else:
            print("the way to use this command is: python manage.py ScrapePropertyShark <zip_code>")
            sys.exit(1)

        # Wait for right-click to start scraping
        self.wait_for_click()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        chrome_options = Options()
        profile_path = 'C:/Users/philip chopp/AppData/Local/Google/Chrome/User Data/'
        chrome_options.add_argument(f"user-data-dir={os.path.dirname(profile_path)}")
        chrome_options.add_argument(f'--profile-directory=Default')  # Assuming "Default" profile

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://www.propertyshark.com/mason/ny/New-York-City/Maps")
        

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.right:
            if pressed:
                pass
            else:
                return False

    def wait_for_click(self):
        print("Right-click to scrape a property.")
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()
            self.scrape()

    def scrape(self):
        print("Scraping started.")
        time.sleep(1)  # Wait for the page to load

        try:
            address, report_data, owner_data, previous_filings = self.find_elements()

            # Check if property already exists
            if PropertyData.objects.filter(address=address).exists():
                print(f"Property with address {address} already exists in database. Skipping data save.")

            else:
                self.save_data(address, report_data, owner_data, previous_filings)
                print(f"Data scraped and saved for address: {address}")

        except Exception as e:
            print("An error occurred during scraping.")
            traceback.print_exc()

        self.wait_for_click()

    def find_elements(self):
        report_tables = self.driver.find_elements(By.CLASS_NAME, "report_table")
        owner_tables = self.driver.find_elements(By.CLASS_NAME, "block")
        previous_fillings_table = self.driver.find_elements(By.XPATH, '//*[@id="mapcontainer"]/div[7]/div[3]/table[1]')
        address = self.driver.find_element(By.XPATH, '//*[@id="mapcontainer"]/div[7]/div[2]/h3/a').text

        reports = [self.parse_table(table) for table in report_tables]
        report_data = {k: v for d in reports for k, v in d.items()}
        owners = []
        owner_data = {}

        for table in owner_tables:
            try:
                owner = self.parse_table(table)
                owners.append(owner)  # This line is optional if you still need the 'owners' list for other purposes
                owner_data[owner["Name"]] = owner["Address"]
            except Exception as e:
                print("Error parsing owner table:", e)

        previous_filings = {}
        if previous_fillings_table:
            rows = previous_fillings_table[0].find_elements(By.TAG_NAME, "tr")
            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                date, amount = cells[1].text.strip(), cells[2].text.strip()
                previous_filings[date] = amount

        report_data["Special factors"] = report_data.get("Special factors", "None Listed").replace("\n", " ")

        return address, report_data, owner_data, previous_filings

    def parse_table(self, table_element):
        rows = table_element.find_elements(By.TAG_NAME, "tr")
        return {row.find_element(By.TAG_NAME, "th").text.strip(): row.find_element(By.TAG_NAME, "td").text.strip() for row in rows}

    def save_data(self, address, report_data, owner_data, previous_filings):
        mapped_data = {
            'address': address or None,
            'block_lot': report_data.get("Block & lot") or None,
            'arms_length': report_data.get("Arm's length") or None,
            'purchase_price': report_data.get("Purchase price") or None,
            'purchase_date': report_data.get("Purchase date") or None,
            'building_class': report_data.get("Building class") or None,
            'building_dimensions': report_data.get("Building dimensions") or None,
            'building_sqft': report_data.get("Building sqft") or None,
            'lot_sqft': report_data.get("Lot sqft") or None,
            'lot_dimensions': report_data.get("Lot dimensions") or None,
            'zoning_districts': report_data.get("Zoning districts") or None,
            'far_as_built': report_data.get("FAR as built") or None,
            'special_factors': report_data.get("Special factors") or None,
            'zip_code': self.zip_code
        }

        property_obj, created = PropertyData.objects.get_or_create(
            address=address, 
            defaults=mapped_data
        )

        for name, addr in owner_data.items():
            OwnerData.objects.create(property=property_obj, name=name, address=addr)

        for date, amount in previous_filings.items():
            PreviousFilings.objects.create(property=property_obj, filing_date=date, filing_amount=amount)

        print(f"Property {address} saved successfully.")