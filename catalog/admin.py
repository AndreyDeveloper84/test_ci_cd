from django.contrib import admin
from .models import Order, Unit

admin.site.register(Order)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ["title"]
