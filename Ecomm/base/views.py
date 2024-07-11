from django.db import IntegrityError
from django.shortcuts import render,redirect,HttpResponse
from .forms import LoginForm,RegisterForm
from django.contrib.auth import authenticate,login,logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category,Product,Customer,Order,OrderItem
from django.shortcuts import get_object_or_404
from django.urls  import reverse

# Create your views here.

def home(request):
    return render(request,'base/home.html')

def login_view(request):
# Redirect logged-in users
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # Authenticate user with form data
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)  # Only call login if user is valid
                return redirect("home")
            elif user is not None and not user.is_active:
                messages.error(request, "Account is inactive.")
            else:
                messages.error(request, "Invalid login credentials.")
        else:
            messages.error(request, "Form validation failed.")
    # If GET request or invalid POST, render the login page with form
    form = LoginForm()  # Create an empty form
    return render(request, "registration\login_page.html", {"form": form})

def logout(request):
    auth_logout(request)  # Logs the user out
    messages.success(request, "You have been logged out successfully.")  # Add success message
    return redirect("login") 

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.save()
            login(request,user)
            return redirect('home')
            messages.success(request,"Account Created successful")
            # Optionally, you can add any additional actions after saving the user here
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

def categories(request):
    return render(request,'base/categories.html')

def category(request,name):
    category=get_object_or_404(Category,name=name)
    if category.name=='Dining':
        product=Product.objects.filter(category=category)
        product_name=category.name
        return render(request,'base/bedroom.html',
                  {
                      'product':product,
                      "product_name":product_name,
                  })
    
    
    elif category.name=='Living':
        product=Product.objects.filter(category=category)
        product_name=category.name
        return render(request,'base/bedroom.html',
                  {
                      'product':product,
                      "product_name":product_name,
                  })
    
    elif category.name=='Bedroom':
        product=Product.objects.filter(category=category)
        product_name=category.name
        return render(request,'base/bedroom.html',
                  {
                      'product':product,
                      "product_name":product_name,
                  })
    
    else:
        return HttpResponse("Error")
    
#product description
def description(request,name):
    description=Product.objects.filter(name=name)
    return render(request,"base/product-description.html",
                  {
                      "description":description,
                      
                  })
#listing all the product in products page
def product_list(request):
    product=Product.objects.all()
    return render(request,"base/product_list.html",{
        "product":product
    })

def view_cart(request):
    if request.user:
        try:
            user = request.user
            customer = Customer.objects.get(user=user)
            order = Order.objects.filter(customer=customer, complete=False).first()
            if order:
                items = OrderItem.objects.all()
                print(f"Items in cart for {request.user.username}: {[item.product.name for item in items]}")
            else:
                items = []
                print(f"No active order found for {request.user.username}")
        except Customer.DoesNotExist:
            items = []
            print(f"No customer found for user {request.user.username}")
    else:
        items = []
        print("User is not authenticated")
    return render(request, 'base/cart.html', {"items": items})

def add_to_cart(request, id):
    item = get_object_or_404(Product, id=id)
    user = request.user.is_authenticated
    customer = Customer.objects.get(user=user)
    # Retrieve the most recent incomplete order for the customer
    order = Order.objects.filter(customer=customer, complete=False).order_by('-date_ordered').first()
    if order is None:
        order = Order.objects.create(customer=customer, complete=False)
    # Get or create the order item for the product within the selected order
    order_item, created = OrderItem.objects.get_or_create(product=item, order=order)
    # If the order item already exists in the order, increase the quantity
    if not created:
        order_item.quantity += 1
        order_item.save()
    return redirect('product_list')   # Redirect to the product list page

def checkout(request):
    items=OrderItem.objects.all()
    return render(request, 'base/checkout.html', {'items': items,})