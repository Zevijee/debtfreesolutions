from django.contrib import admin
from .models import PropertyData, OwnerData, PreviousFilings, Event, TruePeopleData

# Register your models here.
admin.site.register(PropertyData)
admin.site.register(OwnerData)
admin.site.register(PreviousFilings)
admin.site.register(Event)
admin.site.register(TruePeopleData)


