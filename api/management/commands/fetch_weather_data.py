import requests
from datetime import datetime, time
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

    for data, district in zip(forecast_data, districts):
        updates_by_forecast_date = {}
        for datetimestamp, temperature in zip(data['hourly']['time'], data['hourly']['temperature_2m']):
            datestamp, timestamp = datetimestamp.split('T')
            forecast_date = datetime.strptime(datestamp, '%Y-%m-%d').date()
            forecast_time = datetime.strptime(timestamp, '%H:%M').time()
            if temperature and datetime.strptime(timestamp, '%H:%M').time() == TIME:
                updates_by_forecast_date[forecast_date] = {'temperature': temperature, 'forecast_time': forecast_time}   
                             
        creates, updates = Forecast.bulk_update_or_create({'district': district}, 'forecast_date', updates_by_forecast_date)
        print(f"{district}: {creates} rows created, {updates} row updates!")
        
    
        
 
    
    
    
        
        
    
    
    
    
