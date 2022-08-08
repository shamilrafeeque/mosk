
# from email import message
# from django.http import HttpRequest
from django.shortcuts import get_object_or_404,redirect, render
from orders.models import OrderProduct
from orders.models import Order



from .models import Account
from django.contrib import messages,auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm,UserProfileForm,UserForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from store.models import Product
from carts.views import _cart_id
from carts.models import Cart,CartItem
from .models import UserProfile
from .forms import UserProfileForm,UserForm
# Create your views here.

def index(request):
    products=Product.objects.all().filter(is_available=True)

    context={
        'product':products,
    }
    return render(request,'accounts/index.html',context)


def user_registeration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            
            user = Account.objects.create_user(first_name=first_name,last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            #user activation
            current_site=get_current_site(request)
            mail_subject='please activate your account'
            message=render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'doamin':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'thank you for register with us...verify your email address')
            return redirect("login")

    else:     
         form = RegistrationForm()
    context ={
        'form':form,
    }
    return render(request,'accounts/signup.html',context)  

def user_login(request):
    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['password']
        #print(email,password)
        user=auth.authenticate(request,email=email,password=password)
        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item=CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user=user
                        item.save()
            except:
                pass
            auth.login(request,user)
            return redirect('index')
        else:
            messages.error(request,'invalid login credentials.')    
            return redirect('login')
    return render(request,'accounts/login.html')

     
def user_logout(request):
    logout(request)
    messages.success(request, 'you are logged out.')
    return redirect("login")

def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congratilations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')
    

#cart function
#def cart(request):
    #return render(request,'accounts\cart.html')
@login_required(login_url='login')
def profile(request):
    # userprofile = get_object_or_404(UserProfile, user=request.user)
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    UserProfile.objects.get_or_create(user=request.user)
   
    userprofile = UserProfile.objects.get(user_id=request.user.id)

    context = {
        'orders_count':orders_count,
        'userprofile' : userprofile,
    }
    return render(request,'accounts/dashboard/profile.html',context)


def my_orders(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context={
        'orders':orders,
    }
    return render(request,'accounts/dashboard/my_orders.html',context)
@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'userprofile' : userprofile,
    }
    return render(request,'accounts/dashboard/edit_profile.html',context)


def change_password(request):
    if request.method=="POST":
        current_password=request.POST['current_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']

        user=Account.objects.get(username__exact=request.user.username)

        if new_password==confirm_password:
            success=user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                #auth logout(request)
                messages.success(request,"Password update successfully")
                return redirect('change_password')
            else:
                messages.error(request,"please enter valid current password")
                return redirect('change_password')
        else:
            messages.error(request,"password does not match!")
            return redirect('change_password')

    return render(request,'accounts/dashboard/change_password.html')


def order_details(request,order_id):
    order_detail=OrderProduct.objects.filter(order__order_number=order_id)
    order=Order.objects.get(order_number=order_id)
    subtotal=0
    for i in order_detail:
        subtotal+=i.product_price*i.quantity
    context={
        'order_detail':order_detail,
        'order':order,
        'subtotal':subtotal,
    }
    return render(request,'accounts/dashboard/order_details.html',context)

def forgotPassword(request):
    if request.method=="POST":
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)
            # reset password
            current_site=get_current_site(request)
            mail_subject='Reset your password'
            message=render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'doamin':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request,'password reset has been sent to your email address')
            return redirect('login')

        else:
            messages.error(request,'Account does not exists')
            return redirect('forgotPassword')
    return render(request,'accounts/forgotPassword.html')

def resetpassword_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request,'this link has been expires')
        return redirect('login')

def resetPassword(request):
    if request.method=="POST":
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password==confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,"password reset is succeessful")
            return redirect('login')

        else:
            messages.error(request,'password do not match')
            return redirect('resetPassword')
    else:
        return render(request,'accounts/resetPassword.html')