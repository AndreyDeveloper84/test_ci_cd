from django.contrib import admin
from .models import Order, Unit

admin.site.register(Order, Unit)


# Register your models here.
