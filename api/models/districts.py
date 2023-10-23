from django.db import models
from django.contrib import admin
from django.http.request import HttpRequest

class District(models.Model):   
    division_id = models.IntegerField(null=False, blank=False)
    longitude = models.DecimalField(null=False, decimal_places=2, max_digits=4)
    latitude = models.DecimalField(null=False, decimal_places=2, max_digits=4)
    name = models.CharField(
        max_length=55, 
        db_index=True,
        null=False,
        unique=True
    )
    
    def __str__(self) -> str:
        return self.name


class InLineForecasts(admin.TabularInline):
    from .forecasts import Forecast
    model = Forecast
    
    
class DistrictAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "longitude", "latitude"]
    inlines = [InLineForecasts]
    
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return True