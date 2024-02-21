from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('property/<int:property_id>', views.property, name='property'),
    path('date/<str:date>', views.date, name='date'),
    path('call', views.call, name='call'),
    path('delete_event/<int:event_id>', views.delete_event, name='delete_event'),
    path('phone_number_config/<str:phone_number>', views.phone_number_config, name='phone_number_config'),
    path('return_properties', views.return_properties, name='return_properties'),
    path('return_owners', views.return_owners, name='return_owners'),
]