from django.contrib import admin

from . models import *



admin.site.register(UserInformation)
admin.site.register(Addresses)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Wishlist)
admin.site.register(Wallet)