from django.contrib import admin
from .models import *

# Register your models here
admin.site.register(CustomUser)
admin.site.register(Package)
admin.site.register(Accommodation)
admin.site.register(Food)
admin.site.register(CartItem)
admin.site.register(Cart)