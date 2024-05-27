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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['customer','date_ordered']
    list_filter=('customer',)
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'quantity']
    list_filter=('product',)
    def save_model(self, request, obj, form, change):
        # If an order instance is not provided, create one for the current user
        if not obj.order:
            # Assuming you have logic to retrieve or create an order for the current user
            order_instance, created = Order.objects.get_or_create(user=request.user, ordered=False)
            obj.order = order_instance
        obj.save()

admin.site.register(Customer)
