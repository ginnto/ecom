from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from . models import *
from home.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.

def c_id(request):
    ct_id=request.session.session_key #if session key is exist
    if not ct_id:
        ct_id=request.session.create() #there is no session key then create new one
    return ct_id


# @login_required(login_url='register')
# def add_cart(request, product_id):
#     prod = products.objects.get(id=product_id)
#     user = request.user
#
#     try:
#         cart = cartlist.objects.get(user=user)
#     except cartlist.DoesNotExist:
#         cart = cartlist.objects.create(cart_id=c_id(request), user=user)
#         cart.save()
#
#     try:
#         cart_item = items.objects.get(prod=prod, cart=cart)
#         if cart_item.quan < prod.stock:
#             cart_item.quan += 1
#         cart_item.save()
#     except items.DoesNotExist:
#         cart_item = items.objects.create(prod=prod, quan=1, cart=cart)
#         cart_item.save()
#
#     return redirect('cartDetails')



@login_required(login_url='login')     #c/n     # login url for when user is not authenticated.... it redirect to register
def add_cart(request,product_id):
    prod=products.objects.get(id=product_id)
    user = request.user  #c/n

    try:
        ct=cartlist.objects.get(user=user)    #already existing
    except cartlist.DoesNotExist:                                 #cartlist
        ct=cartlist.objects.create(cart_id=c_id(request),user=user)    #new user          #c/n
        ct.save()

    try:
        c_items=items.objects.get(prod=prod,cart=ct)      #same product existing
        if c_items.quan < c_items.prod.stock:
            c_items.quan +=1  #quan= quan + 1
            prod.stock -=1
            prod.save()

        c_items.save()                                           #items
    except items.DoesNotExist:
        c_items=items.objects.create(prod=prod,quan=1,cart=ct)
        prod.stock -= 1
        prod.save()
        c_items.save()
    return redirect('cartDetails')

def cart_details(request,tot=0,count=0,cart_items=None,ct_items=None):

    try:
        user = request.user #c/n

        if user.is_authenticated:
            ct = cartlist.objects.filter(user=user)

        else:
            cart_id = request.session.get('cart_id')
            ct = cartlist.objects.filter(cart_id=cart_id)
# -------------------------------------------------------------------
        ct_items = items.objects.filter(cart__in=ct, active=True)
        for i in ct_items:
            tot += (i.prod.price * i.quan)
            count += i.quan

    except ObjectDoesNotExist:
        return HttpResponse("<script> alert('Empty Cart');window.location='/';</script>")

    return render(request,'cart.html',{'ci':ct_items,'t':tot,'cn':count})

@login_required(login_url='register')  #changed
def min_cart(request,product_id):
    user = request.user
    try:
        if user.is_authenticated:
            ct_list = cartlist.objects.filter(user=user)
        else:
            cart_id = request.session.get('cart_id')
            ct_list = cartlist.objects.filter(cart_id=cart_id)
    # ct=cartlist.objects.get(user=user,cart_id=c_id(request))
        if ct_list.exists:
            for ct in ct_list:
                prod=get_object_or_404(products,id=product_id)
                try:
                    c_items=items.objects.get(prod=prod,cart=ct)
                    if c_items.quan>1:
                        c_items.quan-=1
                        c_items.save()
                    else:
                        c_items.delete()
                except items.DoesNotExist:
                    pass
    except cartlist.DoesNotExist:
        pass
    return redirect('cartDetails')

@login_required(login_url='register')  #changed
def cart_delete(request, product_id):
    user = request.user
    try:
        if user.is_authenticated:
            ct_list = cartlist.objects.filter(user=user)
        else:
            cart_id = request.session.get('cart_id')
            ct_list = cartlist.objects.filter(cart_id=cart_id)

        if ct_list.exists():
            for ct in ct_list:
                prod = get_object_or_404(products, id=product_id)
                try:
                    c_items = items.objects.get(prod=prod, cart=ct)
                    c_items.delete()
                except items.DoesNotExist:
                    pass

    except cartlist.DoesNotExist:
        pass

    return redirect('cartDetails')


def checkout(request):
    if request.method == 'POST':
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        country = request.POST['county']
        address = request.POST['address']
        towncity = request.POST['city']
        postcodezip = request.POST['pin']
        phone = request.POST['phone']
        email = request.POST['email']
        cart = cartlist.objects.filter(user=request.user).first()

        checkout = Checkout(
            user=request.user,
            cart=cart,
            firstname=firstname,
            lastname=lastname,
            country=country,
            address=address,
            towncity=towncity,
            postcodezip=postcodezip,
            phone=phone,
            email=email
        )
        checkout.save()
        return redirect('payment')

    return render(request, 'checkout.html')

def payments(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        name = request.POST.get('name')
        expiry_month = request.POST.get('expiry_month')
        expiry_year = request.POST.get('expiry_year')
        cvv = request.POST.get('cvv')

        pay = payment(
            user=request.user,
            account_number=account_number,
            name=name,
            expiry_month=expiry_month,
            expiry_year=expiry_year,
            cvv=cvv
        )
        pay.save()

        user = request.user
        ct = cartlist.objects.get(user=user, cart_id=c_id(request))
        items.objects.filter(cart=ct).delete()
        return redirect('success')

    return render(request, 'bank.html')

def success(request):
    return render(request,'successful.html')