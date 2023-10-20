from django.db import models
from django.contrib import admin
from django.http.request import HttpRequest
from .districts import District

class Forecast(models.Model):
    temperature = models.DecimalField(null=False, decimal_places=2, max_digits=4)
    forecast_time = models.DateTimeField(null=False, db_index=True)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True) 
    district = models.ForeignKey(District, related_name='forecastOfDistrict', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.district.name + ' ' + self.forecast_time.strftime(format="%m/%d/%Y, %H:%M:%S")  


class ForecastAdmin(admin.ModelAdmin):
    list_display = ['id', 'temperature', 'forecast_time', 'district']
    list_filter = ['district']
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
    
    
    
    
    