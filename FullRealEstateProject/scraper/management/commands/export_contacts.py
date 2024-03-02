import csv
from django.core.management import BaseCommand
from scraper.models import PhoneNumber

class Command(BaseCommand):
    help = 'Export owner names and phone numbers to CSV'

    def handle(self, *args, **options):
        with open('phone_numbers.csv', 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Number', 'Address']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            phone_numbers = PhoneNumber.objects.select_related('owner').all()

            for phone_number in phone_numbers:
                number = phone_number.number

                number = number.replace('(', '')
                number = number.replace(')', '')
                number = number.replace('-', '')
                number = number.replace(' ', '')

                name = phone_number.owner.name

                name.replace(',', '')

                zip_code = phone_number.owner.property.zip_code
                address = phone_number.owner.property.address + ', ' + zip_code
                
                writer.writerow({'Name': f'{name} | {address}', 'Number': number, 'Address': address})