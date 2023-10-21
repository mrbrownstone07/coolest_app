import os
import json
import requests
from datetime import datetime, time
from django.conf import settings
from django.db.transaction import atomic
from api.models.districts import District
from api.models.forecasts import Forecast
from django.core.management.base import BaseCommand

TIME = time(hour=14, minute=00)

class Command(BaseCommand):
    help = "Pulls weather forecast data from the API and Pushes into DB."
    def handle(self, *args, **options):
        fetch_weather_data()
    
def fetch_weather_data():
    API_ENDPOINT = "https://api.open-meteo.com/v1/forecast"
    latitudes= []
    longitudes = []
    districts = District.objects.all()
    
    for district in districts:
        latitudes.append(str(district.latitude))
        longitudes.append(str(district.longitude))
        
    request_url = f"{API_ENDPOINT}?latitude={','.join(latitudes)}&longitude={','.join(longitudes)}&forecast_days=16&hourly=temperature_2m&timezone=Asia/Dhaka"
    response = requests.get(request_url)
    forecast_data = response.json()
    
    with atomic():
        forecasts = []
        for data, district in zip(forecast_data, districts):
            for datetimestamp, temperature in zip(data['hourly']['time'], data['hourly']['temperature_2m']):
                datestamp, timestamp = datetimestamp.split('T')
                print(f"Temperature: {temperature}, Date: {datestamp}, Time: {timestamp}, District: {district.name}, PK: {district.id}")              
                if temperature and datetime.strptime(timestamp, '%H:%M').time() == TIME:
                    forecast = Forecast(
                        temperature=temperature,
                        forecast_date=datetime.strptime(datestamp, '%Y-%m-%d'),
                        forecast_time=datetime.strptime(timestamp, '%H:%M').time(),
                        district=district
                    )
                    forecasts.append(forecast)          
        Forecast.objects.bulk_create(forecasts)
                
        
 
    
    
    
        
        
    
    
    
    
