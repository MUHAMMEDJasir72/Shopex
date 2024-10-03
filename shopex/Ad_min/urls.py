
from django.urls import path
from.import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin_home', views.admin_home, name='admin_home'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('base/',views.base,name='base'),
    path('products/',views.products,name='products'),
    path('users/',views.users,name='users'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock-user/<int:id>/', views.unblock_user, name='unblock_user'),
    path('add_product/',views.add_product, name='add_product'),
    path('product_details/<int:product_id>/',views.product_details, name='product_details'),
    path('brands/',views.brands, name='brands'),
    path('product_type/',views.product_type, name='product_type'),
    path('product_size/',views.product_size, name='product_size'),
    path('block_product/<int:product_id>/',views.block_product,name='block_product'),
    path('unblock_product/<int:product_id>/',views.unblock_product,name='unblock_product'),
    path('update_product/<int:product_id>/',views.update_product,name='update_product'),
    path('update_variant/<int:variant_id>/',views.update_variant,name='update_variant'),
    path('orders/',views.orders_view,name='orders'),
    path('order_details/<int:order_id>/',views.order_details,name='order_details'),
    path('order_status/<int:order_id>/status/<str:new_status>/',views.order_status,name='order_status'),
    path('change_brand_status/<int:brand_id>/', views.change_brand_status, name='change_brand_status'),
    path('change_size_status/<int:size_id>/', views.change_size_status, name='change_size_status'),
    path('change_type_status/<int:type_id>/', views.change_type_status, name='change_type_status'),
    path('product_offer/',views.product_offer,name='product_offer'),
    path('delete_product_offer/<int:offer_id>/',views.delete_product_offer,name='delete_product_offer'),
    path('brand_offer/',views.brand_offer,name='brand_offer'),
    path('delete_brand_offer/<int:offer_id>/',views.delete_brand_offer,name='delete_brand_offer'),
    path('coupons/',views.coupons,name='coupons'),
    path('delete_coupon/<int:coupon_id>/',views.delete_coupon,name='delete_coupon'),
    path('sales_report/',views.sales_report,name='sales_report'),
    path('export_sales_report_excel/', views.export_sales_report_excel, name='export_sales_report_excel'),
    path('export_sales_report_pdf/', views.export_sales_report_pdf, name='export_sales_report_pdf'),
    path('edit_product_offer/<int:offer_id>/', views.edit_product_offer, name='edit_product_offer'),
    path('edit_brand_offer/<int:offer_id>/', views.edit_brand_offer, name='edit_brand_offer'),
    path('remove_user_order/<int:order_id>/<int:order_item_id>/',views.remove_user_order,name='remove_user_order'),
    path('cancel_user_order/<int:order_id>/',views.cancel_user_order,name='cancel_user_order'),
    path('total_sales_count/', views.total_sales_count, name='total_sales_count'),
    path('approve_return/<int:order_id>/', views.approve_return, name='approve_return'),
    path('approve_item_return/<int:order_id>/<int:order_item_id>/', views.approve_item_return, name='approve_item_return'),
    path('edit_coupon/', views.edit_coupon, name='edit_coupon'),





    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

