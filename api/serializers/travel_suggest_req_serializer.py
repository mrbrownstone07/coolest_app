from rest_framework import serializers
from ..models.districts import District
from ..models.forecasts import Forecast
from ..models.travel_suggestion_requests import TravelSuggestionRequest

class DistrictRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            district = District.objects.get(name=data)
            return district
        except District.DoesNotExist:
            raise serializers.ValidationError(f"{data} is not a district.")


class TravelSuggestionRequestSerializer(serializers.ModelSerializer):
    location = DistrictRelatedField(queryset=District.objects.all(),many=False)
    destination = DistrictRelatedField(queryset=District.objects.all(),many=False)
    
    class Meta:
        model = TravelSuggestionRequest
        fields = ['location', 'destination', 'travel_date']
    
    def validate(self, attrs):
        if not Forecast.check_forecast_date(forecast_date=attrs.get('travel_date')):
            raise serializers.ValidationError(
                {"travel_date": f"we currently have no forecast for {attrs.get('travel_date')}."}
            ) 
        return super().validate(attrs)
        
