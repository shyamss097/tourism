from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def homepage(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_manager = form.cleaned_data['is_manager']
            user.save()
            # authenticate and log in the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            # redirect to appropriate dashboard
            if user.is_manager:
                return redirect('home')
            else:
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request,'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') # Replace 'home' with your desired redirect URL
        else:
            # Show an error message if authentication fails
            error_message = "Invalid login credentials. Please try again."
            return render(request, 'registration/login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


def package_list(request):
    packages = Package.objects.all()
    return render(request, 'package_list.html', {'packages': packages})



def package_detail(request, pk):
    package = get_object_or_404(Package, pk=pk)

    # get all accommodations and their prices
    accommodations = Accommodation.objects.all().values('id', 'name', 'price')
    # get all foods and their prices
    foods = Food.objects.all().values('id', 'name', 'price')

    if request.method == 'POST':
        # get selected accommodation and its price
        accommodation_id = request.POST.get('accommodation')
        if accommodation_id:
            accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
            accommodation_price = accommodation.price
        else:
            accommodation = None
            accommodation_price = 0

        # get selected food and its price
        food_id = request.POST.get('food')
        if food_id:
            food = get_object_or_404(Food, pk=food_id)
            food_price = food.price
        else:
            food = None
            food_price = 0

        # calculate total cost
        total_duration = package.duration
        total_food_cost = total_duration * food_price * 3
        total_accommodation_cost = total_duration * accommodation_price

        # render template with selected options and total cost
        return render(request, 'travel/package_detail.html', {
            'package': package,
            'accommodations': accommodations,
            'foods': foods,
            'selected_accommodation': accommodation,
            'selected_food': food,
            'total_food_cost': total_food_cost,
            'total_accommodation_cost': total_accommodation_cost,
            'total_cost': package.price + total_food_cost + total_accommodation_cost,
        })

    # render template with all options and no selections
    return render(request, 'package_detail.html', {
        'package': package,
        'accommodations': accommodations,
        'foods': foods,
        'selected_accommodation': None,
        'selected_food': None,
        'total_food_cost': 0,
        'total_accommodation_cost': 0,
        'total_cost': package.price,
    })


def add_to_cart(request, package_id):
    # Retrieve the package
    package = get_object_or_404(Package, pk=package_id)

    # Get the selected food and accommodation types from the form
    selected_foods = request.POST.getlist('food')
    selected_accommodation_id = request.POST.get('accommodation')
    selected_accommodation = get_object_or_404(Accommodation, pk=selected_accommodation_id)

    # Calculate the total cost of the package based on the selected options
    duration = int(request.POST.get('duration'))
    selected_foods = [food for food in selected_foods if isinstance(food, Food)]
    food_cost = sum([food.price for food in selected_foods]) * duration * 3  # 3 meals per day
    accommodation_cost = selected_accommodation.price * duration
    total_price = package.price + food_cost + accommodation_cost

    # Create a new cart item and add the selected food and accommodation types
    cart_item = CartItem(package=package, duration=duration, accommodation=selected_accommodation, total_price=total_price,  user=request.user)
    cart_item.save()
    cart_item.food.set(selected_foods)  # Use set() to add selected foods to the cart item

    

    # Redirect to the cart page
    return redirect('view-cart')

def view_cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    
   
    context = {'cart_items': cart_items}
    return render(request, 'cart.html', context)

def get_cart_total_price(cart):
    total_price = 0
    for item in cart.cartitem_set.all():
        total_price += item.total_price
    return total_price

# @login_required
# def checkout(request, pk):
#     package = get_object_or_404(Package, pk=pk)
#     cart = request.user.cart
#     duration = package.duration
#     selected_foods = cart.food.all()
#     selected_accommodation = cart.accommodation
#     food_cost = sum([food.price for food in selected_foods]) * duration * 3  # 3 meals per day
#     accommodation_cost = selected_accommodation.price * duration
#     total_price = package.price + food_cost + accommodation_cost
#     order = Order.objects.create(user=request.user, package=package, total_price=total_price)
#     cart.delete()
#     return render(request, 'checkout.html', {'order': order})

@login_required
def checkout(request, package_id):
    user = request.user
    cart = user.cart

    if not cart.items.exists():
        return redirect('view-cart')

    package = get_object_or_404(Package, id=package_id)

    food_cost = sum([item.food.price for item in cart.items.all()]) * package.duration * 3
    accommodation_cost = sum([item.accommodation.price for item in cart.items.all()]) * package.duration

    total_price = food_cost + accommodation_cost + package.price

    # create the order
    order = user.orders.create(package=package, total_price=total_price)

    # save the cart items to the order
    for item in cart.items.all():
        order.items.create(package=item.package, duration=item.duration, food=item.food, accommodation=item.accommodation, total_price=item.total_price)

    # clear the cart
    cart.items.all().delete()

    # render the ticket template
    return render(request, 'ticket.html', {'order': order})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    if request.method == 'POST':
        cart_item.delete()
        return redirect('view-cart')
    context = {
        'cart_item': cart_item
    }
    return render(request, 'remove_from_cart.html', context)
