from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.auth.models import User


@login_required(login_url='/users/sign_in')
def home(request):
    foods = Food.objects.all()
    category = request.GET.get('category')
    search = request.GET.get('search')
    establishments = Establishments.objects.all()
    establishments = establishments.filter(
        Q(name__icontains=search)) if search else establishments
    foods = foods.filter(
        Q(name__icontains=search)) if search else foods
    establishments = establishments.filter(type=category) if category else establishments
    return render(request, 'home.html', {'foods': foods, 'establishments': establishments})


def create_establishment(request):
    form = EstablishmentCreationForm(request.POST or None, request.FILES or None)
    locationform = LocationForm(request.POST)
    user = request.user
    if form.is_valid() and request.method == 'POST':
        if locationform.is_valid():
            location = locationform.save()
            a = form.save(commit=False)
            a.user = user
            a.location = location
            a.save()
            return redirect('delivery:detail_establishment', a.pk)
    print(form.errors)
    return render(request, 'create_establishment.html', {'form': form, 'locationform': locationform})


def detail_establishment(request, pk):
    establishment = Establishments.objects.get(pk=pk)
    foods = Food.objects.filter(establishment=establishment)
    user = request.user
    if user.usertype.establishment:
        categories2 = FoodCategory.objects.filter(food__in=foods, food__establishment=establishment)
        categories = []
        for item in categories2:
            if item not in categories:
                categories.append(item)
    else:
        customer = Customer.objects.get(user=request.user)
        food_id = request.GET.get('food')
        cart_items = CartItem.objects.filter(customer=customer)
        if food_id:
            food = Food.objects.get(id=food_id)
            cart_item = CartItem.objects.filter(food=food, customer=customer)
            if cart_items:
                for item2 in cart_items:
                    if food.establishment.name == item2.food.establishment.name:
                        if not cart_item:
                            CartItem.objects.create(
                                customer=customer,
                                food=food,
                                quantity=1
                            )
                            return redirect('delivery:detail_establishment', food.establishment.pk)

                        for item in cart_item:
                            item.quantity += 1
                            item.save()
                            return redirect('delivery:detail_establishment', food.establishment.pk)
            else:
                if not cart_item:
                    CartItem.objects.create(
                        customer=customer,
                        food=food,
                        quantity=1
                    )
                    return redirect('delivery:detail_establishment', food.establishment.pk)

                for item in cart_item:
                    item.quantity += 1
                    item.save()
                    return redirect('delivery:detail_establishment', food.establishment.pk)
            return render(request, 'error.html')
        categories2 = FoodCategory.objects.filter(food__in=foods, food__establishment=establishment)
        categories = []
        for item in categories2:
            if item not in categories:
                categories.append(item)
    return render(request, 'detail_establishment.html',
                  {'establishment': establishment, 'categories': categories, 'foods': foods})


def create_food(request):
    form = FoodCreationForm(request.POST or None, request.FILES or None)
    establishment = Establishments.objects.get(user=request.user)
    if request.method == 'POST' and form.is_valid():
        food = form.save(commit=False)
        food.establishment = establishment
        food.save()
        return redirect('delivery:detail_food', food.pk)
    return render(request, 'create_food.html', {'form': form})


def detail_food(request, pk):
    food = Food.objects.get(pk=pk)
    return render(request, 'detail_food.html', {'food': food})


def create_order(request):
    customer = Customer.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(customer=customer)
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])
    user = request.user
    form = OrderForm(request.POST)
    customer = Customer.objects.get(user=user)

    if not cart_items:
        return render(request, 'error.html')

    if request.method == 'POST' and form.is_valid():
        order = Order.objects.create(
            customer=user,
            address=customer.phone,
            total_price=total_price,
        )
        for cart_item in cart_items:
            OrderProduct.objects.create(
                order=order,
                product=cart_item.product,
                amount=cart_item.quantity,
                total=cart_item.total_price()
            )
        cart_items.delete()
        return redirect('users:profile')
    return render(request, 'orders.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
        'form': form
    })


def customer_create(request):
    user = request.user
    form = CustomerCreationForm(request.POST)
    locationform = LocationForm(request.POST)
    if form.is_valid() and request.method == 'POST':
        if locationform.is_valid():
            location = locationform.save()
            a = form.save(commit=False)
            a.user = user
            a.location = location
            a.save()
            return redirect('delivery:home')
    return render(request, 'customer_creation.html', {'form': form, 'locationform': locationform})


def create_order(request):
    if request.user.usertype.establishment == False:
        customer = Customer.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(customer=customer)
        for a in cart_items:
            establishments = [a]
            for i in establishments:
                establishment = a.food.establishment
        total_price = sum([item.total_price() for item in cart_items])
        total_quantity = sum([item.quantity for item in cart_items])
        form = OrderForm(request.POST)

        if not cart_items:
            return render(request, 'error.html')

        if request.method == 'POST' and form.is_valid():
            order = Order.objects.create(
                customer=customer,
                address=request.POST.get('address'),
                phone=request.POST.get('phone'),
                total_price=total_price,
                establishment=establishment
            )
            for cart_item in cart_items:
                OrderProduct.objects.create(
                    order=order,
                    food=cart_item.food,
                    amount=cart_item.quantity,
                    total=cart_item.total_price()
                )
            cart_items.delete()
            return redirect('users:profile')
        form = OrderForm(instance=customer)

    return render(request, 'order_creation_page.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
        'form': form
    })




def establishment_orders(request):
    establishment = Establishments.objects.get(user=request.user)
    if request.user == establishment.user:
        orders = Order.objects.filter(establishment=establishment)
    return render(request, 'establishment_orders.html', {"orders": orders})


def edit_food(request, pk):
    food = Food.objects.get(pk=pk)
    if request.user == food.establishment.user:
        form = FoodCreationForm(request.POST or None, request.FILES or None, instance=food)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('delivery:detail_establishment', food.establishment.pk)

    return render(request, 'edit_food.html', {'form': form})


def delete_food(request, pk):
    food = Food.objects.get(pk=pk)
    if request.user == food.establishment.user:
        food.delete()
        return redirect('delivery:detail_establishment', food.establishment.pk)
    return redirect('delivery:home')


def cart(request):
    if request.user.usertype.establishment == False:
        customer = Customer.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(customer=customer)
        total_price = sum([item.total_price() for item in cart_items])
        total_quantity = sum([item.quantity for item in cart_items])

    return render(request, 'cart.html',
                  {'cart_items': cart_items, 'total_quantity': total_quantity, 'total_price': total_price})


def delete_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk).delete()
    return redirect('delivery:cart')


def edit_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    action = request.GET.get('action')

    if action == 'decrement' and cart_item.quantity == 1:
        cart_item.delete()
        return redirect('delivery:cart')
    if action == 'decrement' and cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        return redirect('delivery:cart')
    cart_item.quantity += 1
    cart_item.save()
    return redirect('delivery:cart')


def is_success(request, pk):
    order = Order.objects.get(pk=pk)
    order.readiness = True
    order.save()
    return redirect('delivery:establishment_orders')