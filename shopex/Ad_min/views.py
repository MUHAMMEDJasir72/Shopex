



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from user.models import Order,OrderItem,OrderAddress,Wallet,Transaction
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
import random
import string
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from django.http import HttpResponse
from decimal import Decimal
import openpyxl
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from openpyxl.utils.dataframe import dataframe_to_rows





 

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id 
            return redirect('admin_home')
        else:
            messages.error(request, "Invalid username or password.")  
            return render(request, 'admin_login.html')

    return render(request, 'admin_login.html')




  
def base(request):
    
    return render(request,'base.html')





@never_cache
def products(request):
    search_query = request.GET.get('search', '')  # Get the search query
    products = Product.objects.all()

    if search_query:
        products = products.filter(
            Q(product_name__icontains=search_query) |  # Filter by product name
            Q(productbrand__brand_name__icontains=search_query) |  # Filter by brand name
            Q(producttype__product_type__icontains=search_query)  # Filter by product type
        )

    paginator = Paginator(products, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products.html', {
        'products': products,
        'page_obj': page_obj,
        'search_query': search_query  
    })




@never_cache
def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        size_id = request.POST.get('size')
        producttype_id = request.POST.get('type')
        brand_id = request.POST.get('brand')
        description = request.POST.get('description')
        product_price = request.POST.get('price')
       

        size = get_object_or_404(ProductSize, id=size_id) 
        product_type = get_object_or_404(ProductType, id=producttype_id) 
        brand = get_object_or_404(Brand, id=brand_id) 

        if product_name and size_id and producttype_id and brand_id and description and product_price:
            Product.objects.create(
                product_name=product_name,
                producttype=product_type,
                productbrand=brand,
                productsize=size,
                description=description,
                price=product_price

            )
        return redirect('products')

    brands=Brand.objects.filter(brand_status=True)
    types=ProductType.objects.filter(type_status=True)
    sizes=ProductSize.objects.filter(size_status=True)

    return render(request, 'add_product.html', {'brands': brands, 'types':types, 'sizes':sizes})





def block_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.status = False  
    product.save()
    return redirect('product_details', product_id=product.id)

def unblock_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.status = True  
    product.save()
    return redirect('product_details', product_id=product.id)








@never_cache
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        size_id = request.POST.get('size')
        producttype_id = request.POST.get('type')
        brand_id = request.POST.get('brand')
        description = request.POST.get('description')
        product_price = request.POST.get('price')

        size = get_object_or_404(ProductSize, id=size_id)
        product_type = get_object_or_404(ProductType, id=producttype_id)
        brand = get_object_or_404(Brand, id=brand_id)

       
        if product_name and size and product_type and brand and description:
            product.product_name = product_name
            product.producttype = product_type
            product.productbrand = brand
            product.productsize = size
            product.description = description
            product.price = product_price
            product.save()

            # Redirect to the product details page after saving
            return redirect('product_details', product_id=product.id)

    # Fetch necessary data for the form

def update_variant(request, variant_id):
    # Ensure the request is POST
    if request.method == 'POST':
        variant = get_object_or_404(ProductVariant, id=variant_id)

        # Update the variant fields with the form data
        variant.colour = request.POST.get('color')
        variant.stock = request.POST.get('stock')
        variant.save()

        if request.FILES.getlist('edit_images'):
            # Delete old images if you want to replace them
            variant.images.all().delete()

            for image in request.FILES.getlist('edit_images'):
                ProductImage.objects.create(product_variant=variant, images=image)

        return redirect('product_details', product_id=variant.product.id)














@never_cache
def product_details(request,product_id):

    product = get_object_or_404(Product, id=product_id)
    variants=ProductVariant.objects.filter(product=product_id)
    images = ProductImage.objects.filter(product_variant__in=variants).first()

    if request.method == 'POST':
        colour = request.POST.get('colour')
        stock = request.POST.get('stock')
        product_images = request.FILES.getlist('images') 
      

        if colour and stock and product_images:
            variant_obj= ProductVariant.objects.create(
                product=product,
                colour=colour,
                stock=stock,
            )
            for image in product_images:
                ProductImage.objects.create(
                    product_variant=variant_obj,
                    images=image,
                
            )   
        return redirect('product_details', product_id=product_id) 
    brands=Brand.objects.filter(brand_status=True)
    types=ProductType.objects.filter(type_status=True)
    sizes=ProductSize.objects.filter(size_status=True)
    return render(request,'product_details.html',{'product':product, 'variants':variants, 'images':images, 'brands': brands, 'types': types, 'sizes': sizes, 'variant': variants.first()})


def brands(request):
    
    if request.method == 'POST':
        brand = request.POST.get('brand')
        
        if brand:
            Brand.objects.create(
                brand_name=brand
            )
            return redirect('brands')
        
    brands=Brand.objects.all()

    return render(request,'brands.html',{'brands':brands})


def product_type(request):

    if request.method == 'POST':
        producttype = request.POST.get('type')
        
        if producttype:
            ProductType.objects.create(
                product_type=producttype
            )
            return redirect('product_type')
        
    types=ProductType.objects.all()

    return render(request,'product_type.html',{'types':types})

def product_size(request):

    if request.method == 'POST':
        productsize = request.POST.get('size')
        
        if productsize:
            ProductSize.objects.create(
                product_size=productsize + 'L'
            )
            return redirect('product_size')
        
    sizes=ProductSize.objects.all()

    return render(request,'product_size.html',{'sizes':sizes})



 

def users(request):

    search_query = request.GET.get('search', '')

    users = User.objects.all().filter(is_superuser=False).order_by('-id')

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) | Q (email__icontains=search_query) | Q (id__icontains=search_query)
        )

    paginator = Paginator(users, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request,'users.html',{'users':users, 'page_obj': page_obj})


def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('users')


def unblock_user(request, id):
    user = get_object_or_404(User, id=id)
    user.is_active = True
    user.save()
    return redirect('users') 











def admin_home(request):
    # Top 10 selling products by total quantity sold
    top_products = Product.objects.filter(
        variants__orderitem__order__status='Delivered'
    ).annotate(
        total_quantity_sold=Sum('variants__orderitem__quantity')
    ).order_by('-total_quantity_sold')[:10]
    
    # Top 10 selling categories (ProductType) by total quantity sold
    top_categories = ProductType.objects.filter(
        products__variants__orderitem__order__status='Delivered'
    ).annotate(
        total_quantity_sold=Sum('products__variants__orderitem__quantity')
    ).order_by('-total_quantity_sold')[:10]
    
    # Top 10 selling brands by total quantity sold
    top_brands = Brand.objects.filter(
        products__variants__orderitem__order__status='Delivered'
    ).annotate(
        total_quantity_sold=Sum('products__variants__orderitem__quantity')
    ).order_by('-total_quantity_sold')[:10]
    
    context = {
        'top_products': top_products,
        'top_categories': top_categories,
        'top_brands': top_brands,
    }
    
    return render(request, 'admin_home.html', context)



def admin_logout(request):
    logout(request)
    return redirect('admin_login')



def orders_view(request):
    search_query = request.GET.get('search', '')

    # Filter orders based on search query
    orders = Order.objects.all()

    

    if search_query:
        orders = orders.filter(
            Q(user__id__icontains=search_query) |
            Q(status__icontains=search_query) |
            Q(razorpay_order_id__icontains=search_query) |
            Q(payment_method__icontains=search_query)
        )

    # Paginate orders
    orders = orders.order_by('-ordered_at')
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'orders.html', {'orders': orders, 'page_obj': page_obj, 'search_query': search_query})

def order_details(request, order_id):
   
    order = get_object_or_404(Order, id=order_id)
    order_item = OrderItem.objects.filter(order=order)
    address = get_object_or_404(OrderAddress, order=order)


    total = 0 
    for i in order_item:
        if i.order_item_status:
            if i.product.product_offer and i.product.brand_offer:
                if i.product.brand_offer < i.product.product_offer:
                    total += i.product.brand_offer * i.quantity
                else:
                    total += i.product.product_offer * i.quantity
            elif i.product.product_offer:
                total += i.product.product_offer * i.quantity
            elif i.product.brand_offer:
                total += i.product.brand_offer * i.quantity
            else:
                total += i.product.price * i.quantity

        


    if order.coupon:
        discount = total * order.coupon.percentage / 100
    else:
        discount = 0


    # Prepare context for the template
    context = {
        'order': order,
        'order_items': order_item,
        'address':address,
        'discount':discount
    }

    return render(request, 'order_details.html', context)


def remove_user_order(request, order_id, order_item_id):
    # Retrieve the order and order item
    order = get_object_or_404(Order, id=order_id)
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    coupon = order.coupon

    # Try to retrieve the user's wallet, create one if it doesn't exist
    wallet_item, created = Wallet.objects.get_or_create(user=request.user)

    discount = 0

    # Calculate the discount based on product and brand offers, or coupon
    brand_offer = order_item.product.productbrand.brandoffers.first()
    product_offer = order_item.product.productoffers.first()

    # If both brand and product offers are present
    if brand_offer and product_offer:
        if brand_offer.brand_offer_percentage > product_offer.product_offer_percentage:
            offer_percentage = order_item.product.brand_offer
        else:
            offer_percentage = order_item.product.product_offer
    elif brand_offer:
        offer_percentage = order_item.product.brand_offer
    elif product_offer:
        offer_percentage = order_item.product.product_offer
    else:
        offer_percentage = order_item.product.price

    # Apply coupon discount if available
    if coupon:
        discount = (coupon.percentage / 100) * offer_percentage * order_item.quantity
        order.total_amount -= Decimal(offer_percentage * order_item.quantity - discount)
    else:
        discount = offer_percentage * order_item.quantity
        order.total_amount -= Decimal(discount)


    # Update wallet if payment was through Razorpay
    if order.payment_method in ['razorpay', 'wallet']:
        wallet_item.wallet_amount += discount
        wallet_item.save()

        # Create a transaction record for wallet refund
        Transaction.objects.create(
            wallet=wallet_item,
            transaction_amount=discount,
            type = 'Credit'
        )

    # Save the updated order total
    order.save()

    # Mark the order item as inactive (considered removed)
    order_item.order_item_status = False
    order_item.save()

    # If total amount becomes zero or negative, cancel the order
    if not order.items.filter(order_item_status=True).exists():
        order.status = 'Cancelled'
        order.total_amount = 0
        order.save()

    # Update the stock for the removed order item
    variant = order_item.variant
    variant.stock += order_item.quantity
    variant.save()

    # Redirect to the order details page after removal
    return redirect('order_details', order_id=order_id)

def cancel_user_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    wallet_item, created = Wallet.objects.get_or_create(user=request.user)


    if order.payment_method in ['razorpay', 'wallet']:
        wallet_item.wallet_amount += order.total_amount
        trans = order.total_amount
        wallet_item.save()
        
        Transaction.objects.create(
            wallet = wallet_item,
            transaction_amount = trans,
            type = 'Credit'
        )

    order.status = 'Cancelled'
    order.total_amount = 0
    order.save()

    order_items = OrderItem.objects.filter(order=order)
    for item in order_items:
        variant = item.variant
        variant.stock += item.quantity
        variant.save()

    return redirect('order_details', order_id=order_id)


def order_status(request, order_id, new_status):
    # Update the status of the order
    order = Order.objects.get(id=order_id)
    order.status = new_status
    wallet_item, created = Wallet.objects.get_or_create(user=request.user)
    if new_status == 'Delivered':
        order.delivered_at = timezone.now()
        order.paid = True
    
    elif new_status == 'Cancelled':
        if order.payment_method in ['razorpay', 'wallet']:
            wallet_item.wallet_amount += order.total_amount
            trans = order.total_amount
            wallet_item.save()
            
            Transaction.objects.create(
                wallet = wallet_item,
                transaction_amount = trans,
                type = 'Credit'
            )

    order.save()

   
    return redirect('order_details', order_id=order_id)





def change_brand_status(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    brand.brand_status = not brand.brand_status
    brand.save()
    # Redirect to the page where the brands are listed
    return redirect('brands') 

def change_size_status(request, size_id):
    size = get_object_or_404(ProductSize, id=size_id)
    size.size_status = not size.size_status
    size.save()
    # Redirect to the page where the brands are listed
    return redirect('product_size')    

def change_type_status(request, type_id):
    type = get_object_or_404(ProductType, id=type_id)
    type.type_status = not type.type_status
    type.save()
    # Redirect to the page where the brands are listed
    return redirect('product_type')



 







def coupons(request):
    if request.method == 'POST':
        percentage_str = request.POST.get('percentage')
        expiration_date = request.POST.get('expiration_date')
        minimum_str = request.POST.get('minimum_amount')
        maximum_str = request.POST.get('maximum_amount')
        
        try:
            percentage = int(percentage_str)
            minimum_amount = int(minimum_str)  # Convert minimum_amount to an integer
            maximum_amount = int(maximum_str)  # Convert percentage to an integer
        except ValueError:
            messages.error(request, 'Percentage must be a valid integer.')
            return redirect('coupons')

        if percentage <= 0 or percentage >= 100:
            messages.error(request, 'Percentage should be between 0 and 100.')            
            return redirect('coupons')
        
        code = generate_coupon_code()

        while Coupon.objects.filter(code=code).exists():
            code = generate_coupon_code()
        
        if expiration_date:  # Check if expiration_date is provided
            Coupon.objects.create(
                code=code,
                percentage=percentage,
                expiration_date=expiration_date,
                minimum_amount=minimum_amount,
                maximum_amount=maximum_amount
            )
            messages.success(request, 'Coupon code added successfully.')
            return redirect('coupons')
         
    coupons_list = Coupon.objects.all().order_by('-id')
    today = timezone.now().date().strftime('%Y-%m-%d')

    for coupon in coupons_list:
        if coupon.expiration_date < timezone.now():
            coupon.active = False
            coupon.save()
    
    return render(request, 'coupons.html', {'coupons_list': coupons_list, 'today': today})



def generate_coupon_code(length=10):
    """Generate a random string of uppercase letters and digits."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))



def delete_coupon(request, coupon_id):

    coupon = get_object_or_404(Coupon, id=coupon_id)
    coupon.delete()
    return redirect('coupons')


 
def product_offer(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        discount_percentage = int(request.POST.get('offer', 0)) 

        # Fetch the product or return 404 if not found
        product = get_object_or_404(Product, id=product_id)

        discount_amount = 0
        if 0 <= discount_percentage <= 100:
            discount_amount = (discount_percentage / 100) * product.price

            product.product_offer = product.price - discount_amount

            product.save()

            # Check if offer already exists, and update or create
            existing_offer = ProductOffer.objects.filter(product=product).first()
            if existing_offer:
                existing_offer.product_offer_percentage = discount_percentage
                existing_offer.save()
            else:
                ProductOffer.objects.create(product=product, product_offer_percentage=discount_percentage)

        return redirect('product_offer')

    # Handle GET request
    product_offers = ProductOffer.objects.all().order_by('-id')
    all_products = Product.objects.all()

    offered_products = product_offers.values_list('product_id', flat=True)
    available_products = all_products.exclude(id__in=offered_products)

    return render(request, 'product_offer.html', {'products': available_products, 'product_offers': product_offers})

@never_cache
def edit_product_offer(request,offer_id):
    offer = get_object_or_404(ProductOffer, id=offer_id)
    product = offer.product
    discount_percentage = int(request.POST.get('offer'))

    if request.method == 'POST':
        
        discount_amount = (discount_percentage / 100) * product.price
        product.product_offer = product.price - discount_amount
        product.save()
        offer.product_offer_percentage = discount_percentage
        offer.save()
        return redirect('product_offer')




def delete_product_offer(request, offer_id):
 
    offer = get_object_or_404(ProductOffer, id=offer_id)
    product = offer.product

    product.product_offer=None
    product.save()

    offer.delete()
    
    return redirect('product_offer')

def brand_offer(request):

    if request.method == 'POST':
        brand_id = request.POST.get('brand')
        discount_percentage = int(request.POST.get('offer'))
        
        brand = Brand.objects.get(id=brand_id)
        if discount_percentage:
            products = Product.objects.filter(productbrand=brand)
            discount_amount = 0
            for product in products:
                discount_amount = (discount_percentage / 100) * product.price
                product.brand_offer= product.price - discount_amount
                product.save()
                

        existing_offer = BrandOffer.objects.filter(brand=brand).first()
        if existing_offer:
            existing_offer.brand_offer_percentage = discount_percentage
            existing_offer.save()
        else:
            BrandOffer.objects.create(brand=brand, brand_offer_percentage=discount_percentage)
        return redirect('brand_offer')


    brands = Brand.objects.all()
    brand_offers = BrandOffer.objects.all()

    # Find brands that don't yet have an offer
    offered_brands = brand_offers.values_list('brand_id', flat=True)
    available_brands = brands.exclude(id__in=offered_brands)

    return render(request, 'brand_offer.html', {'brands':available_brands, 'brand_offers':brand_offers})




@never_cache
def edit_brand_offer(request, offer_id):
    brand_offer = get_object_or_404(BrandOffer, id=offer_id)
    brand = brand_offer.brand  # Assuming BrandOffer has a ForeignKey to Brand
    products = Product.objects.filter(productbrand=brand)
    
    if request.method == 'POST': 
        discount_percentage = int(request.POST.get('offer', 0))
        for product in products:
            discount_amount = (discount_percentage / 100) * product.price
            product.brand_offer = product.price - discount_amount
            product.save()

        brand_offer.brand_offer_percentage = discount_percentage
        brand_offer.save()      
    
        return redirect('brand_offer')
    



   






def delete_brand_offer(request, offer_id):
    offer = get_object_or_404(BrandOffer, id=offer_id)

    products = Product.objects.filter(productbrand=offer.brand)
    
    for product in products:
        if product.brand_offer:  
            product.brand_offer = None  
            product.save()  

    offer.delete()
    
    return redirect('brand_offer')  #











def sales_report(request):
    # Retrieve all delivered orders and order them by the latest date
    orders = Order.objects.filter(status='Delivered').order_by('-ordered_at')

    # Get filter values from the request
    filter_type = request.GET.get('filter', 'all')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    today = datetime.today()

    # Apply filters based on the request
    if filter_type == 'daily':
        orders = orders.filter(ordered_at__date=today)
    elif filter_type == 'weekly':
        week_start = today - timedelta(days=today.weekday())  # Start of the current week (Monday)
        orders = orders.filter(ordered_at__date__gte=week_start)
    elif filter_type == 'monthly':
        month_start = today.replace(day=1)  # Start of the current month
        orders = orders.filter(ordered_at__date__gte=month_start)
    elif filter_type == 'custom' and start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            orders = orders.filter(ordered_at__date__range=[start_date, end_date])
        except ValueError:
            start_date = None
            end_date = None

    # Calculate total sales count
    sales_count = orders.count()
  

    # Calculate total amount
    total_amount = orders.aggregate(total=Sum('total_amount'))['total'] or 0

    # Calculate total discount
    total_discount = 0
    for order in orders:
        if order.coupon:  # Only consider orders with a coupon
            order_items = order.items.all()
            for order_item in order_items:
                discount = 0
                brand_offer = order_item.product.productbrand.brandoffers.first()
                product_offer = order_item.product.productoffers.first()

                # Determine which offer to apply
                if brand_offer and product_offer:
                    if brand_offer.brand_offer_percentage > product_offer.product_offer_percentage:
                        discount = (order.coupon.percentage / 100) * order_item.product.brand_offer * order_item.quantity
                    else:
                        discount = (order.coupon.percentage / 100) * order_item.product.product_offer * order_item.quantity
                elif brand_offer:
                    discount = (order.coupon.percentage / 100) * order_item.product.brand_offer * order_item.quantity
                elif product_offer:
                    discount = (order.coupon.percentage / 100) * order_item.product.product_offer * order_item.quantity
                else:
                    discount = (order.coupon.percentage / 100) * order_item.product.price * order_item.quantity

                total_discount += discount
    
    # Pagination
    paginator = Paginator(orders, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sales_report.html', {
        'page_obj': page_obj,
        'filter': filter_type,
        'sales_count': sales_count,
        'total_amount': total_amount,
        'total_discount': total_discount,
        'start_date': start_date,
        'end_date': end_date,
    })










# views.py




def total_sales_count(request):
    filter_type = request.GET.get('filter')  # Get the filter type (week, month, year)
    now = datetime.now()

    # Exclude orders with status 'returned'
    order_filter = Order.objects.exclude(status='Returned')

    if filter_type == 'week':
        start_date = now - timedelta(days=now.weekday())  # Start of the current week (Monday)
        end_date = start_date + timedelta(days=6)  # End of the current week (Sunday)
        sales_count = (
            order_filter.filter(delivered_at__date__range=[start_date, end_date])
            .values('delivered_at__date')  # Group by delivery date
            .annotate(count=Count('id'))  # Count orders
            .order_by('delivered_at__date')
        )
        labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']  # Day names
        counts = [next((entry['count'] for entry in sales_count if entry['delivered_at__date'] == (start_date + timedelta(days=i)).date()), 0) for i in range(7)]

    elif filter_type == 'month':
        start_date = now.replace(month=1, day=1)  # First day of the year
        sales_count = (
            order_filter.filter(delivered_at__year=now.year)
            .values('delivered_at__month')  # Group by delivery month
            .annotate(count=Count('id'))
            .order_by('delivered_at__month')
        )
        labels = [datetime(now.year, i, 1).strftime('%B') for i in range(1, 13)]  # List of all months (January to December)
        counts = [next((entry['count'] for entry in sales_count if entry['delivered_at__month'] == i), 0) for i in range(1, 13)]

    elif filter_type == 'year':
        current_year = now.year
        start_year = current_year - 5  # Start from 5 years ago
        end_year = current_year + 5  # Include 5 years after the current year
        sales_count = (
            order_filter.filter(delivered_at__year__gte=start_year, delivered_at__year__lte=end_year)
            .values('delivered_at__year')  # Group by delivery year
            .annotate(count=Count('id'))
            .order_by('delivered_at__year')
        )
        labels = [str(year) for year in range(start_year, end_year + 1)]  # List of years from 5 years ago to 5 years after
        counts = [next((entry['count'] for entry in sales_count if entry['delivered_at__year'] == year), 0) for year in range(start_year, end_year + 1)]

    return JsonResponse({'labels': labels, 'counts': counts})


















def export_sales_report_excel(request):
    # Retrieve filtered orders
    orders = Order.objects.filter(status='Delivered').order_by('-ordered_at')

    # Apply filters (same as in your sales_report view)
    filter_type = request.GET.get('filter', 'all')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    today = datetime.today()

    if filter_type == 'daily':
        orders = orders.filter(ordered_at__date=today)
    elif filter_type == 'weekly':
        week_start = today - timedelta(days=today.weekday())
        orders = orders.filter(ordered_at__date__gte=week_start)
    elif filter_type == 'monthly':
        month_start = today.replace(day=1)
        orders = orders.filter(ordered_at__date__gte=month_start)
    elif filter_type == 'custom' and start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            orders = orders.filter(ordered_at__date__range=[start_date, end_date])
        except ValueError:
            pass

    # Compute sales count, total amount, and total discount
    sales_count = orders.count()
    total_amount = orders.aggregate(total=Sum('total_amount'))['total'] or 0
    total_discount = 0
    for order in orders:
        order_items = order.items.all()
        if order.coupon:
            for order_item in order_items:
                discount = 0
                brand_offer = order_item.product.productbrand.brandoffers.first()
                product_offer = order_item.product.productoffers.first()

                if brand_offer and product_offer:
                    if brand_offer.brand_offer_percentage > product_offer.product_offer_percentage:
                        discount = (order.coupon.percentage / 100) * order_item.product.brand_offer * order_item.quantity
                    else:
                        discount = (order.coupon.percentage / 100) * order_item.product.product_offer * order_item.quantity
                elif brand_offer:
                    discount = (order.coupon.percentage / 100) * order_item.product.brand_offer * order_item.quantity
                elif product_offer:
                    discount = (order.coupon.percentage / 100) * order_item.product.product_offer * order_item.quantity
                else:
                    discount = (order.coupon.percentage / 100) * order_item.product.price * order_item.quantity

                total_discount += discount

    # Create an Excel workbook and worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Sales Report'

    # Add headers and computed values
    headers = ['Sales Count', 'Total Amount', 'Total Discount']
    values = [sales_count, total_amount, total_discount]
    worksheet.append(headers)
    worksheet.append(values)
    worksheet.append([])  # Add a blank row for separation

    # Add order data headers
    order_headers = ['Order Id', 'User name', 'Total Amount', 'Ordered at', 'Delivered at', 'Payment Method']
    worksheet.append(order_headers)

    # Add order data
    for order in orders:
        row = [
            order.id,
            order.user.username,
            order.total_amount,
            order.ordered_at.strftime('%Y-%m-%d'),
            order.delivered_at.strftime('%Y-%m-%d'),
            order.payment_method,
        ]
        worksheet.append(row)

    # Save the workbook to a BytesIO object
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sales_report.xlsx'
    workbook.save(response)

    return response




def export_sales_report_pdf(request):
    # Retrieve filtered orders
    orders = Order.objects.filter(status='Delivered').order_by('-ordered_at')

    # Apply filters (same as in your sales_report view)
    filter_type = request.GET.get('filter', 'all')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    today = datetime.today()

    if filter_type == 'daily':
        orders = orders.filter(ordered_at__date=today)
    elif filter_type == 'weekly':
        week_start = today - timedelta(days=today.weekday())
        orders = orders.filter(ordered_at__date__gte=week_start)
    elif filter_type == 'monthly':
        month_start = today.replace(day=1)
        orders = orders.filter(ordered_at__date__gte=month_start)
    elif filter_type == 'custom' and start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            orders = orders.filter(ordered_at__date__range=[start_date, end_date])
        except ValueError:
            pass

    # Compute sales count, total amount, and total discount
    sales_count = orders.count()
    total_amount = orders.aggregate(total=Sum('total_amount'))['total'] or 0
    total_discount = 0
    for order in orders:
        order_items = order.items.all()
        if order.coupon:
            for order_item in order_items:
                discount = 0
                brand_offer = order_item.product.productbrand.brandoffers.first()
                product_offer = order_item.product.productoffers.first()

                if brand_offer and product_offer:
                    if brand_offer.brand_offer_percentage > product_offer.product_offer_percentage:
                        discount = (order.coupon.percentage / 100) * order_item.product.brand_offer * order_item.quantity
                    else:
                        discount = (order.coupon.percentage / 100) * order_item.product.product_offer * order_item.quantity
                elif brand_offer:
                    discount = (order.coupon.percentage / 100) * order_item.product.brand_offer * order_item.quantity
                elif product_offer:
                    discount = (order.coupon.percentage / 100) * order_item.product.product_offer * order_item.quantity
                else:
                    discount = (order.coupon.percentage / 100) * order_item.product.price * order_item.quantity

                total_discount += discount

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=sales_report.pdf'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Define styles
    styles = getSampleStyleSheet()
    header_style = styles['Title']
    normal_style = styles['Normal']

    # Define table data
    data = [
        ['Sales Count', 'Total Amount', 'Total Discount'],
        [sales_count, total_amount, total_discount],
        [],  # Empty row for separation
        ['Order Id', 'User name', 'Total Amount', 'Ordered at', 'Delivered at', 'Payment Method']
    ]

    for order in orders:
        data.append([
            order.id,
            order.user.username,
            order.total_amount,
            order.ordered_at.strftime('%Y-%m-%d'),
            order.delivered_at.strftime('%Y-%m-%d'),
            order.payment_method,
        ])

    # Create a table with the data
    table = Table(data)

    # Add table styling
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Build the PDF document with the table
    doc.build([Paragraph('Sales Report', header_style), table])

    return response


def approve_return(request, order_id):
    # Get the order or raise a 404 error if it doesn't exist
    order = get_object_or_404(Order, id=order_id)
    wallet_item, created = Wallet.objects.get_or_create(user=request.user)

    # Update the order status to 'Returned' and set 'paid' to False
    order.status = 'Returned'
    order.paid = False
    order.return_request = False
    wallet_item.wallet_amount += order.total_amount
    trans = order.total_amount
    wallet_item.save()
    order.save()

    Transaction.objects.create(
        wallet = wallet_item,
        transaction_amount = trans,
        type = 'credit'
    )
    

    # Redirect to the order details page
    return redirect('order_details', order_id=order_id)


def approve_item_return(request, order_id, order_item_id):
    # Get the order or raise a 404 error if it doesn't exist
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    order = get_object_or_404(Order, id=order_id)
    wallet_item, created = Wallet.objects.get_or_create(user=request.user)


    order_item.order_item_status = 'Returned'
    order_item.item_return_request = False

    discount =0
    
    if order.coupon:
        if order_item.product.product_offer and order_item.product.brand_offer:
            if order_item.product.brand_offer < order_item.product.product_offer:
                discount = (order.coupon.percentage / 100) * order_item.product.brand_offer * order_item.quantity
                amount = order_item.product.brand_offer * order_item.quantity
            else:
                discount = (order.coupon.percentage / 100) * order_item.product.product_offer * order_item.quantity
                amount = order_item.product.product_offer * order_item.quantity
        elif order_item.product.brand_offer:
            discount = (order.coupon.percentage / 100) * order_item.product.brand_offer * order_item.quantity
            amount = order_item.product.brand_offer * order_item.quantity
        elif order_item.product.product_offer:
            discount = (order.coupon.percentage / 100) * order_item.product.product_offer * order_item.quantity
            amount = order_item.product.product_offer * order_item.quantity
        else:
            discount = (order.coupon.percentage / 100) * order_item.product.price * order_item.quantity
            amount = order_item.product.price * order_item.quantity

    else:
        amount = order_item.product.price * order_item.quantity

    wallet_item.wallet_amount += amount - discount
    trans = amount -discount
    wallet_item.save()
    order_item.save()

    Transaction.objects.create(
        wallet = wallet_item,
        transaction_amount = trans,
        type = 'credit'
    )
    
    all_items_returned = all(item.order_item_status == 'Returned' for item in order.items.all())
    if all_items_returned:
        order.status = 'Returned'  # Update order status to 'Returned'
        order.save()

    # Redirect to the order details page
    return redirect('order_details', order_id=order_id)


def edit_coupon(request):
    if request.method == 'POST':
        coupon_id = request.POST.get('coupon_id')
        coupon = get_object_or_404(Coupon, id=coupon_id)
        coupon.code = request.POST['code']
        coupon.percentage = request.POST['percentage']
        coupon.minimum_amount = request.POST['minimum_amount']
        coupon.maximum_amount = request.POST['maximum_amount']
        coupon.expiration_date = request.POST['expiration_date']
        coupon.save()
        return redirect('coupons')