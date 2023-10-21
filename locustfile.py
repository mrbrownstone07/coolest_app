from locust import HttpUser, task
import random

class FirstLocust(HttpUser):
    
    @task
    def test_coolest_districts_api(self):
        self.client.get('/api/v1/coolest-districts')
        
        
    @task 
    def test_travel_suggestions_api(self):
        request_data = [
            {'location': 'dhaka', 'destination': "Sunamganj", 'travel_date': '2023-11-05'},
            {'location': 'Chuadanga', 'destination': "Netrokona", 'travel_date': '2023-11-05'},
            {'location': 'Lakshmipur', 'destination': "Habiganj", 'travel_date': '2023-11-05'},
            {'location': 'Sherpur', 'destination': "Feni", 'travel_date': '2023-11-05'},
            {'location': 'Maulvibaz', 'destination': "Gazipur", 'travel_date': '2023-11-05'},
            {'location': 'Kurigram', 'destination': "Satkhira", 'travel_date': '2023-11-05'},
            {'location': 'Meherpur', 'destination': "Faridpur", 'travel_date': '2023-11-05'},
            {'location': 'Brahmanbaria', 'destination': "Jashore", 'travel_date': '2023-11-05'},
            {'location': 'Kushtia', 'destination': "Meherpur", 'travel_date': '2023-11-05'},
            {'location': 'Magura', 'destination': "Khulna", 'travel_date': '2023-11-05'},
        ]
        api_response = self.client.post('/api/v1/travel-suggestions', data=request_data[random.randint(0, 9)])
        
