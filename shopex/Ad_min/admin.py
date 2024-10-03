from django.contrib import admin
from . models import *

# Register your models here.


admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
admin.site.register(Brand)
admin.site.register(ProductType)
admin.site.register(ProductSize)
admin.site.register(ProductOffer)
admin.site.register(BrandOffer)
admin.site.register(Coupon)
admin.site.register(Review)

