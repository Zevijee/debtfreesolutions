from django.db import models

class PropertyData(models.Model):
    address = models.CharField(max_length=255, unique=True)
    block_lot = models.CharField(max_length=100, blank=True, null=True)
    arms_length = models.CharField(max_length=100, blank=True, null=True)
    purchase_price = models.CharField(max_length=100, blank=True, null=True)
    purchase_date = models.CharField(max_length=100, blank=True, null=True)
    building_class = models.CharField(max_length=100, blank=True, null=True)
    building_dimensions = models.CharField(max_length=100, blank=True, null=True)
    building_sqft = models.CharField(max_length=100, blank=True, null=True)
    lot_sqft = models.CharField(max_length=100, blank=True, null=True)
    lot_dimensions = models.CharField(max_length=100, blank=True, null=True)
    zoning_districts = models.CharField(max_length=100, blank=True, null=True)
    far_as_built = models.CharField(max_length=100, blank=True, null=True)
    special_factors = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    zip_code = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.address

class PreviousFilings(models.Model):
    property = models.ForeignKey(PropertyData, on_delete=models.CASCADE, related_name='previous_filings')
    filing_date = models.CharField(max_length=100, blank=True, null=True)
    filing_amount = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.filing_date

class OwnerData(models.Model):
    property = models.ForeignKey(PropertyData, on_delete=models.CASCADE, related_name='owners')
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class TruePeopleData(models.Model):
    owner = models.ForeignKey(OwnerData, on_delete=models.CASCADE, related_name='true_people_data')
    data = models.TextField(blank=True, null=True)
    data_found = models.BooleanField(default=False)

    def __str__(self):
        return self.owner.name

class PhoneNumber(models.Model):
    owner = models.ForeignKey(OwnerData, on_delete=models.CASCADE, related_name='phone_numbers')
    number = models.CharField(max_length=100)
    called = models.BooleanField(default=False)
    state = models.CharField(max_length=100, default='unknown', blank=True, null=True)

class Event(models.Model):
    date = models.CharField(max_length=100)
    event_choices = [
        ('follow_up_call', 'follow up call'),
        ('reschedule_appointment', 'reschedule appointment'),
        ('needs_visit', 'needs visit'),
        ('property_appointment_scheduled', 'property appointment scheduled'),
        ('contract_signing', 'contract signing'),
        ('scheduled_appraisal', 'scheduled appraisal'),
        ('scheduled_inspection', 'scheduled inspection'),
        ('scheduled_cash_for_keys_negotiation', 'scheduled cash for keys negotiation'),
        ('scheduled_closing', 'scheduled closing'),
    ]

    event = models.CharField(choices=event_choices, max_length=100, blank=True, null=True)

    on_property = models.ForeignKey(PropertyData, on_delete=models.CASCADE, related_name='events', blank=True, null=True)
    owner = models.ForeignKey(OwnerData, on_delete=models.CASCADE, related_name='events', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)