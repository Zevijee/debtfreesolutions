from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from scraper.models import PropertyData, OwnerData, PreviousFilings, TruePeopleData, Event, PhoneNumber, currentZip
from django.http import JsonResponse, HttpResponseBadRequest
import json
import tkinter as tk
from tkinter import ttk
from django.db.models import Case, When, Value, IntegerField
import subprocess
import tkinter as tk
from tkinter import ttk  # Import ttk module for ComboBox
from django.http import JsonResponse
import json
import subprocess
import time
from datetime import datetime
import pytz

# Set the timezone to New York
new_york_tz = pytz.timezone('America/New_York')

# Get the current time in New York timezone
now_in_new_york = datetime.now(new_york_tz)

# Format the date and time in a 12-hour format including AM or PM
formatted_time = now_in_new_york.strftime('%Y-%m-%d %I:%M:%S %p')

print(formatted_time)


# Create your views here.
def index(request):
    properties = PropertyData.objects.filter(deleted=False)

    zippy = currentZip.objects.first().zip_code

    for p in properties:
        owners = OwnerData.objects.filter(property=p)
        for owner in owners:
            if TruePeopleData.objects.filter(owner=owner, data_found=False).exists():
                p.deleted = True
                p.save()
                break

    properties_by_zip = {}

    current_zip = ''
    for p in properties:
        current_zip = p.zip_code
        if current_zip not in properties_by_zip:
            properties_by_zip[current_zip] = [p]
        else:
            properties_by_zip[current_zip].append(p)
        
    # print(properties_by_zip)

    return render(request, 'viewer/index.html', {
        'properties_by_zip': properties_by_zip,
        'current_zip': zippy,
        })

def property(request, property_id):
    property = PropertyData.objects.get(pk=property_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create_note':
            note = request.POST.get('note')
            property.notes = note
            property.save()
        elif action == 'delete_property':
            property.deleted = True
            property.save()
            return redirect('index')

        return redirect('property', property_id=property_id)
    
    # Get the property

    # Get the owners
    owners = OwnerData.objects.filter(property=property)

    # Get the previous filings
    previous_filings = PreviousFilings.objects.filter(property=property)

    # Get the true people data
    true_people_data = TruePeopleData.objects.filter(owner__in=owners)
    
    # Get the telephone numbers
    phone_numbers = PhoneNumber.objects.filter(owner__in=owners)

    # Set the timezone to New York
    new_york_tz = pytz.timezone('America/New_York')

    # Get the current time in New York timezone
    now_in_new_york = datetime.now(new_york_tz)

    # Format the date and time in a 12-hour format including AM or PM
    current_date = now_in_new_york.strftime('%Y-%m-%d %I:%M:%S %p')

    return render(request, 'viewer/property.html', {
            'property': property,
            'owners': owners,
            'previous_filings': previous_filings,
            'true_people_data': true_people_data,
            'phone_numbers': phone_numbers,
            'current_date': current_date,
            })


def date(request, date):       
    if request.method == 'POST':
        event = Event(date=date)
        
        event_type = request.POST.get('action')
        event_date = request.POST.get('date')
        event_property = request.POST.get('property')
        owner = request.POST.get('owner')
        note  = request.POST.get('note')

        print(event_property)


        if not event_property:
            return render(request, 'viewer/date.html', {'date': date, 'error': 'Please select a property'})

        p = PropertyData.objects.filter(id=event_property).first()

        event.event = event_type
        event.date = event_date
        event.on_property = p
        event.owner = OwnerData.objects.filter(name=owner).first() if owner else None
        event.notes = note if note else None
        
        event.save()            

        return redirect('date', date=date)   

    # get all the events with this date
    events = Event.objects.filter(date=date)

    return render(request, 'viewer/date.html', {'date': date, 'events': events})

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    date = event.date
    event.delete()

    return redirect('date', date=date)





def phone_number_config(request, phone_number):
    number = PhoneNumber.objects.get(id=phone_number)
    print(number)

    if request.method == 'PUT':
        print('PUT')
        data = json.loads(request.body)
        print(data)
        number.state = data['state']
        number.save()

        return JsonResponse({'message': 'Success'})

    data = {
        'id': number.id,
        'number': number.number,
        'state': number.state,
    }

    print(data)

    # Return the data as a JSON response
    return JsonResponse(data)

def return_properties(request):
    properties = PropertyData.objects.all()

    data = {}

    for p in properties:
        data[p.id] = {
            'address': p.address,
            'id': p.id,
        }

    return JsonResponse(data)

def return_owners(request):
    owners = OwnerData.objects.all()

    data = {}

    for o in owners:
        data[o.id] = {
            'data': o.name,
            'id': o.property.id,
        }

    return JsonResponse(data)

def test(request):
    return render(request, 'viewer/testing.html')

def update_zip(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        zip_code = data['zip_code']

        current_zip = currentZip.objects.first()
        current_zip.zip_code = zip_code
        current_zip.save()

        return JsonResponse({'message': 'Success'})