from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from . models import *
from home.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


# Create your views here.
def cart_details(request,tot=0,count=0,cart_items=None,ct_items=None):
    try:
        user = request.user #c/n

        if user.is_authenticated:
            ct = cartlist.objects.filter(user=user)


        else:
            cart_id = request.session.get('cart_id')
            ct = cartlist.objects.filter(cart_id=cart_id)

        ct_items = items.objects.filter(cart__in=ct, active=True)
        for i in ct_items:
            tot += (i.prod.price * i.quan)
            count += i.quan

    except ObjectDoesNotExist:
        return HttpResponse("<script> alert('Empty Cart');window.location='/';</script>")

    return render(request,'cart.html',{'ci':ct_items,'t':tot,'cn':count})

def c_id(request):
    ct_id=request.session.session_key
    if not ct_id:
        ct_id=request.session.create()
    return ct_id


@login_required(login_url='register')#c/n     # login url for when user is not authenticated.... it redirect to register
def add_cart(request,product_id):
    prod=products.objects.get(id=product_id)
    user = request.user  #c/n

    # if not user.is_authenticated:
    #     return HttpResponse("<script> alert('no ac');window.location='/register';</script>")

    try:
        ct=cartlist.objects.get(cart_id=c_id(request))
    except cartlist.DoesNotExist:
        ct=cartlist.objects.create(cart_id=c_id(request),user=user)  #c/n
        ct.save()

    try:
        c_items=items.objects.get(prod=prod,cart=ct)
        if c_items.quan < c_items.prod.stock:
            c_items.quan+=1
        c_items.save()
    except items.DoesNotExist:
        c_items=items.objects.create(prod=prod,quan=1,cart=ct)
        c_items.save()
    return redirect('cartDetails')

def min_cart(request,product_id):
    ct=cartlist.objects.get(cart_id=c_id(request))
    prod=get_object_or_404(products,id=product_id)
    c_items=items.objects.get(prod=prod,cart=ct)
    if c_items.quan>1:
        c_items.quan-=1
        c_items.save()
    else:
        c_items.delete()
    return redirect('cartDetails')

def cart_delete(request,product_id):
    ct=cartlist.objects.get(cart_id=c_id(request))
    prod=get_object_or_404(products,id=product_id)
    try:
        c_items = items.objects.get(prod=prod, cart=ct)
        c_items.delete()
    except items.DoesNotExist:
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

def payment(request):
    if request.method == 'POST':
        # Retrieve the form data from the POST request
        account_number = request.POST.get('account-number')
        name = request.POST.get('name')
        expiry_month = request.POST.get('expiry-month')
        expiry_year = request.POST.get('expiry-year')
        cvv = request.POST.get('cvv')

        # Perform validation and additional actions if needed

        # Save the form data to the database or perform other actions
        # You can create a model object and save it to the database here

        # Return a success response or redirect to a success page
        return render(request, 'checkout_success.html')

    return render(request, 'checkout.html')
