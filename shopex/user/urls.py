
from django.urls import path
from.import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('confirm_password/', views.confirm_password, name='confirm_password'),
    path('new_password/', views.new_password, name='new_password'),
    path('new_password_forgot_pass/', views.new_password_forgot_pass, name='new_password_forgot_pass'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp_forgot_pass/', views.verify_otp_forgot_pass, name='verify_otp_forgot_pass'),
    path('', views.index, name='index'),
    path('profile/',views.profile,name='profile'),
    path('sample/', views.sample, name='sample'),
    path('shop/',views.shop,name='shop'),
    path('user_base/',views.user_base,name='user_base'),
    path('single_product/<int:product_id>/<int:variant_id>/<int:image_id>/',views.single_product,name='single_product'),
    path('verify_otp/',views.verify_otp,name='verify_otp'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    path('add_address/', views.add_address, name='add_address'),
    path('add_address_cart/', views.add_address_cart, name='add_address_cart'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('addcart/<int:product_id>/<int:variant_id>/<int:image_id>/',views.addcart,name='addcart'),
    path('cart/',views.cart,name='cart'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('delete_cart/<int:cart_id>/',views.delete_cart,name='delete_cart'),
    path('update-cart-quantity/', views.update_cart_quantity, name='update_cart_quantity'),
    path('ordered/<int:product_id>/<int:address_id>/', views.ordered, name='ordered'),
    path('place_order/',views.place_order,name='place_order'),
    path('order_confirmation/',views.order_confirmation,name='order_confirmation'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('my_order_details/<int:order_id>/',views.my_order_details,name='my_order_details'),
    path('cancel_order/<int:order_id>/',views.cancel_order,name='cancel_order'),
    path('remove_order_item/<int:order_id>/<int:order_item_id>/',views.remove_order_item,name='remove_order_item'),
    path('validate-coupon/',views.validate_coupon, name='validate_coupon'),
    path('verify_payment-payment/', views.verify_payment, name='verify_payment'),
    path('verify_continue_payment-payment/', views.verify_continue_payment, name='verify_continue_payment'),
    path('payment_page/', views.payment_page, name='payment_page'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/<int:variant_id>/<int:image_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_wishlist/<int:item_id>/',views.remove_wishlist,name='remove_wishlist'),
    path('wallet/', views.wallet, name='wallet'),
    path('generate_invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),
    path('continue_payment/<int:order_id>/', views.continue_payment, name='continue_payment'),
    path('item_return_request/<int:order_item_id>/<int:order_id>/', views.item_return_request, name='item_return_request'),
    path('submit_review/<int:product_id>/<int:variant_id>/<int:image_id>/', views.submit_review, name='submit_review'),









    
   


 

   
    

]


