from django.contrib import admin
from .models import *

# Register your models here
admin.site.site_title = "Tourism Project"
admin.site.index_title = "Tourism"
admin.site.site_header = "Tourism Admin"

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'package', 'total_price')
admin.site.register(CustomUser)
admin.site.register(Package)
admin.site.register(Accommodation)
admin.site.register(Food)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
admin.site.register(Places)
