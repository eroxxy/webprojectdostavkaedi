from xmlrpc.client import DateTime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.db import IntegrityError
from orders.models import Price, PizzaTopping, FoodSize, PizzaType, PizzaOrder
from django.db.models import Q
from datetime import datetime

def index(request):
    """
    If a user is authenticated then this controls menu and ordering.
    If an admin is authenticated then this controls the showing of orders and marking orders
    complete
    """

    if not request.user.is_authenticated:
        return render(request, "orders/fancy_login.html", {"message": None})

    if request.method == 'POST':
        if request.POST.get("del", "") == "false":
            order_data = request.POST
            order_to_basket(order_data, request)
        else:
            pid = request.POST.get("id", "")
            delOrder = PizzaOrder.objects.get(id=pid)
            delOrder.delete()
        

    basket_data, basket_total = get_basket_contents(request)

    checkout_data = get_processed_orders()

    context = {
        "user": request.user,
        "basket": basket_data,
        "basket_total": basket_total,
        "checkout": checkout_data,
        "menu": {
            'Pizzas': [str(i) for i in Price.objects.all() if i.food_type == 'Pizza'],
        },
        "pizza_toppings": PizzaTopping.objects.all(),
    }

    # redirect depending on admin or user profile
    if User.objects.get(username=request.user).is_staff:
        return render(request, "orders/admin.html", context)
    else:
        return render(request, "orders/user.html", context)

def login_view(request):
    """allows a user to login"""
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('index')
    else:
        return render(request, "orders/fancy_login.html", {"message": "Invalid credentials."})


def logout_view(request):
    """allows a user to logout"""
    logout(request)
    return render(request, "orders/fancy_login.html", {"message": "Logged out."})


def register_view(request):
    """allows a new user to register their information"""
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        # print(username)
        # if any of the fields are blank - restart registration with message
        for val in [username, password, first_name, last_name, email]:
            if val == '':
                return render(request, "orders/fancy_register.html", {"message": "fill in all fields"})
        try:
            user = User.objects.create_user(
                username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        except IntegrityError:
            return render(request, "orders/fancy_register.html", {"message":  "This username is taken"})
        user.save()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('login')
        else:
            return render(request, "orders/fancy_register.html", {"message": "Invalid credentials."})
    return render(request, "orders/fancy_register.html", {"message": None})


def order_status(request):
    """
    if user: marks all basket items as 'Ordered'
    if admin: marks selected order as 'Complete'
    """

    if 'admin_form' in request.POST:
        model = f"{request.POST['food_type'][:-1]}Order"
        model = globals()[model]

        order = model.objects.filter(pk=request.POST['id']).first()

        if order.status == 'Ordered':
            order.status = 'Processing'
        elif order.status == 'Processing':
            order.status = 'Sent'
        elif order.status == 'Sent':
            order.status = 'Complete'

        order.save()

    models = [PizzaOrder]

    for model in models:
        for item in model.objects.filter(user=request.user.username, status='Draft').all():
            item.status = 'Ordered'
            item.date = datetime.now()
            item.save()

    return redirect('index')


def order_to_basket(order_data, request):
    """creates a 'draft' order entry in the database"""
    models = {
        'Pizzas': (PizzaType, PizzaOrder, PizzaTopping)
    }

    # get all the required query data from order
    food_type = models[order_data['food_type']][0].objects.filter(
        name=order_data['food_item']).first()

    if order_data['food_type'] in ['Pizzas', 'Subs', 'Platters']:
        if order_data['food_type'] == 'Pizzas':
            food_type = PizzaType.objects.filter(
                name=order_data['food_item'].split()[0]).first()
        size = FoodSize.objects.filter(size=order_data['size']).first()
        food = models[order_data['food_type']][1](food_type=food_type,
         user=request.user.username, status='Draft', foodsize=size)
    else:
        food = models[order_data['food_type']][1](food_type=food_type,
         user=request.user.username, status='Draft')
    food.save()

    if 'topping' in order_data:
        toppings = models[order_data['food_type']][2].objects.filter(name__in=order_data.getlist('topping'))
        food.toppings.set(toppings)
        food.save()
    else:
        if order_data['food_type'] == 'Pizzas':
            food.reg_pizza_type = 'Special'
        food.save()


def get_processed_orders():
    """retrieve all 'ordered' orders"""
    checkout_data = {
        'Pizzas': [(i.id, i.user, i) for i in PizzaOrder.objects.filter(~Q(status='Complete'))]
    }
    return checkout_data


def get_basket_contents(request):
    """get basket orders for current user"""
    basket_data = []
    basket_data_o = []
    basket_total = 0

    for i in PizzaOrder.objects.filter(user=request.user.username, status='Draft'):
        basket_data.append([i.id, i.get_price, i])
    
    for i in basket_data:
        basket_total += float(str(i[1]))
        basket_data_o.append([i[0], i[2].__str__()])

    return basket_data_o, basket_total
