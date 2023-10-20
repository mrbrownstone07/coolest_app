import os
import json
import requests
from django.conf import settings
from api.models.districts import District
from api.models.forecasts import Forecast
from django.core.management.base import BaseCommand


FILE_PATH = os.path.join(settings.BASE_DIR, 'forecast.json')

class Command(BaseCommand):
    help = "Pulls weather forecast data from the API and Pushes into DB."
    def handle(self, *args, **options):
        fetch_weather_data()
    
def fetch_weather_data():
    API_ENDPOINT = "https://api.open-meteo.com/v1/forecast"
    # f = open(FILE_PATH, encoding='utf-8')
    # forecast_data = json.load(f)
    
    districts = District.objects.all()
    latitudes= []
    longitudes = []
    
    for district in districts:
        latitudes.append(str(district.latitude))
        longitudes.append(str(district.longitude))
        
    request_url = f"{API_ENDPOINT}?latitude={','.join(latitudes)}&longitude={','.join(longitudes)}&forecast_days=16&hourly=temperature_2m"
    response = requests.get(request_url)
    forecast_data = response.json()
    
    for data, district in zip(forecast_data, districts):
        for time, temperature in zip(data['hourly']['time'], data['hourly']['temperature_2m']):
            print(f"Temperature: {temperature}, Time: {time}, District: {district.name}, PK: {district.id}")
            forecast = Forecast(
                temperature=temperature,
                forecast_time=time,
                district=district
            )
            forecast.save()
            
        
 
    
    
    
        
        
    
    
    
    
