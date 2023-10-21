from django.db import models
from django.contrib import admin
from django.http.request import HttpRequest
from .districts import District

class TravelSuggestionRequest(models.Model):
    location = models.ForeignKey(District, related_name='TravelSuggestionLocation', on_delete=models.CASCADE, db_index=True)
    destination = models.ForeignKey(District, related_name='TravelSuggestionDestination', on_delete=models.CASCADE, db_index=True)
    travel_date = models.DateField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

  
class TravelSuggestionRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'location', 'destination', 'travel_date', 'created_at', 'processed']
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
    