from django.db import models
from django.contrib import admin
from django.http.request import HttpRequest


class TravelSuggestionRequestLog(models.Model):
    request_ip = models.CharField(max_length=55, blank=True, null=True)
    location = models.CharField(max_length=55, blank=True, null=True)
    destination = models.CharField(max_length=55, blank=True, null=True)
    travel_date = models.CharField(max_length=55, blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    error = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class TravelSuggestionRequestLogAdmin(admin.ModelAdmin):
    list_display = ['request_ip', 'location', 'destination', 'travel_date', 'response', 'error', 'created_at', 'updated_at']
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    
    

    