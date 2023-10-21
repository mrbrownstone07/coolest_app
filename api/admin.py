from django.contrib import admin
from .models.districts import District, DistrictAdmin
from .models.forecasts import Forecast, ForecastAdmin
from .models.travel_suggestion_requests import (TravelSuggestionRequest, 
                                                TravelSuggestionRequestAdmin)
from .models.travel_suggestion_request_logs import (TravelSuggestionRequestLog,
                                                    TravelSuggestionRequestLogAdmin)

admin.site.register(District, DistrictAdmin)
admin.site.register(Forecast, ForecastAdmin)
admin.site.register(TravelSuggestionRequest, TravelSuggestionRequestAdmin)
admin.site.register(TravelSuggestionRequestLog, TravelSuggestionRequestLogAdmin)