from django.shortcuts import render,redirect
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from rapidfuzz import fuzz
from django import template
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.humanize.templatetags.humanize import intcomma

@property
def cart_total_vnd(self):
    return intcomma(int(self.get_cart_total)).replace(',', '.')

register = template.Library()


@register.filter
def vnd(value):
    try:
        return f"{int(value):,}".replace(",", ".")
    except:
        return value
def detail(request, id):
    order = get_order(request)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

    product = Product.objects.get(id=id)

    context = {
        'product': product,
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'app/detail.html', context)

def search_suggestions(request):
    q = request.GET.get("q", "")
    products = Product.objects.filter(name__icontains=q)[:8]

    data = [
        {
            "id": p.id,
            "name": p.name,
            "image": p.image.url if p.image else "",
        }
        for p in products
    ]
    return JsonResponse(data, safe=False)

def search_fuzzy(request):
    query = request.GET.get('q')
    products = Product.objects.all()
    results = []

    if query:
        for p in products:
            score = fuzz.partial_ratio(query.lower(), p.name.lower())
            if score > 70:  
                results.append(p)

    return render(request, 'search.html', {'products': results})
def category(request):
    order = get_order(request)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
    active_category = request.GET.get('category','')
    if active_category:
        category = Category.objects.get(slug=active_category)
        sub_categories = category.sub_categories.all()
        products = Product.objects.filter(
            Q(category=category) | Q(category__in=sub_categories)
        )
    context = {'products': products,
               'items': items,
                'order': order,
                'cartItems': cartItems,
                'active_category':active_category
                }
    return render(request,'app/category.html',context)
def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_items' :0,'get_cart_total': 0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    return render(request,'app/search.html',{"searched":searched,"keys":keys,'products': products,'cartItems':cartItems})
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form':form}
    return render(request,'app/register.html',context)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username =username,password =password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else: messages.info(request,'user or password not correct!')
    context = {}
    return render(request,'app/login.html',context)
def logoutPage(request):
    logout(request)
    return redirect('login')
def home(request):
    order = get_order(request)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

    products = Product.objects.all()


    context = {
        
        'products': products,
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'app/home.html', context)

def cart(request):
    order = get_order(request)

    if not request.user.is_authenticated:
        sync_cookie_cart_to_order(request, order)

    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

    response = render(request, 'app/cart.html', {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    })

    if not request.user.is_authenticated:
        response.delete_cookie('cart')

    return response

def checkout(request):
    order = get_order(request)

    if not request.user.is_authenticated:
        sync_cookie_cart_to_order(request, order)

    if request.method == "POST" and "selected_items" in request.POST:
        selected_ids = json.loads(request.POST.get("selected_items"))
        items = order.orderitem_set.filter(id__in=selected_ids)

        # LƯU TẠM vào session cho bước submit form sau
        request.session["checkout_items"] = selected_ids
    else:
        selected_ids = request.session.get("checkout_items", [])
        items = order.orderitem_set.filter(id__in=selected_ids)

    context = {
        "items": items,
        "order": order,
        "cartItems": items.count(),
    }
    return render(request, "app/checkout.html", context)


def get_order(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(
            customer=request.user,
            complete=False
        )
    else:
        # 🔥 BẮT BUỘC tạo session nếu chưa có
        if not request.session.session_key:
            request.session.create()

        order, created = Order.objects.get_or_create(
            session_key=request.session.session_key,
            complete=False
        )
    return order
def sync_cookie_cart_to_order(request, order):
    try:
        cart = json.loads(request.COOKIES.get('cart', '{}'))
    except:
        cart = {}

    for product_id, item in cart.items():
        product = Product.objects.get(id=product_id)
        orderItem, created = OrderItem.objects.get_or_create(
            order=order,
            product=product
        )
        orderItem.quantity = item['quantity']
        orderItem.save()
@require_POST
def updateItem(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    productId = data.get('productId')
    action = data.get('action')

    if not productId or not action:
        return JsonResponse({'error': 'Missing productId or action'}, status=400)

    product = get_object_or_404(Product, id=productId)
    order = get_order(request)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order,
        product=product
    )

    if action == 'add':
        orderItem.quantity += 1
        orderItem.save()

    elif action == 'remove':
        orderItem.quantity -= 1
        if orderItem.quantity <= 0:
            orderItem.delete()
        else:
            orderItem.save()

    elif action == 'delete':   
        orderItem.delete()

    else:
        return JsonResponse({'error': 'Invalid action'}, status=400)

    return JsonResponse({
        'status': 'ok',
        'cartItems': order.get_cart_items})