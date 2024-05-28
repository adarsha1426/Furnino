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
    path('add/<int:id>',views.add_to_cart,name="add"),
    path('description/<str:name>',views.description,name="description"),
    path('checkout/',views.checkout,name="checkout"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
