from django.db.models import Avg
from rest_framework import status
from .models.forecasts import Forecast
from rest_framework.views import APIView
from datetime import date, timedelta, time 
from rest_framework.response import Response


class CoolestDistrictsView(APIView):
    
    def get(self, request):
        forecasts = Forecast.objects.select_related(
            'district').filter(
                forecast_date__gt=date.today(),
                forecast_date__lte=date.today() + timedelta(days=7),
                forecast_time=time(hour=14, minute=00, second=00)
            ).values('district__name').annotate(avg_temp=Avg('temperature')).order_by('avg_temp')[:10]

        response_data = {}
        for forecast in forecasts:
           response_data[forecast['district__name']] = float(forecast['avg_temp'])
             
        return Response(response_data, status=status.HTTP_200_OK)
