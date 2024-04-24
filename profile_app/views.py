from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views import View
from .models import Profile, Product, Cart, CartItem, Order, OrderItem
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt
from .utils import render_to_pdf



# class HomeView(View):
#     def get(self, request):
#         return render(request,'home.html')
def HomeView(request):
    return render(request,'home.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        else:
            print(form.errors)

    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home-page')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



def user_logout(request):
    logout(request)
    return redirect('login')


# class UserProfile(View):
#     template_name = 'profile.html'
#
#     def get(self, request):
#         try:
#             user_profile = Profile.objects.get(user=request.user)
#         except Profile.DoesNotExist:
#             user_profile = None
#         form_data = {
#             'name': user_profile.full_name if user_profile else '',
#             'email': request.user.email if user_profile else '',
#             'designation': user_profile.designation if user_profile else '',
#             'mobile_no': user_profile.mobile_number if user_profile else '',
#             'profile_image': user_profile.profile_image if user_profile else '',
#             'profile_summary': user_profile.profile_summary if user_profile else '',
#             'city': user_profile.city if user_profile else '',
#             'state': user_profile.state if user_profile else '',
#             'country': user_profile.country if user_profile else '',
#         }
#         context = {
#             'profile': user_profile,
#             'form_data': form_data
#         }
#         return render(request, self.template_name, context)
#
#     def post(self, request):
#         try:
#             user_profile = Profile.objects.get(user=request.user)
#         except Profile.DoesNotExist:
#             user_profile = None
#         uploaded_image = request.FILES.get('profile_image', None)
#         if uploaded_image:
#             user_profile.profile_image.save(uploaded_image.name, ContentFile(uploaded_image.read()))
#         full_name = request.POST.get('name')
#         email = request.POST.get('email')
#         designation = request.POST.get('designation')
#         mobile_number = request.POST.get('mobile_no')
#         profile_summary = request.POST.get('profile_summary')
#         city = request.POST.get('city')
#         state = request.POST.get('state')
#         country = request.POST.get('country')
#
#         if user_profile:
#             user_profile.full_name = full_name
#             user_profile.designation = designation
#             user_profile.mobile_number = mobile_number
#             user_profile.profile_summary = profile_summary
#             user_profile.city = city
#             user_profile.state = state
#             user_profile.country = country
#             user_profile.save()
#
#             user_profile.user.email = email
#             user_profile.user.save()
#
#         return redirect('user-profile')


def UserProfile(request):
    template_name = 'profile.html'
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        uploaded_image = request.FILES.get('profile_image', None)
        if uploaded_image:
            user_profile.profile_image.save(uploaded_image.name, ContentFile(uploaded_image.read()))

        full_name = request.POST.get('name')
        email = request.POST.get('email')
        designation = request.POST.get('designation')
        mobile_number = request.POST.get('mobile_no')
        profile_summary = request.POST.get('profile_summary')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')

        if user_profile:
            user_profile.full_name = full_name
            user_profile.designation = designation
            user_profile.mobile_number = mobile_number
            user_profile.profile_summary = profile_summary
            user_profile.city = city
            user_profile.state = state
            user_profile.country = country
            user_profile.save()

            user_profile.user.email = email
            user_profile.user.save()

        return redirect('user-profile')

    form_data = {
        'name': user_profile.full_name if user_profile else '',
        'email': request.user.email if user_profile else '',
        'designation': user_profile.designation if user_profile else '',
        'mobile_no': user_profile.mobile_number if user_profile else '',
        'profile_image': user_profile.profile_image if user_profile else '',
        'profile_summary': user_profile.profile_summary if user_profile else '',
        'city': user_profile.city if user_profile else '',
        'state': user_profile.state if user_profile else '',
        'country': user_profile.country if user_profile else '',
    }
    context = {
        'profile': user_profile,
        'form_data': form_data
    }
    return render(request, 'profile.html', context)


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})



@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('product-list')


@login_required(login_url='login')
def remove_from_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = Cart.objects.get(user=request.user)
    try:
        cart_item = cart.cartitem_set.get(product=product)
        if cart_item.quantity >= 1:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')



@login_required(login_url='login')
def view_cart(request):
    cart = request.user.cart
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart.html', {'cart_items': cart_items})



@login_required(login_url='login')
def increase_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.user.cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')

@login_required(login_url='login')
def decrease_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.user.cart
    cart_item = cart.cartitem_set.get(product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')



@login_required(login_url='login')
def fetch_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = request.user.cart
        cart_count = CartItem.objects.filter(cart=cart).count()
    return JsonResponse({'cart_count': cart_count})


def get_cart_count(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart=request.user.cart)
        cart_count = cart_items.count()
    else:
        cart_count = 0
    return cart_count


@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        user = request.user
        cart = user.cart

        cart_items = CartItem.objects.filter(cart=cart)
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        try:
            order = Order.objects.create(user=user, total_amount=total_amount)
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    item_total=cart_item.product.price * cart_item.quantity
                )

            # client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            client = razorpay.Client(auth=("rzp_test_njtNlo9VjNXAdB", "NWtejV83o7wYkZBcBrQdfGlm"))
            payment_data = {
                'amount': int(total_amount * 100),
                'currency': 'INR',
                'receipt': f'order_{order.id}',
                'payment_capture': '1'
            }
            orderData = client.order.create(data=payment_data)
            order.payment_id = orderData['id']
            order.save()

            return JsonResponse({'order_id': orderData['id']})

        except Exception as e:
            print(str(e))
            return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)


def checkout(request):
    cart_items = CartItem.objects.filter(cart=request.user.cart)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    cart_count = get_cart_count(request)
    email = request.user.email
    full_name = request.user.profile.full_name

    context = {
        'cart_count': cart_count,
        'cart_items': cart_items,
        'total_amount': total_amount,
        'email':email,
        'full_name': full_name
    }
    return render(request, 'checkout.html', context)


@csrf_exempt
def handle_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        razorpay_order_id = data.get('order_id')
        payment_id = data.get('payment_id')

        try:
            order = Order.objects.get(payment_id=razorpay_order_id)

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment = client.payment.fetch(payment_id)

            if payment['status'] == 'captured':
                order.payment_status = True
                order.save()
                user = request.user
                user.cart.cartitem_set.all().delete()
                # return redirect('download-receipt', order_id=order.id)
                return JsonResponse({'message': 'Payment successful'})
            else:
                return JsonResponse({'message': 'Payment failed'})

        except Order.DoesNotExist:
            return JsonResponse({'message': 'Invalid Order ID'})
        except Exception as e:

            print(str(e))
            return JsonResponse({'message': 'Server error, please try again later.'})


# def generate_receipt_pdf(request, order_id):
#     order = Order.objects.get(id=order_id)
#     context = {'order': order}
#     pdf = render_to_pdf('receipt_template.html', context)
#     if pdf:
#         response = HttpResponse(pdf, content_type='application/pdf')
#         filename = f'receipt_{order_id}.pdf'
#         content = f'attachment; filename="{filename}"'
#         response['Content-Disposition'] = content
#         return response
#     return HttpResponse("Failed to generate PDF", status=404)