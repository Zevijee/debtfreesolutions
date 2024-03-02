from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from scraper.models import ForeclosureData
from bs4 import BeautifulSoup

class Command(BaseCommand):
    help = 'Scrape forclosures'

    def handle(self, *args, **options):
        options = Options()
        options.add_argument("--user-data-dir=C:/Users/philip chopp/AppData/Local/Google/Chrome/User Data")
        options.add_argument("--profile-directory=Default")

        driver = webdriver.Chrome(options=options)
        driver.get('https://www.propertyshark.com/mason/NY/New-York-City/Foreclosures')

        f = 0

        while True:
            i = input('press s to start scraping')
            if i == 's':
                break
            else:
                continue

        while True:
            print('Scraping page', f+1)
            element = driver.find_element(By.ID, "DataContainerAjax")
            properties = element.find_element(By.CLASS_NAME, "properties")
            print(properties.text)

            # Assuming 'html_content' is a variable containing the HTML source you provided
            soup = BeautifulSoup(properties.text, 'lxml')

            # Find all property listings
            property_listings = soup.find_all('li', class_='property')

            for property in property_listings:

                print(property)
                
                # Extracting data using BeautifulSoup
                address = property.find('div', class_='address').get_text(strip=True) if property.find('div', class_='address') else None
                auction_date = property.find(itemprop='startDate')['content'] if property.find(itemprop='startDate') else None
                auction_time = property.find(itemprop='name', content=True)['content'] if property.find(itemprop='name', content=True) else None
                auction_location = property.find(itemprop='location').get_text(strip=True) if property.find(itemprop='location') else None
                date_added = property.find('th', text='Date added').find_next_sibling('td').get_text(strip=True) if property.find('th', text='Date added') else None
                plaintiff = property.find('th', text='Plaintiff').find_next_sibling('td').get_text(strip=True) if property.find('th', text='Plaintiff') else None
                defendant = property.find('th', text='Defendant').find_next_sibling('td').get_text(strip=True) if property.find('th', text='Defendant') else None
                lien = property.find(itemprop='price')['content'] if property.find(itemprop='price') else None
                judgment = property.find('th', text='Judgment').find_next_sibling('td').get_text(strip=True) if property.find('th', text='Judgment') else None
                index_no = property.find('th', text='Index no.').find_next_sibling('td').get_text(strip=True) if property.find('th', text='Index no.') else None
                referee = property.find('th', text='Referee').find_next_sibling('td').get_text(strip=True) if property.find('th', text='Referee') else None
                plaintiff_attorney = property.find('th', text='Plaintiff\'s attorney').find_next_sibling('td').get_text(strip=True) if property.find('th', text='Plaintiff\'s attorney') else None
                plaintiff_attorney_phone = property.find('a', href=True).get_text(strip=True) if property.find('a', href=True) else None
                foreclosure_type = property.find('th', text='Foreclosure type').find_next_sibling('td').get_text(strip=True) if property.find('th', text='Foreclosure type') else None
                auction_notes = property.find('th', text='Auction notes').find_next_sibling('td').get_text(strip=True) if property.find('th', text='Auction notes') else None
                unit_number = property.find('th', text='Unit number').find_next_sibling('td').get_text(strip=True) if property.find('th', text='Unit number') else None
                previously_scheduled_on = property.find('th', text='Previously scheduled on').find_next_sibling('td').get_text(strip=True) if property.find('th', text='Previously scheduled on') else None

                # Creating ForeclosureData instance
                foreclosure_data = ForeclosureData(
                    address=address,
                    auction_date=auction_date,
                    auction_time=auction_time,
                    auction_location=auction_location,
                    date_added=date_added,
                    plaintiff=plaintiff,
                    defendant=defendant,
                    lien=lien,
                    judgment=judgment,
                    index_no=index_no,
                    referee=referee,
                    plaintiff_attorney=plaintiff_attorney,
                    plaintiff_attorney_phone=plaintiff_attorney_phone,
                    foreclosure_type=foreclosure_type,
                    auction_notes=auction_notes,
                    unit_number=unit_number,
                    previously_scheduled_on=previously_scheduled_on
                )

                # Save the instance to the database
                foreclosure_data.save()

                print(f'Foreclosure data for {address} saved to the database')