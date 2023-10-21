from rest_framework import serializers
from ..models.travel_suggestion_request_logs import TravelSuggestionRequestLog

class TravelSuggestionRequestLogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TravelSuggestionRequestLog
        fields = ['request_ip', 'location', 'destination', 'travel_date', 'response', 'error']       
