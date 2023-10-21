from django.urls import path
from api.views import get_coolest_districts, travel_suggestions


urlpatterns = [
    path("coolest-districts/", get_coolest_districts, name='coolest-districts'),
    path("travel-suggestions/", travel_suggestions, name='travel-suggestions'),
]