from django.shortcuts import render,redirect
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
from .models import *
import os
import re
import google.generativeai as genai
import json
import datetime
from .form import RegisterForm
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from rapidfuzz import process,fuzz
from dotenv import load_dotenv
from django import template
from django.views.decorators.http import require_POST


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print(f"DEBUG: API Key load được là: {api_key}")
if not api_key:
    raise ValueError("Không tìm thấy GEMINI_API_KEY trong .env") 
genai.configure(api_key=api_key)


def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()
            
            
            stop_words = ["tìm", "cho", "tôi", "sách", "về", "muốn", "có", "là"]
            keywords = [word for word in user_message.lower().split() if word not in stop_words]
            
            
            query = Q()
            for word in keywords:
                query |= Q(name__icontains=word) | Q(category__name__icontains=word) | Q(detail__icontains=word)
                
            products = Product.objects.filter(query).distinct()[:5]
            
           
            if products.exists():
                product_context = "Các sản phẩm phù hợp:\n"
                for p in products:
                    
                    url = f"/product/{p.id}/" 
                    product_context += f"- [{p.name}]({url}) | Giá: {p.final_price:,.0f}đ\n"
            else:
                product_context = "Không tìm thấy sách cụ thể."

           
            all_categories = Category.objects.all()
            category_context = "Các danh mục bạn có thể tham khảo:\n"
            for c in all_categories:
                url = f"/category/{c.slug}/"
                category_context += f"- [{c.name}]({url})\n"
           
            model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")
            prompt = f"""
            Bạn là trợ lý tư vấn tại Book Store. 
            Thông tin kho sách hiện có:
            {product_context}
            {category_context}
            Khách hàng hỏi: "{user_message}"
            
            Yêu cầu trả lời:
            - Nếu tìm thấy sách, hãy giới thiệu kèm link định dạng [Tên sách](/product/id/).
            - Nếu khách tìm theo thể loại, hãy giới thiệu link danh mục định dạng [Tên danh mục](/category/slug/).
            - Tuyệt đối không gửi link văn bản thô, hãy dùng định dạng Markdown [Tên](Link).
            """
            
            response = model.generate_content(prompt)
            print(products.query)
            return JsonResponse({"reply": response.text})
        

        except Exception as e:
            import traceback
            traceback.print_exc()  
            return JsonResponse({"reply": f"Lỗi: {str(e)}"}, status=500)
        

custom_filters = template.Library()


@custom_filters.filter
def vnd(value):
    try:
        return f"{int(value):,}".replace(",", ".")
    except:
        return value

def user_orders(request):
    if request.user.is_authenticated:
        
        orders = Order.objects.filter(customer=request.user).order_by('-date_order')
    else:
        
        device = request.session.session_key
        orders = Order.objects.filter(session_key=device).order_by('-date_order')
    
    context = {'orders': orders}
    return render(request, 'app/user_orders.html', context)

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    
    if order.customer == request.user and order.status == 'Pending':
        order.status = 'Cancelled'
        order.save()
        messages.success(request, f'Đã hủy đơn hàng #{order.id} thành công.')
    else:
        messages.error(request, 'Bạn không thể hủy đơn hàng này.')
        
    return redirect('user_orders')

def order_detail(request, order_id):
    
    order = get_object_or_404(Order, id=order_id)
    
    
    if order.customer != request.user:
        return render(request, 'app/404.html') 

   
    items = order.orderitem_set.all()
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'app/order_detail.html', context)
def detail(request, id):
    order = get_order(request)
    product = get_object_or_404(Product, id=id)

    if order:
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        cartItems = 0
        
        order = {'get_cart_total': 0, 'get_cart_items': 0}

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
def category_view(request, category_slug=None):
    order = get_order(request)
    
    if order:
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        cartItems = 0
    
    all_main_categories = Category.objects.filter(sub_category__isnull=True)
    
    if category_slug:
      
        active_category = get_object_or_404(Category, slug=category_slug)
        sub_categories = active_category.sub_categories.all()
        products = Product.objects.filter(
            Q(category=active_category) | Q(category__in=sub_categories)
        )
    else:
      
        active_category = None
        products = Product.objects.all()

    price_filter = request.GET.getlist('price')

    selected_prices = request.GET.get('price')

    if price_filter:

        for price in price_filter:

            if price == "0-150":
                products = products.filter(price__lte=150000)

            elif price == "150-300":
                products = products.filter(price__gte=150000, price__lte=300000)

            elif price == "300-500":
                products = products.filter(price__gte=300000, price__lte=500000)

            elif price == "500-700":
                products = products.filter(price__gte=500000, price__lte=700000)

            elif price == "700+":
                products = products.filter(price__gte=700000)
    
    order = get_order(request)
    if order:
        cartItems = order.get_cart_items
    else:
        cartItems = 0

    context = {
        'products': products,
        'active_category': active_category,
        'all_categories': all_main_categories, 
        'selected_prices': [selected_prices] if selected_prices else [],
        'order': order,
        'cartItems': cartItems
    }
    return render(request, 'app/category.html', context)
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
    if request.method == "POST":
        form = RegisterForm(request.POST) 
        if form.is_valid():
            form.save()
            messages.success(request, "Đăng ký thành công!")
            return redirect('login')
    else:
        form = RegisterForm()
        
    context = {'form': form}
    return render(request, 'app/register.html', context)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

       
        failed_attempts_key = f"failed_attempts_{username}"
        is_locked_key = f"is_locked_{username}"

       
        if cache.get(is_locked_key):
            messages.error(request, 'Tài khoản này đã bị khóa 30 phút do nhập sai quá nhiều!')
            return render(request, 'app/login.html', {})

        user = authenticate(request, username=username, password=password)

        if user is not None:
          
            cache.delete(failed_attempts_key)
            login(request, user)
            return redirect('home')
        else:
          
            attempts = cache.get(failed_attempts_key, 0) + 1
            cache.set(failed_attempts_key, attempts, timeout=1800)

            if attempts >= 3:
              
                cache.set(is_locked_key, True, timeout=1800)
                messages.error(request, 'Bạn đã nhập sai 3 lần. Tài khoản bị khóa 30 phút!')
            else:
                messages.info(request, f'Tên đăng nhập hoặc mật khẩu không đúng! (Lần {attempts}/3)')

    context = {}
    return render(request, 'app/login.html', context)
def logoutPage(request):
    logout(request)
    return redirect('login')
def home(request):
    order = get_order(request)
    
    
    if order and order.pk:
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        
        items = []
        cartItems = 0

    tham_khao_products = Product.objects.filter(category__slug='Stk')
    products = Product.objects.all()

    context = {
        'tham_khao_products': tham_khao_products,
        'products': products,
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'app/home.html', context)

def cart(request):
    order = get_order(request)

    
    if order is None:
        items = []
        cartItems = 0
        
        order = {'get_cart_total': 0, 'get_cart_items': 0} 
    else:
        if not request.user.is_authenticated:
            sync_cookie_cart_to_order(request, order)
        
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    response = render(request, 'app/cart.html', {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    })

    if not request.user.is_authenticated and response:
        response.delete_cookie('cart')

    return response

def checkout(request):
    order = get_order(request)
    if not order:
        return redirect('cart')

    
    if not request.user.is_authenticated:
        sync_cookie_cart_to_order(request, order)

    
    selected_ids = request.session.get("checkout_items", [])
    if selected_ids:
        items = order.orderitem_set.filter(id__in=selected_ids)
    else:
        items = order.orderitem_set.all()

    if not items.exists():
        return redirect('cart')

   
    if request.method == "POST" and "address" in request.POST:
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        city = request.POST.get('city')
        address = request.POST.get('address')

        if name and mobile and city and address:
           
            ShoppingAddress.objects.create(
                customer=request.user if request.user.is_authenticated else None,
                order=order,
                name=name, mobile=mobile, city=city, address=address
            )
            
            
            order.transaction_id = f"{datetime.datetime.now().strftime('%Y%m%d')}-{order.id}"
            order.complete = True
            order.status = 'Pending'
            order.save()
            
            
            if 'checkout_items' in request.session:
                del request.session['checkout_items']
            
            response = redirect('order_success', order_id=order.id)
            response.delete_cookie('cart')
            return response

    context = {"items": items, "order": order, "cartItems": items.count()}
    return render(request, "app/checkout.html", context)

def order_success(request, order_id):
    return render(request, 'app/order_success.html', {'order_id': order_id})


def get_order(request):
    
    if request.user.is_authenticated:
      
        return Order.objects.filter(customer=request.user, complete=False).first()
    
   
    else:
        session_key = request.session.session_key
        if not session_key:
            return None
        
   
        return Order.objects.filter(session_key=session_key, complete=False).first()
def sync_cookie_cart_to_order(request, order):
    if not order:
        return
    cart_json = request.COOKIES.get('cart', '{}')
    try:
        cart = json.loads(cart_json)
    except:
        cart = {}

    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            orderItem, created = OrderItem.objects.get_or_create(
                order=order,
                product=product
            )
            orderItem.quantity = item['quantity']
            orderItem.save()
        except Product.DoesNotExist:
            continue
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

    if request.user.is_authenticated:
   
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
    else:
     
        if not request.session.session_key:
            request.session.create()
        order, created = Order.objects.get_or_create(
            session_key=request.session.session_key, 
            complete=False
        )
  

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

 
    if order.orderitem_set.count() == 0:
       
        pass

    return JsonResponse({
        'status': 'ok',
        'cartItems': order.get_cart_items
    })