from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from scraper.models import PropertyData, OwnerData, PreviousFilings, TruePeopleData, Event, PhoneNumber
from django.http import JsonResponse, HttpResponseBadRequest
import json
import tkinter as tk
from tkinter import ttk
from django.db.models import Case, When, Value, IntegerField
import subprocess


# Create your views here.
def index(request):
    properties = PropertyData.objects.filter(deleted=False)

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
        
    print(properties_by_zip)

    return render(request, 'viewer/index.html', {
        'properties_by_zip': properties_by_zip
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

    return render(request, 'viewer/property.html', {
            'property': property,
            'owners': owners,
            'previous_filings': previous_filings,
            'true_people_data': true_people_data,
            'phone_numbers': phone_numbers
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
        event.note = note if note else None
        
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

import tkinter as tk
from tkinter import ttk  # Import ttk module for ComboBox
from django.http import JsonResponse
import json
import subprocess

def call(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mode = data['mode']

        if mode == 'queue':
            owner = OwnerData.objects.get(id=data['owner'])
            # Assuming you have the updated queryset with ordering as previously described
            numbers = PhoneNumber.objects.filter(owner=owner).exclude(state='disconnected')\
                                         .annotate(custom_order=Case(
                                             When(state='active', then=Value(1)),
                                             When(state='unknown', then=Value(2)),
                                             default=Value(3),
                                             output_field=IntegerField()))\
                                         .order_by('custom_order').iterator()

            def update_state():
                if current_number:
                    set_state(current_number.id, state_var.get())

            def set_state(phone_number_id, state):
                # Assuming PhoneNumber model and state updating logic is correctly implemented
                number = PhoneNumber.objects.get(id=phone_number_id)
                number.state = state
                number.save()

            def proceed_to_next_number():
                update_state()  # Update the state when proceeding to the next number
                nonlocal current_number
                current_number = next(numbers, None)
                if current_number:
                    display_number(current_number.number)
                    call_number(current_number.number)                    
                else:
                    root.destroy()  # Close the window if there are no more numbers

            def end_program():
                update_state()  # Ensure state is updated before closing
                root.destroy()  # Immediately exit the GUI

            def display_number(number, state):
                text.delete('1.0', tk.END)  # Clear the existing text
                text.insert(tk.END, f"Calling {number} State: {state}")  # Display the new number

            def call_number(number):
                clean_number = number.translate({ord(c): None for c in " ()-"})
                subprocess.call(["C:\\Users\\philip chopp\\AppData\\Local\\MicroSIP\\microsip.exe", clean_number])

            # Set up the Tkinter GUI
            root = tk.Tk()
            root.geometry("400x300")  # Adjust size for better appearance and to accommodate dropdown
            root.title("Call Queue")
            root.configure(bg="#f0f0f0")  # Set a light background color

            # Dropdown for state selection
            state_var = tk.StringVar(root)
            state_dropdown = ttk.Combobox(root, textvariable=state_var, state="readonly",
                                          values=["active", "disconnected", "unknown"])
            state_dropdown.pack(pady=5)
            state_dropdown.set("active")  # Default value

            # Add a Set State button to apply the selected state
            set_state_button = tk.Button(root, text="Set State", command=update_state)
            set_state_button.pack(pady=5)

            # Style the buttons and text widget as before
            button_style = {'font': ('Helvetica', 12), 'bg': '#d9d9d9', 'padx': 10, 'pady': 5}
            next_button = tk.Button(root, text="Next", command=proceed_to_next_number, **button_style)
            next_button.pack(pady=10)
            end_button = tk.Button(root, text="End", command=end_program, **button_style)
            end_button.pack(pady=5)

            text = tk.Text(root, height=5, width=50, font=('Helvetica', 12), bg="#ffffff")
            text.pack(pady=10)

            current_number = next(numbers, None)
            if current_number:
                display_number(current_number.number, current_number.state)
                call_number(current_number.number)

            root.mainloop()

        return JsonResponse({'message': 'Success'})


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