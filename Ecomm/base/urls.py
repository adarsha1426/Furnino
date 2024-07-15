from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name="home"),
    
    path('login/',views.login_view,name="login"),
    path('register/',views.register,name="register"),
    path('logout',views.logout,name="logout"),
    path('categories/',views.categories,name="categories"),
    path('product_list',views.product_list,name="product_list"),
    path('category/<str:name>',views.category,name="category"),
    path('cart/',views.view_cart,name="cart"),
    path('add/<int:product_id>',views.add_to_cart,name="add"),
    path('accounts/login/',views.login_view,name='login'),
    path('remove/<int:product_id>',views.remove_item,name="delete"),
    path('description/<str:name>',views.description,name="description"),
    path('checkout/',views.checkout,name="checkout"),
    path('accounts/login',views.login_view,name="login"),
    path('buy/<int:product_id>',views.buy_now,name="buy"),
    path('update/<int:product_id>',views.cart_quantity,name="update"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
