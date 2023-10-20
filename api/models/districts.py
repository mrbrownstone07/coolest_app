from django.db import models
from django.contrib import admin

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
    
    
class DistrictAdmin(admin.ModelAdmin):
    pass