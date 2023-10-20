import json
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Pulls weather forecast data from the API and Pushes into DB."
    
    def handle(self, *args, **options):
        parse_district_data()
    
def parse_district_data():
    pass