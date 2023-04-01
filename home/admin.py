from django.contrib import admin
from .models import *

# Register your models here
admin.site.register(Package)
admin.site.register(Accommodation)
admin.site.register(Food)
admin.site.register(Manager)
admin.site.register(User)
admin.site.register(Booking)