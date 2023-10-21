import json
from django.db.models import Avg
from rest_framework import status
from .models.forecasts import Forecast
from rest_framework.decorators import api_view
from utils.helpers import get_client_ip
from datetime import date, timedelta, time 
from rest_framework.response import Response
from utils.file_logger import INFO_LEVEL, ERROR_LEVEL, log
from .serializers.travel_suggest_req_serializer import TravelSuggestionRequestSerializer


@api_view(['GET'])
def get_coolest_districts(request):
    errors = {}
    try:
        forecasts = Forecast.objects.select_related(
            'district').filter(
                forecast_date__gt=date.today(),
                forecast_date__lte=date.today() + timedelta(days=7),
                forecast_time=time(hour=14, minute=00, second=00)
            ).values('district__name').annotate(avg_temp=Avg('temperature')).order_by('avg_temp')[:10]
            
        status_code=status.HTTP_200_OK
        response_data = {forecast['district__name']: float(forecast['avg_temp']) for forecast in forecasts}  
    except Exception as e:
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        errors['forecast_data'] = ['faced error while fetching forecast data!']
        response_data = {"error": True, "errors": errors}

    msg = "Request Processed Successfully!" if status_code==status.HTTP_200_OK else "Request Failed!"
    log(msg=msg, log_level=INFO_LEVEL if status_code == status.HTTP_200_OK else ERROR_LEVEL, 
        extra={'request_url': request.build_absolute_uri(),
                'request_method': "GET",
                'response': json.dumps(response_data.copy(), indent=4),
                'http_status': status_code,
                'module_name': __name__,
                'ip': get_client_ip(request),}
    )        
        
    return Response(response_data, status=status.HTTP_200_OK)
    
    
@api_view(['POST'])   
def travel_suggestions(request):
    serializer = TravelSuggestionRequestSerializer(data=request.data)
    log_data={'request_ip':get_client_ip(request), **request.data}
        
    if serializer.is_valid():
        travel_suggestion_request = serializer.save()
        forecasts = Forecast.objects.select_related(
            'district').filter(
                forecast_date=travel_suggestion_request.travel_date,
                forecast_time=time(hour=14, minute=00, second=00),
                district__in=[travel_suggestion_request.location, travel_suggestion_request.destination]
            ).order_by('temperature')
        
        status_code = status.HTTP_200_OK 
        if forecasts[0].district == travel_suggestion_request.destination:  
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
        response_data = {"error": True, "errors": serializer.errors}
        status_code = status.HTTP_400_BAD_REQUEST
        log_data['error'] = True
    
    log_data['response'] = json.dumps(response_data)  
    msg = "Request Processed Successfully!" if status_code==status.HTTP_200_OK else "Request Failed!"
    log(msg=msg, log_level=INFO_LEVEL if status_code == status.HTTP_200_OK else ERROR_LEVEL, 
        extra={'request_url': request.build_absolute_uri(),
                'request_method': "POST",
                'response': json.dumps(response_data.copy(), indent=4),
                'http_status': status_code,
                'module_name': __name__,
                'ip': get_client_ip(request),}
    ) 
        
    return Response(response_data, status=status_code)
