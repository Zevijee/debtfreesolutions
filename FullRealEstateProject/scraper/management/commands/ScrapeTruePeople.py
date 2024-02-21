from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from .helper_functions import compare_names, check_if_company, change_ip, check_for_captcha, random_wait
import time
from django.db.models import Q
from scraper.models import OwnerData, TruePeopleData, PhoneNumber
import traceback
from bs4 import BeautifulSoup

class TruePeopleScraper:
    def __init__(self, url, address, zip_code, owner_name, owner_id):
        self.url = url
        self.address = address
        self.zip_code = zip_code
        self.owner_name = owner_name
        self.name_links = {}
        self.name_scores = {}
        self.driver = self.create_driver()
        self.owner_id = owner_id

    def create_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=C:\\Users\\Philip chopp\\AppData\\Local\\Google\\Chrome\\User Data\\")
        options.add_argument("--profile-directory=Profile 8")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)
        return driver

    def get_all_the_owner_containers(self):
        for i in range(2):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2)")
            random_wait(1)
        containers = self.driver.find_elements(By.CSS_SELECTOR, "div.card.card-body.shadow-form.card-summary.pt-3, div.card.card-body.shadow-form.card-summary.pt-3 > div.card-body")
        if not containers:
            if not check_for_captcha():
                self.driver.quit()
                raise Exception("No containers found")
            else:
                self.get_all_the_owner_containers()
        for container in containers:
            name = container.find_element(By.CSS_SELECTOR, "div.h4").text
            link_element = container.find_element(By.CSS_SELECTOR, "a.detail-link")
            link = link_element.get_attribute('href')
            self.name_links[name] = link
        next_page_elements = self.driver.find_elements(By.ID, 'btnNextPage')
        if next_page_elements:
            random_wait(2)
            next_page_elements[0].click()
            random_wait(2)
            self.get_all_the_owner_containers()
        else:
            return True

    def scrape(self):
        self.driver.get('https://www.truepeoplesearch.com/')
        time.sleep(4)
        self.driver.get(self.url)
        self.get_all_the_owner_containers()
        for name in self.name_links:
            score = compare_names(name, self.owner_name)
            self.name_scores[name] = score
        highest_score = max(self.name_scores.values())
        highest_score_names = [name for name, score in self.name_scores.items() if score == highest_score]
        owner = highest_score_names[0]
        self.driver.get(self.name_links[owner])
        person_details = self.driver.find_element(By.XPATH, '//*[@id="personDetails"]')
        time.sleep(10)
        html = person_details.get_attribute("innerHTML")
        self.driver.quit()
        
        soup = BeautifulSoup(html, 'html.parser')

            # List of identifiable parts of the href attributes for links to remove
        unwanted_links = [
            "/send?pid=1&tc=detail-top-pf",
            "/send?pid=40&tc=detail-bottom-bf",
            "/send?pid=1&tc=detail-inside-pf-crim",
        ]
            
        for link_part in unwanted_links:
            for a in soup.find_all('a', href=lambda href: href and link_part in href):
                # Find the parent 'div' of the 'a' tag
                parent_div = a.find_parent('div')
                if parent_div:
                    higher_parent_div = parent_div.find_parent('div')  # Second parent div, outside the first one
                    for _ in range(3):
                        if higher_parent_div:
                            higher_parent_div = higher_parent_div.find_parent('div')
                    if higher_parent_div:
                        higher_parent_div.decompose()

        for hr in soup.find_all('hr'):
            hr.decompose()

        for button in soup.find_all('button'):
            button.decompose()

        for atag in soup.find_all('a'):
            atag['href'] = f"https://www.truepeoplesearch.com{atag['href']}"
            atag['target'] = '_blank'

        # Get the text from all the <a> tags with class "dt-hd link-to-more olnk"
        owner_instance = OwnerData.objects.get(id=self.owner_id)
        
        for a in soup.find_all(attrs={"itemprop": "telephone"}):
            phone_number = PhoneNumber(owner=owner_instance, number=a.text)
            phone_number.save()            
        
        # Convert the soup back to a string without the unwanted sections
        modified_html = str(soup)

        # Remove <div class="h5">Sponsored Links</div>
        modified_html = modified_html.replace('<div class="h5">\nSponsored Links\n</div>', '')

        return modified_html, owner

class Command(BaseCommand):
    help = 'Scrapes data from TruePeopleSearch and updates database for owners without TruePeopleData'

    def handle(self, *args, **kwargs):
        # Fetch owners without associated TruePeopleData
        owners_without_true_people_data = OwnerData.objects.filter(
            true_people_data__isnull=True
        )

        for owner in owners_without_true_people_data:
            address = owner.address  # Assuming the owner's address is suitable for scraping
            zip_code = "11691"
            owner_name = owner.name
            owner_id = owner.id

            
            if not check_if_company(owner_name):
                print(f"{owner_name} is a company.")
                TruePeopleData.objects.create(owner=owner, data='this is a company')
                continue
            
            
            # Generate the URL based on the owner's details
            encoded_address = address.replace(" ", "%20").replace("\n", " ").replace("-", "")

            url= f"https://www.truepeoplesearch.com/resultaddress?streetaddress={encoded_address}&citystatezip=11691"

            # Initialize the scraper with the owner's details
            scraper = TruePeopleScraper(url, address, zip_code, owner_name, owner_id)
            try:
                html, scraped_owner_name = scraper.scrape()

                if not html:
                    print(f"No data found for {scraped_owner_name}. Skipping data save.")
                    continue
                
                TruePeopleData.objects.create(owner=owner, data=html, data_found=True)
                self.stdout.write(self.style.SUCCESS(f'Successfully scraped and saved data for {scraped_owner_name} real name is {owner_name}.'))
                
            except Exception as e:
                if "No containers found" in str(e):
                    print(f"No data found for {owner_name}. Skipping data save.")
                    TruePeopleData.objects.create(owner=owner, data='No data found')
                    continue
                                
                traceback.print_exc()
                while True:
                    i = input("Do you want to continue? (y/n): ")
                    if i == "y":
                        break
                    elif i == "n":
                        return
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")