from django.shortcuts import render,HttpResponse,redirect
from .forms import SignUpForm,UserLoginForm
from django.http import JsonResponse,HttpResponseBadRequest
from django.contrib.auth import login,authenticate,logout
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from .models import UserAccount,MenuItem,Cart,OrderPlace
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.db.models import Q
import threading

class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()
        
def MainPage(request):
    return render(request,'myRestaurant/index.html')

def Register(request):
    message = ''
    data = {}
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Successfull'
            
        data = {
            'message': message,
            'registererror': form.errors
        }
        print(message)
        print(form.errors)
    return JsonResponse(data,safe=False)


def login_view(request):
    message = ''
    data = {}
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = request.POST['email']
        password = request.POST['password']
        query = UserAccount.objects.get(email__iexact = email)
            
        user = authenticate(request,email=email, password=password)
        if user:
            login(request, user)
            message = 'loginSucessfully'
        else:
            if query.is_active == False:
                
                current_site = get_current_site(request)
                email_subject = 'Active your Account'
                message = render_to_string('Auth/activate.html',
                    {
                        'user': query,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(query.pk)),
                        'token': generate_token.make_token(query)
                    })
                email_message = EmailMessage(email_subject,message,
                        settings.EMAIL_HOST_USER,[email]
                        )
                EmailThread(email_message).start()
                form.add_error('email',"Please Verify Your Account, link send to your email")
            else:
                form.add_error('password',"Incorrect password. Please try again!")
    data = {
        'formerror' : form.errors,
        'message' : message
    }
    print(form.errors)
    return JsonResponse(data,safe=False)

def ActivateAccountView(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserAccount.objects.get(pk=uid)
    except Exception as identifier:
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('<h1>Your Account Active Successfull.......Thank you</h1>')
    
@login_required
def logout_view(request):
    logout(request)
    return redirect("/")

def add_to_cart(request):
    if request.user.is_authenticated:
        message = ''
        user = request.user
        item_id = request.GET['Item_id']
        item = MenuItem.objects.get(id = item_id)
        cart_items = Cart.objects.filter(Q(user_cart = user) & Q(item = item)).first()
        print(item_id)
        if cart_items:
            print(cart_items)
            cart_items.quantity = cart_items.quantity + 1
            cart_items.save()
            
            message = 'update'
        else:
            quantity = 1
            add_cart = Cart(user_cart = user, item = item, quantity = quantity)
            add_cart.save()
            message = 'add'
                
        data = {
            'message': message,
            }
        return JsonResponse(data,safe=False)
    else:
        return HttpResponseBadRequest("Login Required...!")
        

def remove_to_cart(request,id):
    cart_item = Cart.objects.filter(Q(user_cart = request.user) & Q(id = id))
    cart_item.delete()
    remng_item = Cart.objects.filter(user_cart = request.user)
    total_price = get_total_price(remng_item)
    
    cart=render_to_string('myRestaurant/Cart.html',{'cart_item': remng_item,'total_price': total_price})
    return JsonResponse({'cart': cart})

def get_cart_item(request):
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user_cart = request.user)
        total_price = get_total_price(cart_item)
        
        cart=render_to_string('myRestaurant/Cart.html',{'cart_item': cart_item, 'total_price': total_price})
        return JsonResponse({'cart': cart})
    else:
        return HttpResponseBadRequest("Login Required...!")

def get_total_price(cart_item):
    total_price_list = [cart.item.price * cart.quantity for cart in cart_item]
    total_price = 0
    for price in total_price_list:
        total_price = total_price + price
        
    return total_price

def update_quantity(request):
    
    pm_data = request.GET['PM']
    citem_id = request.GET["cItem_id"]
    quantity = 1
    cart = Cart.objects.get(id = citem_id)
    if pm_data == 'plus':
        cart.quantity = cart.quantity + 1
        cart.save()
        quantity = cart.quantity
    if pm_data == 'minus':
        if cart.quantity > 1:
            cart.quantity = cart.quantity - 1
            cart.save()
            quantity = cart.quantity
        else:
            cart.quantity = cart.quantity
            quantity = cart.quantity
    data = {
        'quantity': quantity,
        'total_price': get_total_price(Cart.objects.filter(user_cart = request.user))  
    }
    return JsonResponse(data, safe = True)

@csrf_exempt
def Order_place(request):
    if request.method == 'GET':
        cart_item = Cart.objects.filter(user_cart = request.user)
        total_price = get_total_price(cart_item)
        order_form=render_to_string('myRestaurant/OrderPlace.html',{'total_price': total_price}) 
        data ={
            'Order_Form': order_form
        }
        return JsonResponse(data, safe = True)
    
    if request.method == 'POST':
        user = request.user
        name = request.POST['name']
        addr = request.POST['address']
        phone = request.POST['phone']
        pay_method = request.POST['payment']
        
        if pay_method == 'Cash on Delivery':
            cart = Cart.objects.filter(user_cart = user)
            
            for c in cart:
                OrderPlace(order_user = user, address = addr,name =name,phone=phone,
                        order_item = c.item, quantity = c.quantity, is_paid = False,
                        amount = c.item.price * c.quantity,).save()
                c.delete()
                
            data ={
                'message': "Order Placed Successfull"
            }
        return JsonResponse(data, safe = True)
    
def OrderView(request):
    orders = OrderPlace.objects.filter(order_user = request.user)
    my_order = render_to_string('myRestaurant/OrderDetails.html',{'orders': orders})
    
    return JsonResponse({'my_order': my_order,}, safe = True)

# from django.core import serializers
# def OrderView(request):
#     orders = OrderPlace.objects.filter(order_user = request.user)
#     my_order = render_to_string('myRestaurant/OrderDetails.html',{'orders': orders})
#     # data = serializers.serialize("json", orders.values('order_id'))
#     data = serializers.serialize("json", orders)

#     return JsonResponse({'my_order': my_order,'orders': data}, safe = True)
  
    