from django.contrib import admin

from .models import Client
from .models import Signature

# Register your models here.
admin.site.register(Client)
admin.site.register(Signature)