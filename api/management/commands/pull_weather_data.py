from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Pulls weather forecast data from the API and Pushes into DB."

    def handle(self, *args, **options):
        pass
    
def pull_data():
    pass
