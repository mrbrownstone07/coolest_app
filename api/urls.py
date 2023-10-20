from django.urls import path
from api.views import CoolestDistrictsView


urlpatterns = [
    path("coolest-districts", CoolestDistrictsView.as_view(), name='coolest-districts'),
]