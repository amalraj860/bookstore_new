from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views





urlpatterns = [
    # path('', HomeView.as_view(), name='home-page'),
    path('', views.HomeView, name='home-page'),
    # path('profile/', UserProfile.as_view(), name='user-profile'),
    path('profile/', views.UserProfile, name='user-profile'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('product-list/', views.product_list, name='product-list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('cart/', views.view_cart, name='cart'),
    path('increase-cart-item/<int:product_id>/', views.increase_cart_item, name='increase-cart-item'),
    path('decrease-cart-item/<int:product_id>/', views.decrease_cart_item, name='decrease-cart-item'),
    path('fetch-cart-count/', views.fetch_cart_count, name='fetch-cart-count'),
    path('fetch-cart-count/', views.fetch_cart_count, name='fetch-cart-count'),
    path('create-order/', views.create_order, name='create-order'),
    path('handle-payment/', views.handle_payment, name='handle-payment'),
    path('checkout/', views.checkout, name='checkout'),
    # path('download-receipt/<int:order_id>/', views.generate_receipt_pdf, name='download-receipt'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)