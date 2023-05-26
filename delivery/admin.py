from django.contrib import admin
from .models import *

admin.site.register(Food)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Establishments)
admin.site.register(FoodCategory)
admin.site.register(CartItem)
admin.site.register(Order)


