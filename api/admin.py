from django.contrib import admin
from .models.districts import District, DistrictAdmin
from .models.forecasts import Forecast, ForecastAdmin

admin.site.register(District, DistrictAdmin)
admin.site.register(Forecast, ForecastAdmin)
