# from multiprocessing import context
from unicodedata import category
from django.contrib import messages
from django.shortcuts import redirect, render
from accounts.models import Account
from carts.models import Cart,CartItem
from category.models import Category
from orders.models import Order,OrderProduct,Payment
from store.models import Product,Variation,ProductGallery
from .forms import CategoryForm,ProductForm,VariationForm
from django.template.defaultfilters import slugify
from django.db.models.functions import TruncMinute
import datetime
from django.db.models import Sum
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url="admin_login")
def adminpanel(request):
    if request.user.is_superadmin:
        try:
            total_revenue = round( Order.objects.filter(is_ordered = True).aggregate(sum = Sum('order_total'))['sum'])
        except:
            total_revenue = 0

        total_cost= round((total_revenue * .80))
        total_profit = round(total_revenue - total_cost)  
        chart_year = datetime.date.today().year
        chart_month = datetime.date.today().month

        #getting daily revenue
        daily_revenue = Order.objects.filter(                     
            created_at__year=chart_year,created_at__month=chart_month
        ).order_by('created_at').annotate(day=TruncMinute('created_at')).values('day').annotate(sum=Sum('order_total')).values('day','sum')

        day=[]
        revenue=[]
        for i in daily_revenue:
            day.append(i['day'].minute)
            revenue.append(int(i['sum']))

        # male = Category.objects.get(category_name = 'shoes')
        # female =Category.objects.get(category_name = 'watches')
        # sandals =Category.objects.get(category_name = 'sandals')

        product_count = OrderProduct.objects.all().count()


        context = {
            'total_revenue' : total_revenue,
            'total_cost' : total_cost,
            'total_profit' : total_profit,
            # 'male' : male,
            # 'female' : female,
            # 'sandlers' : sandals,

            'product_count' : product_count,
            'day' : day,
            'revenue' : revenue,
        }
        return render(request,'adminpanel/adminpanel.html',context)
    else:
        return redirect('index')
    # return render(requst,'adminpanel/adminpanel.html')

def admin_login(request):
    return render(request,'adminpanel/admin_accounts/admin_login.html')


@login_required(login_url="admin_login")
def user_acconnt_table(request):
    if request.user.is_superadmin:
        active_user=Account.objects.all().filter(is_admin=False,is_active=True)
        banned_user=Account.objects.all().filter(is_admin=False,is_active=False)
        context={
            'active_user':active_user,
            'banned_user':banned_user,
        }
        return render(request,'adminpanel/admin_accounts/user_details.html',context)
    else:
        return redirect('index')

def banuser(request,id):
    user=Account.objects.get(id=id)
    user.is_active=False
    user.save()
    return redirect('user_details_table')

def unban(request,id):
    user=Account.objects.get(id=id)
    user.is_active=True
    user.save()
    return redirect('user_details_table')



@login_required(login_url="admin_login")
def admincartitem(request,id):
    if request.user.is_superadmin:
        cart=Cart.objects.all()
        cart_item=CartItem.objects.all().filter(is_active=True)
        context={
            'carts':cart,
            'cart_items':cart_item
        }
        if id==1:
            return render(request,'adminpanel/cart_table/carts.html',context)
        else:
            return render(request,'adminpanel/cart_table/cart_items.html',context)
    else:
        return redirect('admin_login')

@login_required(login_url="admin_login")
def categorytable(request):
    category=Category.objects.all()
    context={
        'category':category,
    }
    return render(request,'adminpanel/category_table/category_table.html',context)


def addcategory(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            category_name = form.cleaned_data['category_name']
            slug = slugify(category_name)
            category.slug = slug
            category.save()
            messages.success(request,'New category added successfully')
            return redirect('categorytable')
    context = {
        'form' : form,
    }
    return render (request,'adminpanel/category_table/add_category.html',context)



def editcategory(request,id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST,request.FILES,instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            slug = slugify(category_name)
            category = form.save()
            category.slug = slug
            category.save()
            messages.success(request,'category editted successfully')
            return redirect('categorytable')
    else:
        form = CategoryForm(instance=category)
    context = {
        'form' : form,
    }
    return render(request,'adminpanel/category_table/add_category.html',context)


def deletecategory(request,id):
    category=Category.objects.get(id=id)
    category.delete()
    return redirect('categorytable')

@login_required(login_url="adminpanel")
def ordertable(request,id):
    if request.user.is_superadmin:
        order=Order.objects.filter(is_ordered=True,status='New')
        accepted_orders = Order.objects.filter(is_ordered=True,status='Accepted')
        completed_orders = Order.objects.filter(is_ordered=True,status="Completed")
        cancelled_orders = Order.objects.filter(is_ordered=True,status="Cancelled")
        Orderproduct=OrderProduct.objects.all()
        payment=Payment.objects.all()
        context={
            'orders':order,
            'order_products':Orderproduct,
            'payments':payment,
            'accepted_orders' : accepted_orders,
            'completed_orders' : completed_orders,
            'cancelled_orders' : cancelled_orders,

        }
        if id==1:
            return render(request,'adminpanel/ordertable/orders.html',context)
        elif id==2:
            return render(request,'adminpanel/ordertable/orderproduct.html',context)
        elif id==3:
                return render(request,'adminpanel/ordertable/accepted_orders.html',context)
        elif id==4:
            return render(request,'adminpanel/ordertable/completed_orders.html',context)
        elif id==5:
            return render(request,'adminpanel/ordertable/cancelled_orders.html',context)
        else:
            return render(request,'adminpanel/ordertable/payment.html',context)
    else:
        return redirect('index')

def order_accepted(request,order_id):
   
        order = Order.objects.get(id=order_id)
        order.status = 'Accepted'
        order.save()
        return redirect('ordertable',id=3)
    # else:
    #     return redirect ('add_product')
def order_completed(request,order_id):
    # if request.user.is_superadmin:
        order=Order.objects.get(id=order_id)
        order.status = 'Completed'
        order.save()
        return redirect('ordertable',id=4)
    # else:
    #     return redirect('home')

#@login_required(login_url="login")
def order_cancelled(request,order_id):
    # if request.user.is_superadmin:
        order=Order.objects.get(id=order_id)
        order.status = 'Cancelled'
        order.save()
        return redirect('ordertable',id=5 )
    # else:
    #     return render(request,'adminpanel/order_table/order_cancelled.html')
@login_required(login_url='adminpanel')
def storetable(request,id):
    if request.user.is_superadmin:
        product=Product.objects.all()
        variation=Variation.objects.all()
        context={
            'products':product,
            'variations':variation,
        }
        if id==1:
            return render(request,'adminpanel/storetable/adminproduct.html',context)
        else:
            return render(request,'adminpanel/storetable/adminvariations.html',context)
    else:
        return redirect('index')



def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        #print(form)
        if form.is_valid():
            product = form.save(commit=False)
            product_name = form.cleaned_data['product_name']
            slug = slugify(product_name)
            product.slug = slug

            product.save()
            try:
                images = request.FILES.getlist('images')
                for image in images:
                        ProductGallery.objects.create(
                            image = image,
                            product = product,
                        )
            except:
                pass
            return redirect('storetable',id=1)
    else:
        form = ProductForm()
    context = {
        'form' : form,
    }
    return render(request,'adminpanel/storetable/add_product.html',context)

def Editproduct(request,id):
    product=Product.objects.get(id=id)
    if request.method=='POST':
        form=ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            product_name=form.cleaned_data['product_name']
            slug=slugify(product_name)
            product=form.save()
            product.slug=slug
            product.save()
            return redirect('storetable',id=1)
    else:
        form=ProductForm(instance=product)
    context={
        'form':form,
    }
    return render(request,'adminpanel/storetable/add_product.html',context)

def productdelete(request,id):
    products = Product.objects.get(id=id)
    products.delete()
    return redirect('storetable',id=1)

def add_variation(request):
    form = VariationForm()
    
    if request.method == 'POST':
        form = VariationForm(request.POST)
        if form.is_valid():
            variation = form.save()
            
            variation.save()
            messages.success(request,'New variation added successfully')
            return redirect('storetable',id=2)
    

    else:
        form = VariationForm()
    context = {
        'form' : form,
    }        
    return render(request,'adminpanel/storetable/add_variation.html',context)


def edit_variation(request,id):
    variation = Variation.objects.get(id=id)
    if request.method == 'POST':
        form = VariationForm(request.POST,request.FILES,instance=variation)
        if form.is_valid():
            
            variation = form.save()
            
            variation.save()
            messages.success(request,'variation editted successfully')
            return redirect('storetable',id=2)
    else:
        form = VariationForm(instance=variation)
    context = {
        'form' : form,
    }
    return render(request,'adminpanel/storetable/add_variation.html',context)


def variationdelete(request,id):
    product=Variation.objects.get(id=id)
    product.delete()
    return redirect('storetable',id=2)


@login_required(login_url='adminpanel')
def admin_search(request):
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
           products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keywords) | Q(product_name__icontains=keywords))
            # orders = Order.objects.order_by('-created_date').filter(
            #     Q(order_number__icontains= keyword) | Q(user__icontains= keyword)
            #     | Q(status__icontains = keyword) 
            # )
        #     main_category = MainCategory.objects.filter()

            
        #     paginator = Paginator(products,9)
        #     page = request.GET.get('page')
        #     paged_proucts = paginator.get_page(page)

        #     product_count = products.count()
        # else:
        #     products = Product.objects.all()
        #     paginator = Paginator(products,9)
        #     page = request.GET.get('page')
        #     paged_proucts = paginator.get_page(page)

        #     product_count = products.count()
        context = {
            # 'products':paged_proucts,
            # 'product_count' : product_count,
            # 'orders' : orders,
            'products':products,

        }
        
        return render(request,'adminpanel/storetable/adminproduct.html',context)
    return redirect('adminpanel')


def variationsearch(request):
    if 'keywordss' in request.GET:
        keywordss=request.GET['keywordss']
    if keywordss:
        variations=Variation.objects.order_by('-creatd_date').filter(Q(variation_category__icontains=keywordss)|Q(variation_value__icontains=keywordss))
    context={
        'variations':variations,
    }
    return render(request,'adminpanel/storetable/adminvariations.html',context)

def adminuserdetails(request):
    if 'keywordss' in request.GET:
        keyword=request.GET['keywordss']
    if keyword:
        user=Account.objects.filter(Q(first_name__icontains=keyword)|Q(last_name__icontains=keyword)|Q(email__icontains=keyword)|Q(phone_number__icontains=keyword)|Q(username__icontains=keyword))
    context={
        'active_user':user,
        'banned_user':user,
    }
    return render(request,'adminpanel/admin_accounts/user_details.html',context)

def ordersearch(request):
    Orderproduct=OrderProduct.objects.all()
    
    if 'keywords' in request.GET:
        keyword=request.GET['keywords']
    if keyword:
        orders=Order.objects.order_by('-created_at').filter(Q(order_number__icontains=keyword)|Q(email__icontains=keyword))
    context={
        'orders':orders,
        'order_products':Orderproduct,
    }
    return render(request,'adminpanel/ordertable/orders.html',context)