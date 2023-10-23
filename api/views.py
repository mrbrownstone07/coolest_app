import json
import traceback
from django.db.models import Q
from django.db.models import Avg
from rest_framework import status
from .models.forecasts import Forecast
from rest_framework.decorators import api_view
from utils.helpers import get_client_ip
from datetime import date, timedelta
from rest_framework.response import Response
from utils.file_logger import INFO_LEVEL, ERROR_LEVEL, log
from .serializers.travel_suggest_req_serializer import TravelSuggestionRequestSerializer
from drf_spectacular.utils import extend_schema,OpenApiResponse,OpenApiExample


@extend_schema(
    summary='Top 10 Coolest Districts for 7 Days avg.',
    description="This is GET method api, which provides data of top 10 Coolest Districts for 7 Days avg at 2:00 PM",
    responses={
        200: OpenApiResponse(description='Json Response'),
        500: OpenApiResponse(description='Server Error')
    },
    examples = [
        OpenApiExample(
            'Success Case Response example 1',
            value={    
                "Netrokona": 27.685714,
                "Joypurhat": 27.771429,
                "Mymensingh": 27.9,
                "Kishoreganj": 27.914286,
                "Sherpur": 28.0,
                "Bhola": 28.028571,
                "Bogura": 28.057143,
                "Jamalpur": 28.085714,
                "Cox's Bazar": 28.085714,
                "Gaibandha": 28.128571
            },
            response_only=True,
        ),
    ]
)
@api_view(['GET'])
def get_coolest_districts(request):
    print(type(request))
    errors = {}
    error_trackback = ''
    try:
        forecasts = Forecast.objects.select_related(
            'district').filter(
                forecast_date__gt=date.today(),
                forecast_date__lte=date.today() + timedelta(days=7),
            ).values('district__name').annotate(avg_temp=Avg('temperature')).order_by('avg_temp')[:10]  
                
        status_code=status.HTTP_200_OK
        response_data = {forecast['district__name']: float(forecast['avg_temp']) for forecast in forecasts}     
    except Exception:
        error_trackback = traceback.format_exc()
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        errors['forecast_data'] = ['faced error while fetching forecast data!']
        response_data = {"error": True, "errors": errors}

    msg = "Request Processed Successfully!" if status_code==status.HTTP_200_OK else "Request Failed!"
    log(msg=msg, log_level=INFO_LEVEL if status_code == status.HTTP_200_OK else ERROR_LEVEL, 
        extra={'request_url': request.build_absolute_uri(),
                'trackback': error_trackback,
                'request_method': "GET",
                'response': json.dumps(response_data.copy(), indent=4),
                'http_status': status_code,
                'module_name': __name__,
                'ip': get_client_ip(request),}
    )        
        
    return Response(response_data, status=status.HTTP_200_OK)
    
@extend_schema(
    summary='Travel Suggestings',
    description="This is POST method api, in which given your location district, destination district and date of travel you can get a suggestion"
    + "whether you should travel or not based on the temperature of 2:00 PM.",
    request=TravelSuggestionRequestSerializer,
    responses={
        200: OpenApiResponse(description='Json Response'),
        400: OpenApiResponse(description='Validation error')
    },
    examples = [
        OpenApiExample(
            'Success Case Response example 1',
            value={"decision": "You Should Visit Cox's Bazar."},
            response_only=True,
        ),
        OpenApiExample(
            'Success Case Response example 2',
            value={"decision": "You Should not Visit Cox's Bazar."},
            response_only=True,
        ),
        OpenApiExample(
            'Error Case Response example 1',
            value={    
                "error": True,
                "errors": {
                    "location": [
                        "This field is required."
                    ]
                }
            },
            response_only=True,
        ),
    ]
) 
@api_view(['POST'])   
def travel_suggestions(request):
    serializer = TravelSuggestionRequestSerializer(data=request.data)
    log_data={'request_ip':get_client_ip(request), **request.data}
        
    if serializer.is_valid():
        travel_suggestion_request = serializer.save()
        
        forecasts = Forecast.objects.select_related(
            'district').filter(
                Q( district=travel_suggestion_request.location )
                | Q( district=travel_suggestion_request.destination ),
                forecast_date=travel_suggestion_request.travel_date,
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
