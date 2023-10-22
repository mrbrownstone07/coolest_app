from django.db import models
from django.contrib import admin
from django.http.request import HttpRequest
from .districts import District
from datetime import time
from django.db import transaction

class Forecast(models.Model):
    temperature = models.DecimalField(null=False, decimal_places=2, max_digits=4, db_index=True)
    forecast_date = models.DateField(null=False, db_index=True)
    forecast_time = models.TimeField(null=False, db_index=True)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True) 
    district = models.ForeignKey(District, related_name='forecastOfDistrict', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"""{self.district.name} 
            {self.forecast_date.strftime(format="%m/%d/%Y")} 
            {self.forecast_time.strftime(format="%H:%M:%S")}"""  
    
    def check_forecast_date(forecast_date):
        return Forecast.objects.filter(
            forecast_date=forecast_date, 
            forecast_time=time(hour=14, minute=00, second=00)
        ).exists()    
    
    @classmethod
    def bulk_update_or_create(cls, common_keys, unique_key_name, unique_key_to_defaults):
        """
        common_keys: {field_name: field_value}
        unique_key_name: field_name
        unique_key_to_defaults: {field_value: {field_name: field_value}}
        
        ex. Event.bulk_update_or_create(
            {"organization": organization}, "external_id", {1234: {"started": True}}
        )
        """
        with transaction.atomic():
            filter_kwargs = dict(common_keys)
            filter_kwargs[f"{unique_key_name}__in"] = unique_key_to_defaults.keys()
            existing_objs = {
                getattr(obj, unique_key_name): obj
                for obj in cls.objects.filter(**filter_kwargs).select_for_update()
            }
            
            create_data = {
                k: v for k, v in unique_key_to_defaults.items() if k not in existing_objs
            }
            for unique_key_value, obj in create_data.items():
                obj[unique_key_name] = unique_key_value
                obj.update(common_keys)
            creates = [cls(**obj_data) for obj_data in create_data.values()]
            if creates:
                cls.objects.bulk_create(creates)

            # This set should contain the name of the `auto_now` field of the model
            update_fields = {"updated_at"}
            updates = []
            for key, obj in existing_objs.items():
                obj.update(unique_key_to_defaults[key], save=False)
                update_fields.update(unique_key_to_defaults[key].keys())
                updates.append(obj)
            if existing_objs:
                cls.objects.bulk_update(updates, update_fields)
        return len(creates), len(updates)

    def update(self, update_dict=None, save=True, **kwargs):
        """ Helper method to update objects """
        if not update_dict:
            update_dict = kwargs
        # This set should contain the name of the `auto_now` field of the model
        update_fields = {"updated_at"}
        for k, v in update_dict.items():
            setattr(self, k, v)
            update_fields.add(k)
        if save:
            self.save(update_fields=update_fields)



class ForecastAdmin(admin.ModelAdmin):
    list_display = ['id', 'temperature', 'forecast_date', 'forecast_time', 'district', 'created_at', 'updated_at']
    date_hierarchy = 'forecast_date'
    list_filter = ['district', 'forecast_time']
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
    
    
    
    
    