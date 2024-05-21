from django.contrib import admin
from .models import Category,Product,User,Order,OrderItem,Customer
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','slug']
    prepopulated_fields={'slug':('name',)}
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','slug','category','price')
    list_filter=('category',)
    prepopulated_fields={'slug':('name',)}


admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)
