from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as authlogin, logout as authlogout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Ad_min.models import Product,ProductVariant,ProductImage,ProductSize,ProductType,Brand,Coupon,ProductOffer,Review
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
import random
import string
from django.core.mail import send_mail
from django.conf import settings
import time
from django.utils.timezone import now
from datetime import timedelta
from .models import UserInformation,Addresses,Cart,Order,OrderItem,OrderAddress,Wishlist,Wallet,Transaction,CouponUsed
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import hmac
import hashlib
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .models import Order, OrderItem
from django.core.paginator import Paginator




def user_base(request):
    return render(request,'user_base.html')




@never_cache
def login(request):
    if 'username' in request.session:
        return redirect('index')
    if request.method == "POST":
        username = request.POST['name']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            authlogin(request, user)
            request.session['username'] = username
            return redirect('index')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'login.html')

@never_cache
def logout(request):
    authlogout(request)
    return redirect('index')

def confirm_password(request):
    
    if request.method == "POST":
        password = request.POST.get('password')
        user = request.user
        
        # Authenticate user
        if user.check_password(password):
            return redirect('new_password')
        else:
            messages.error(request, 'Wrong Password')
            return redirect('confirm_password')
    
    return render(request, 'confirm_password.html')



def new_password(request):
    user = request.user
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if len(new_password) < 8:
            messages.error(request, 'New password must be at least 8 characters long.')
        elif new_password != confirm_password:
            messages.error(request, 'The new password and confirm password do not match.')
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after the password change

            return redirect('profile')
    return render(request, 'new_password.html')






def index(request):
    products = Product.objects.filter(status=True).prefetch_related('variants__images').all()
    new_arrivals = Product.objects.select_related(
        'productbrand', 
        'producttype', 
        'productsize'
    ).prefetch_related(
        'variants__images'  # Prefetch images for the product variants
    ).all().order_by('-id')

    brands = Brand.objects.filter(brand_status=True)
    types = ProductType.objects.filter(type_status=True)
    sizes = ProductSize.objects.filter(size_status=True)
    
    return render(request, 'index.html', {
        'new_arrivals': new_arrivals, 
        'brands': brands, 
        'types': types, 
        'sizes': sizes,
        'products':products
    })



def sample(request):
    
    return render(request, 'sample.html')









    



def profile(request):
    user = request.user
    try:
        # Get the logged-in user's profile information
        user_info = UserInformation.objects.get(user=user)
    except UserInformation.DoesNotExist:
        # If no UserInformation exists, create a new one
        user_info = UserInformation(user=user)
        user_info.save()

    if request.method == 'POST':
        # Update user information based on the form data
        user_info.firstname = request.POST.get('first_name', user_info.firstname)
        user_info.lastname = request.POST.get('last_name', user_info.lastname)
        user_info.gender = request.POST.get('gender', user_info.gender)
        user_info.mobile = request.POST.get('mobile_number', user_info.mobile)
        
        # Save the updated profile information
        user_info.save()

        return redirect('profile')  # Redirect to the profile page after saving

    addresses = Addresses.objects.filter(user=user)  # Only show user's addresses
      # Get the selected address

    context = {
        'details': user_info,
        'addresses': addresses,
        
    }
    return render(request, 'profile.html', context)


def add_address(request):
    if request.method == 'POST':
        # Extract data from the form
        fullname = request.POST.get('fullname')
        mobilenumber = request.POST.get('mobilenumber')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        landmark = request.POST.get('landmark')
        city = request.POST.get('city')
        state = request.POST.get('state')
        
        if all([fullname, mobilenumber, pincode, address, landmark, city, state]):
            Addresses.objects.create(
                user=request.user,
                fullname=fullname,
                mobil_number=mobilenumber,
                pincode=pincode,
                address=address,
                landmark=landmark,
                city=city,
                state=state,
            ) 
            # messages.success(request, 'Address added successfully.')
            return redirect('profile')
        else:
            # messages.error(request, 'Please fill in all fields.')
            return redirect('profile')
    
    return render(request, 'profile.html')


def add_address_cart(request):
    if request.method == 'POST':
        # Extract data from the form
        fullname = request.POST.get('fullname')
        mobilenumber = request.POST.get('mobilenumber')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        landmark = request.POST.get('landmark')
        city = request.POST.get('city')
        state = request.POST.get('state')
        
        if all([fullname, mobilenumber, pincode, address, landmark, city, state]):
            Addresses.objects.create(
                user=request.user,
                fullname=fullname,
                mobil_number=mobilenumber,
                pincode=pincode,
                address=address,
                landmark=landmark,
                city=city,
                state=state,
            ) 
            messages.success(request, 'Address added successfully.')
            return redirect('cart')




def delete_address(request, address_id):
    address = get_object_or_404(Addresses, id=address_id)
    address.delete()
    return redirect('profile')   # Adjust the redirect URL as needed










def edit_address(request, address_id):
    addresses = get_object_or_404(Addresses, id=address_id)

    if request.method == 'POST':
        # Get form data from the request
        fullname = request.POST.get('fullname')
        mobil_number = request.POST.get('mobil_number')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        landmark = request.POST.get('landmark')  # Corrected typo here
        state = request.POST.get('state')
        source = request.POST.get('source')

        # Update the address object
        addresses.fullname = fullname
        addresses.mobil_number = mobil_number
        addresses.city = city
        addresses.pincode = pincode
        addresses.landmark = landmark
        addresses.state = state
        addresses.address = address
        addresses.save()
        if source == 'profile':
            return redirect('profile')
        elif source == 'cart':
            return redirect('cart')
    
    return render(request, 'edit_address.html', {'addresses': addresses})

    








def shop(request):
    products = Product.objects.filter(status=True).prefetch_related('variants__images').all()
    brands = Brand.objects.filter(brand_status=True)
    types = ProductType.objects.filter(type_status=True)
    sizes = ProductSize.objects.filter(size_status=True)

    

    # Get filters from request
    search_query = request.GET.get('search', None)
    brand_filter = request.GET.get('brand')
    type_filter = request.GET.get('type')
    size_filter = request.GET.get('size')
    sort_filter = request.GET.get('sort')

    if search_query:
        products = products.filter(
            Q(product_name__icontains=search_query)
        )
    
    # Apply filters to products
    if brand_filter:
        products = products.filter(productbrand_id=brand_filter)
    if type_filter:
        products = products.filter(producttype_id=type_filter)
    if size_filter:
        products = products.filter(productsize_id=size_filter)
    
    # Apply sorting
    if sort_filter == 'new_arrivals':
        products = products.order_by('-id')
    elif sort_filter == 'a_to_z':
        products = products.order_by('product_name')
    elif sort_filter == 'z_to_a':
        products = products.order_by('-product_name')
    elif sort_filter == 'price_low_to_high':
        products = products.order_by('price')
    elif sort_filter == 'price_high_to_low':
        products = products.order_by('-price')


    # Create paginator instance - Set items per page
    paginator = Paginator(products, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

          # Send the page object to the template
   

    return render(request, 'shop.html', {
        "products": products.distinct(),
        'brands': brands,
        'types': types,
        'sizes': sizes,
        'page_obj': page_obj,
    })









def single_product(request, product_id, variant_id, image_id):
    product = get_object_or_404(Product, id=product_id)
    
    
    reviews = Review.objects.filter(product=product)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    image = get_object_or_404(ProductImage, id=image_id)
    
    offer = ProductOffer.objects.filter(product=product_id)
    


    
    colors = ProductVariant.objects.filter(product=product_id).all()

    images = ProductImage.objects.filter(product_variant=variant)
    main_image = images.first()

    return render(request, 'single_product.html', {
        'product': product,
        'variant': variant,
        'images': images,
        'colors': colors,
        'img':main_image.images,
        'image':image,
        'reviews':reviews,
        
    })




@never_cache
def signup(request):
    if request.method == "POST":
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        email = request.POST['email'].strip()
        
        if User.objects.filter(Q(email=email) | Q(username=username)).exists():
            messages.info(request, 'User name or email already exists.')
            return redirect('signup')
        elif len(password) < 8:
            messages.info(request, 'Password must be at least 8 characters long.')
            return redirect('signup')
        else:
            User.objects.create_user(username=username, password=password, email=email)
            otp = generate_otp()
            send_otp_email(email, otp)
            store_otp_in_session(request, otp)
            request.session['email'] = email
            return redirect('verify_otp')
    
    return render(request, 'signup.html')


def generate_otp(length=6):
    digits = string.digits
    otp = ''.join(random.choice(digits) for _ in range(length))
    return otp

def send_otp_email(user_email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp}. It is valid for 1 minutes.'
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
    except Exception as e:
        print(f"Failed to send OTP email: {e}")

def store_otp_in_session(request, otp):
    expiration_time = time.time() + 60  
    request.session['otp'] = otp
    request.session['otp_expiration'] = expiration_time

def is_otp_valid(request, input_otp):
    stored_otp = request.session.get('otp')
    expiration_time = request.session.get('otp_expiration')

    if not stored_otp or not expiration_time:
        return False

    if time.time() < expiration_time and stored_otp == input_otp:
        return True
    return False

@never_cache
def verify_otp(request):
    if request.method == 'POST':
        input_otp = request.POST.get('otp')

        if not input_otp:
            messages.error(request, 'Please enter the OTP.')
            return redirect('verify_otp.html')

        if is_otp_valid(request, input_otp):
            del request.session['otp']
            del request.session['otp_expiration']
            messages.success(request, 'OTP verified successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Invalid or expired OTP. Please try again.')
            return redirect('verify_otp')

    otp_expiration = request.session.get('otp_expiration', 0)
    remaining_time = int(otp_expiration - time.time())
    remaining_time = max(remaining_time, 0)

    return render(request, 'verify_otp.html', {
        'remaining_time': remaining_time
    })

@never_cache
def resend_otp(request):
    email = request.session.get('email')

    if not email:
        messages.error(request, 'Email not found in session. Please start the signup process again.')
        return redirect('signup')

    otp = generate_otp()
    send_otp_email(email, otp)
    store_otp_in_session(request, otp)
    messages.success(request, 'A new OTP has been sent to your email.')

    return redirect('verify_otp')




def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            otp = generate_otp()
            send_otp_email(email, otp)
            store_otp_in_session(request, otp)
            request.session['email'] = email
            return redirect('verify_otp_forgot_pass')
        else:
            messages.error(request, 'Email address not found.')
            return redirect('forgot_password')
    return render(request, 'forgot_password.html')
        

    


def new_password_forgot_pass(request):
    email = request.session.get('email')  # Retrieve the email from the session

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if len(new_password) < 8:
            messages.error(request, 'New password must be at least 8 characters long.')
        elif new_password != confirm_password:
            messages.error(request, 'The new password and confirm password do not match.')
        else:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password changed successfully. Please log in with your new password.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'No user found with the provided email address.')

    return render(request, 'new_password_forgot_pass.html')


def verify_otp_forgot_pass(request):
    if request.method == 'POST':
        input_otp = request.POST.get('otp')

        if not input_otp:
            messages.error(request, 'Please enter the OTP.')
            return redirect('verify_otp.html')

        if is_otp_valid(request, input_otp):
            del request.session['otp']
            del request.session['otp_expiration']
            messages.success(request, 'OTP verified successfully!')
            return redirect('new_password_forgot_pass')
        else:
            messages.error(request, 'Invalid or expired OTP. Please try again.')
            redirect('verify_otp')

    otp_expiration = request.session.get('otp_expiration', 0)
    remaining_time = int(otp_expiration - time.time())
    remaining_time = max(remaining_time, 0)

    return render(request, 'verify_otp.html', {
        'remaining_time': remaining_time
    })


def cart(request):
    user = request.user
    items = Cart.objects.filter(user=user).order_by('-product')
    addresses = Addresses.objects.filter(user=user)
   
    wallet, created = Wallet.objects.get_or_create(user=user)    
    coupons = Coupon.objects.all()

    for coupon in coupons:
        if coupon.expiration_date < timezone.now():
            coupon.active = False
            coupon.save()
    try:
        used_coupons = CouponUsed.objects.filter(user=user).values_list('coupon_id', flat=True)
    except CouponUsed.DoesNotExist:
        used_coupons = None

    return render(request, 'cart.html', {'items': items, 'addresses':addresses, 'wallet':wallet, 'coupons': coupons, 'used_coupons': used_coupons})










def update_cart_quantity(request):
    user = request.user

    if not user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated.'}, status=401)

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')

        if not product_id or not quantity:
            return JsonResponse({'error': 'Product ID and quantity are required.'}, status=400)

        try:
            product_id = int(product_id)
            quantity = int(quantity)
        except ValueError:
            return JsonResponse({'error': 'Invalid input. Product ID and quantity must be integers.'}, status=400)

        if quantity <= 0:
            return JsonResponse({'error': 'Quantity must be greater than zero.'}, status=400)

        try:
            # Update the cart item quantity for the specific product
            cart_item, created = Cart.objects.get_or_create(user=user, product_id=product_id)
            cart_item.quantity = quantity
            cart_item.save()
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Cart item not found.'}, status=404)

        # Recalculate totals
        items = Cart.objects.filter(user=user)
        total_quantity = sum(item.quantity for item in items)
        total_amount = sum(item.variant.price * item.quantity for item in items)

        return JsonResponse({
            'total_quantity': total_quantity,
            'total_amount': total_amount,
            'item_quantity': cart_item.quantity,
            'item_total': cart_item.variant.price * cart_item.quantity
        })

    return JsonResponse({'error': 'Invalid request method.'}, status=405)




def addcart(request, product_id, variant_id, image_id):
    quantity = int(request.GET.get('quantity', 1))
    product = get_object_or_404(Product, id=product_id)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    image = get_object_or_404(ProductImage, id=image_id)
    user = request.user
    next_page = request.GET.get('next', 'single_product')
    
    if not user.is_authenticated:
        return redirect('login')

    # Check if the item is already in the cart
    cart_item, created = Cart.objects.get_or_create(user=user, product=product, variant=variant, image=image)
    
    if not created:
        if quantity + cart_item.quantity > variant.stock:
            messages.error(request,"Not enough stock")
            if next_page == 'wishlist':
                return redirect('wishlist')
            else:
                return redirect('single_product', product_id=product_id, variant_id=variant_id, image_id=image_id)
        else:
        # If the item is already in the cart, update the quantity
            cart_item.quantity += quantity
    else:
        # If the item is not in the cart, set the quantity to the selected value
        cart_item.quantity = quantity
    
    cart_item.save()

    

    # Redirect based on the next parameter value
    if next_page == 'wishlist':
        return redirect('wishlist')  # Assuming you have a wishlist URL name
    else:
        return redirect('single_product', product_id=product_id, variant_id=variant_id, image_id=image_id)  # Assuming you have a URL pattern named 'cart_page'


@require_POST
def update_quantity(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))

    if product_id and quantity:
        cart_item = Cart.objects.filter(product_id=product_id, user=request.user).first()
        if cart_item:
            cart_item.quantity = quantity
            cart_item.save()
            return JsonResponse({'success': True, 'quantity': cart_item.quantity})
        else:
            return JsonResponse({'success': False, 'error': 'Item not found in cart'})
    return JsonResponse({'success': False, 'error': 'Invalid data'})




def delete_cart(request, cart_id):

    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

    
def ordered(request, product_id,address_id):

    product = get_object_or_404(Product, id=product_id)
    product = get_object_or_404(Addresses, id=address_id)



    return render(request, 'ordered.html')













# Initialize Razorpay Client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

def place_order(request):
    if request.method == 'POST':
        # Extract cart items and other order-related details
        cart_items = Cart.objects.filter(user=request.user)
        address_id = request.POST.get('address')
        payment_method = request.POST.get('payment_method')
        coupon_code = request.POST.get('coupon')
        totalamount = Decimal(request.POST.get('total_amount'))

        if not address_id:
            messages.error(request, 'address not provided')
            return redirect('cart')


        if payment_method == 'wallet':
            wallet = Wallet.objects.get(user=request.user)
            if wallet.wallet_amount < totalamount:
                messages.error(request, "Insufficient wallet balance.")
                return redirect('cart')
            else:
                wallet.wallet_amount -= totalamount
                trans = totalamount
                wallet.save()
                Transaction.objects.create(
                wallet = wallet,
                transaction_amount = trans,
                type = 'Debit'
        )

        
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if not coupon.active or coupon.expiration_date < timezone.now():
                    coupon = None
                if not (coupon.minimum_amount <= totalamount <= coupon.maximum_amount):
                    coupon = None
            except Coupon.DoesNotExist:
                coupon = None
        else:
            coupon = None

        
      
        total_quantity = 0

        # Get selected address
        selected_address = Addresses.objects.get(id=address_id)

        # Calculate total amount and quantity
        for item in cart_items:
            # product_price = float(request.POST.get(f'price_{item.id}', 0))
            quantity = int(request.POST.get(f'quantity_{item.id}', 0))
            # total_amount += product_price * quantity
            total_quantity += quantity

       
        order = Order.objects.create(
            user=request.user,
            total_amount=totalamount,
            status='Pending',
            payment_method=payment_method,
            coupon=coupon,
            paid=(payment_method == 'wallet')
             
        )

        # Create the order address
        OrderAddress.objects.create(
            order=order,
            fullname=selected_address.fullname,
            mobil_number=selected_address.mobil_number,
            pincode=selected_address.pincode,
            address=selected_address.address,
            landmark=selected_address.landmark,
            city=selected_address.city,
            state=selected_address.state
        )

        # Create order items
        for item in cart_items:
            product = item.product
            variant = item.variant
            quantity = int(request.POST.get(f'quantity_{item.id}', 0))

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                variant=variant,
            )
            variant.stock -= quantity
            variant.save()

        cart_items.delete()
     

        
       

        if coupon is not None: 
            CouponUsed.objects.create(
            user = request.user,
            coupon = coupon  
            )

        if payment_method == 'razorpay':
            # Create Razorpay order
            razorpay_data = {
                "amount":  int(totalamount * 100) if totalamount else int(totalamount * 100),
                "currency": "INR",
                "receipt": f"order_{order.id}",
                "payment_capture": "1",  # Auto capture
            }
            razorpay_order = razorpay_client.order.create(data=razorpay_data)

            # Save Razorpay order ID to the order
            order.razorpay_order_id = razorpay_order['id']
            order.save()

            # Redirect to Razorpay checkout page
            return render(request, 'payment_page.html', {
                'order': order,
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_key': settings.RAZORPAY_API_KEY,
                'total_amount': totalamount,
            })

        # If not Razorpay, handle other payment methods (e.g., cash on delivery)
        return redirect('order_confirmation')



def continue_payment(request, order_id):

    order = get_object_or_404(Order, id=order_id)
    totalamount=order.total_amount

    razorpay_data = {
        "amount":  int(totalamount * 100) if totalamount else int(totalamount * 100),
        "currency": "INR",
        "receipt": f"order_{order.id}",
        "payment_capture": "1",  # Auto capture
    }
    razorpay_order = razorpay_client.order.create(data=razorpay_data) 
    order.razorpay_order_id = razorpay_order['id']
    order.save()

    return render(request, 'continue_payment_page.html', {
        'order': order,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key': settings.RAZORPAY_API_KEY,
        'total_amount': totalamount,
    })



@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        try:
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_signature = request.POST.get('razorpay_signature')
            order_id = request.POST.get('order_id')

            order = Order.objects.get(id=order_id)

            # Verify signature
            generated_signature = hmac.new(
                key=settings.RAZORPAY_API_SECRET.encode(),
                msg=f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
                digestmod=hashlib.sha256
            ).hexdigest()

            if generated_signature == razorpay_signature:
                # Payment is successful
                order.paid = True
                order.save()
                return redirect('order_confirmation')
            


            return JsonResponse({'status': 'Signature mismatch'}, status=400)

        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")
    return HttpResponseBadRequest("Invalid request")




@csrf_exempt
def verify_continue_payment(request):
    if request.method == 'POST':
        try:
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_signature = request.POST.get('razorpay_signature')
            order_id = request.POST.get('order_id')

            order = Order.objects.get(id=order_id)

            # Verify signature
            generated_signature = hmac.new(
                key=settings.RAZORPAY_API_SECRET.encode(),
                msg=f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
                digestmod=hashlib.sha256
            ).hexdigest()

            if generated_signature == razorpay_signature:
                # Payment is successful
                order.paid = True
                order.save()
                return redirect('my_order_details', order_id=order.id)

            return JsonResponse({'status': 'Signature mismatch'}, status=400)

        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")
    return HttpResponseBadRequest("Invalid request")


def payment_page(request):
    return render(request, 'payment_page.html')

from django.http import JsonResponse
from .models import Coupon

def validate_coupon(request):
    code = request.GET.get('code')
    total_amount = float(request.GET.get('total_amount'))

    try:
        coupon = Coupon.objects.get(code=code, active=True)

        if coupon.minimum_amount <= total_amount <= coupon.maximum_amount:
            return JsonResponse({
                'valid': True,
                'percentage': coupon.percentage,
                'minimum_amount': coupon.minimum_amount,
                'maximum_amount': coupon.maximum_amount,
            })
        else:
            return JsonResponse({
                'valid': False,
                'error': f"Coupon is only applicable for amounts between ₹{coupon.minimum_amount} and ₹{coupon.maximum_amount}."
            })

    except Coupon.DoesNotExist:
        return JsonResponse({
            'valid': False,
            'error': 'Invalid coupon code.'
        })


           
             


 

def order_confirmation(request):
    return render(request, 'order_confirmation.html')



def my_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-ordered_at')
    
    paginator = Paginator(orders, 6)  # Show 5 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'my_orders.html', {'orders':orders, 'page_obj': page_obj})



def my_order_details(request, order_id):
    
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order).all()
    address = get_object_or_404(OrderAddress, order=order)
    all_items_returned = all(item.item_return_request for item in order_items)


    return render(request, 'my_order_details.html', {'order_items':order_items, 'address':address, 'order':order, 'all_items_returned': all_items_returned})



def cancel_order(request, order_id):
    
    order = get_object_or_404(Order, id=order_id)
    wallet_item, created = Wallet.objects.get_or_create(user=request.user)
   

    if order.payment_method in ['razorpay', 'wallet'] and order.paid:
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

    # Redirect to the order details page
    return redirect('my_order_details', order_id = order_id)




def remove_order_item(request, order_id, order_item_id):
    # Retrieve the order and order item
    order = get_object_or_404(Order, id=order_id)
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    coupon = order.coupon

    # Try to retrieve the user's wallet, create one if it doesn't exist
    wallet_item, created = Wallet.objects.get_or_create(user=request.user)

    discount = 0
    
    # Calculate the discount if a coupon is applied
   
        # Determine the applicable offer
    if order_item.product.product_offer or order_item.product.brand_offer:
        brand_offer = order_item.product.productbrand.brandoffers.first()
        product_offer = order_item.product.productoffers.first()
        if brand_offer and product_offer:
            if brand_offer.brand_offer_percentage > product_offer.product_offer_percentage:
                if coupon:
                    discount = (coupon.percentage / 100) * order_item.product.brand_offer * order_item.quantity
                else:
                    discount = order_item.product.brand_offer * order_item.quantity   
            else:
                if coupon:
                    discount = (coupon.percentage / 100) * order_item.product.product_offer * order_item.quantity
                else:
                    discount = order_item.product.product_offer * order_item.quantity
        elif brand_offer:
            if coupon:
                discount = (coupon.percentage / 100) * order_item.product.brand_offer * order_item.quantity
            else:
                discount = order_item.product.brand_offer * order_item.quantity
        elif product_offer:
            if coupon:
                discount = (coupon.percentage / 100) * order_item.product.product_offer * order_item.quantity
            else:
                discount = order_item.product.product_offer * order_item.quantity
    else:
        if coupon:
            discount = (coupon.percentage / 100) * order_item.product.price * order_item.quantity
        else:
            discount = order_item.product.price * order_item.quantity


    order.total_amount -= Decimal(discount)

    # Update the wallet amount
    if order.payment_method in ['razorpay', 'wallet'] and order.paid:
        wallet_item.wallet_amount += discount
        wallet_item.save()

        Transaction.objects.create(
        wallet=wallet_item,
        transaction_amount=discount,
        type = 'Credit'
    )
    
    order.save()

    # Mark the order item as inactive
    order_item.order_item_status = 'Cancelled'
    order_item.save()

    if order.items.filter(order_item_status='Cancelled').count() == order.items.count():
        order.status = 'Cancelled'
        order.total_amount = 0
        order.save()


    # Update stock for the removed order item
    variant = order_item.variant
    variant.stock += order_item.quantity
    variant.save()

    # Create a transaction record for the wallet refund
    

    # Redirect to order details page
    return redirect('my_order_details', order_id=order_id)





def wishlist(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Get the wishlist items for the logged-in user
    wishlist_items = Wishlist.objects.filter(user=request.user)

    paginator = Paginator(wishlist_items, 4)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items, 'page_obj':page_obj})









def add_to_wishlist(request, product_id, variant_id, image_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    product = get_object_or_404(Product, id=product_id)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    image = get_object_or_404(ProductImage, id=image_id)

    user = request.user
    
    # Check if the specific product variant with the image is already in the user's wishlist
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=user,
        products=product,
        variant=variant
    )

    return redirect('single_product', product_id=product.id, variant_id=variant.id, image_id=image.id)



def remove_wishlist(request, item_id):
    # Assuming the user is authenticated
    user = request.user
    
    # Get the wishlist item based on the item_id, and remove it for the user
    wishlist_item = get_object_or_404(Wishlist, id=item_id, user=user)
    
    # Remove the item from the wishlist
    wishlist_item.delete()
    
    # Redirect back to the wishlist page
    return redirect('wishlist')



def wallet(request):
    # Get or create the user's wallet
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    
    # Fetch transactions related to this wallet, ordered by the most recent
    transactions = Transaction.objects.filter(wallet=wallet).order_by('-created_at')

    # Paginate the transactions, showing 7 per page
    paginator = Paginator(transactions, 7)  # Show 7 transactions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass both the wallet and paginated transactions to the template
    return render(request, 'wallet.html', {
        'wallet': wallet,
        'page_obj': page_obj
    })


from io import BytesIO
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa

def generate_invoice(request, order_id):
    # Get the order
    order = Order.objects.get(id=order_id, user=request.user)

    # Render the HTML template with context
    context = {
        'order': order,
    }
    html = render_to_string('invoice_template.html', context)

    # Create a BytesIO buffer for the PDF
    buffer = BytesIO()

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html, dest=buffer)

    # Check if there were any errors
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    # Get the value of the BytesIO buffer and create a response
    pdf = buffer.getvalue()
    buffer.close()

    # Return the PDF as a response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_{order_id}.pdf'
    return response





def item_return_request(request, order_item_id, order_id):

    order_item = get_object_or_404(OrderItem, id=order_item_id)
    order_item.item_return_request = True
    order_item.save()
    
    return redirect('my_order_details', order_id = order_id)




def submit_review(request, product_id, variant_id, image_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('review')

        if rating and comment:
            review = Review(user=request.user, product_id=product_id, rating=rating, comment=comment)
            review.save()
            

        return redirect('single_product', product_id=product_id, variant_id=variant_id, image_id=image_id)