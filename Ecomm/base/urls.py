from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name="home"),
    path('cart/',views.cart,name="cart"),
    path('login/',views.login_view,name="login"),
    path('register/',views.register,name="register"),
    path('logout',views.logout,name="logout"),
    path('product/',views.product,name="product"),
    path('category/<str:name>',views.category,name="category"),
]
