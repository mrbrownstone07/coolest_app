from django.contrib import admin
from .models.districts import District, DistrictAdmin


admin.site.register(District, DistrictAdmin)
