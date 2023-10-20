import os
import json
from django.conf import settings
from django.db.transaction import atomic
from django.core.management.base import BaseCommand, CommandError

from api.models.districts import District

FILE_PATH = os.path.join(settings.BASE_DIR, 'districts.json')

class Command(BaseCommand):
    help = "This command will parse the districts.json file and push the data into the district model."
    
    def handle(self, *args, **options):
        load_districts_data()

  
def load_districts_data():
    f = open(FILE_PATH, encoding='utf-8')
    data = json.load(f)
    
    with atomic():  
        for district in data['districts']:
            obj = District(
                name=district['name'],
                division_id=district['division_id'],
                longitude=district['long'],
                latitude=district['lat'],
            )
            obj.save() 
        
        