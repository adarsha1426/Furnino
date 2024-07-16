from django.db import models
from django.conf import settings
import uuid
class Category(models.Model):
    name = models.CharField(max_length=200)  # dining, living, kitchen
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/', blank=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"])
        ]

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id'], name='unique_user_customer')
        ]
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    items = models.ManyToManyField(Product)
    transaction_id=uuid.uuid4()


    def __str__(self):
        return f"Order #{self.id} by {self.customer.full_name}"

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_cost() for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
   

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0)
    complete = models.BooleanField(default=False, null=True, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Ensure this matches the User model

    def __str__(self):
        return f"OrderItem {self.id} ({self.quantity} x {self.product.name})"

    def get_cost(self):
        return self.product.price * self.quantity
