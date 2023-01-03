from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.login, name='login'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('admin_add_serviceprovider/',views.admin_add_serviceprovider,name='admin_add_serviceprovider'),
    path('admin_serviceprovider_view/',views.admin_serviceprovider_view,name='admin_serviceprovider_view'),
    path('admin_serviceprovider_edit/',views.admin_serviceprovider_edit,name='admin_serviceprovider_edit'),
    path('logout_admin/',views.logout_admin,name='logout_admin'),
    path('service_home/',views.service_home,name='service_home'),
    path('add_products/',views.add_products,name='add_products'),
    path('service_provider_product_view/',views.service_provider_product_view,name='service_provider_product_view'),
    path('service_provider_product_edit/',views.service_provider_product_edit,name='service_provider_product_edit'),
    path('service_provider_order_view/',views.service_provider_order_view,name='service_provider_order_view'),
    path('service_provider_order_history/',views.service_provider_order_history,name='service_provider_order_history'),
    path('logout_service_provider/',views.logout_service_provider,name='logout_service_provider'),
    path('user_register/',views.user_register,name='user_register'),
    path('user_home/',views.user_home,name='user_home'),
    path('view_orders_user/',views.view_orders_user,name='view_orders_user'),
    path('history_orders_user/',views.history_orders_user,name='history_orders_user'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('chat_section/',views.chat_section,name='chat_section'),
    path('user_soil/',views.user_soil,name='user_soil'),
    path('user_soil_history/',views.user_soil_history,name='user_soil_history'),
    path('service_provider_soil/',views.service_provider_soil,name='service_provider_soil'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)