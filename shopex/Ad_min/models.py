from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User



class Brand(models.Model):
    brand_name= models.CharField(max_length=255)
    brand_status = models.BooleanField(default=True)

    def __str__(self):
        return self.brand_name

class ProductType(models.Model):
    product_type= models.CharField(max_length=255)
    type_status = models.BooleanField(default=True)

    def __str__(self):
        return self.product_type
    

class ProductSize(models.Model):
    product_size= models.CharField(max_length=255)
    size_status = models.BooleanField(default=True)

    def __str__(self):
        return self.product_size    


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    status = models.BooleanField(default=True)
    product_offer = models.IntegerField(null=True, blank=True)
    brand_offer = models.IntegerField(null=True, blank=True)
    final_price = models.IntegerField(null=True, blank=True)
    productbrand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    producttype = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='products')
    productsize = models.ForeignKey(ProductSize, on_delete=models.CASCADE, related_name='products')



    def __str__(self):
        return self.product_name


class ProductVariant(models.Model):  # Renamed for clarity
    colour = models.CharField(max_length=100)
    stock = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')

    def __str__(self):
        return f"{self.product.product_name} - {self.colour}"


class ProductImage(models.Model):  # Renamed for clarity
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='images')
    images = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product_variant}"



class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    percentage = models.IntegerField()  
    expiration_date = models.DateTimeField()
    active = models.BooleanField(default=True)
    minimum_amount = models.IntegerField()
    maximum_amount = models.IntegerField()


    def __str__(self):
        return f"{self.code} - {self.percentage}%"
    
    def deactivate_if_expired(self):
        if timezone.now() > self.expiration_date:
            self.active = False
            self.save()
    def is_valid_for_amount(self, total_amount):
        """
        Checks if the coupon is valid for the given total amount.
        """
        return self.active and self.minimum_amount <= total_amount <= self.maximum_amount
    

class ProductOffer(models.Model):
    product_offer_percentage = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productoffers')


class BrandOffer(models.Model):
    brand_offer_percentage = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brandoffers')


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField() 
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} - {self.rating}"


