from django.db import models
from django.contrib.auth.models import User
from Ad_min.models import Product,ProductVariant,ProductImage,Coupon





    



class UserInformation(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    mobile = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Addresses(models.Model):
    fullname = models.CharField(max_length=50)
    mobil_number = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    landmark = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_selected = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.fullname}, {self.city}, {self.state}"
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='cart_items')
    image = models.ForeignKey(ProductImage, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"


class Order(models.Model):
 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10)
    ordered_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(null=True, blank=True)
    return_request = models.BooleanField(default=False)





class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    order_item_status = models.CharField(max_length=10)
    item_return_request = models.BooleanField(default=False)
    


    

class OrderAddress(models.Model):
    fullname = models.CharField(max_length=50)
    mobil_number = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    landmark = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallet')
    wallet_amount = models.IntegerField(default=0)
    
class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    transaction_amount = models.IntegerField()   
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50)


class CouponUsed(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupons')
    
    