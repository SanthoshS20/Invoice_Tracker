from django.contrib import admin

from .models import UserDetail, Invoice
admin.site.register(UserDetail)
admin.site.register(Invoice)
