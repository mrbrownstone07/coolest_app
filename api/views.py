import json
from django.db.models import Avg
from rest_framework import status
from .models.forecasts import Forecast
from rest_framework.views import APIView
from helpers.generics import get_client_ip
from datetime import date, timedelta, time 
from rest_framework.response import Response
from .serializers.travel_suggest_req_serializer import TravelSuggestionRequestSerializer
from .serializers.travel_suggest_req_log_serializer import TravelSuggestionRequestLogSerializer

class CoolestDistrictsView(APIView):
    
    def get(self, request):
        forecasts = Forecast.objects.select_related(
            'district').filter(
                forecast_date__gt=date.today(),
                forecast_date__lte=date.today() + timedelta(days=7),
                forecast_time=time(hour=14, minute=00, second=00)
            ).values('district__name').annotate(avg_temp=Avg('temperature')).order_by('avg_temp')[:10]
    
        response_data = {forecast['district__name']: float(forecast['avg_temp']) for forecast in forecasts}   
        return Response(response_data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        serializer = TravelSuggestionRequestSerializer(data=request.data)
        log_data={'request_ip':get_client_ip(request), **request.data}
         
        if serializer.is_valid():
            travel_suggestion_request = serializer.save()
            forecast = Forecast.objects.select_related(
                'district').filter(
                    forecast_date=travel_suggestion_request.travel_date,
                    forecast_time=time(hour=14, minute=00, second=00),
                    district__in=[travel_suggestion_request.location, travel_suggestion_request.destination]
                ).order_by('temperature')
            
            return_status = status.HTTP_200_OK   
            if forecast[0].district == travel_suggestion_request.destination:  
                response_data = {
                    'decision': f'You Should Visit {travel_suggestion_request.destination}.'
                }
            else:
                 response_data = {
                    'decision': f'You Should Not Visit {travel_suggestion_request.destination}.'
                }
            travel_suggestion_request.processed = True
            travel_suggestion_request.save()
        else:
            response_data = serializer.errors
            return_status = status.HTTP_400_BAD_REQUEST
            log_data['error'] = True
        
        log_data['response'] = json.dumps(response_data)
        log_serializer = TravelSuggestionRequestLogSerializer(data=log_data)
        if log_serializer.is_valid():
            log_serializer.save()
        else:
            print(log_serializer.errors)
            
        return Response(response_data, status=return_status)
