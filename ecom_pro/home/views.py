from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from . models import *
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def home(request,c_slug=None):
    c_page=None
    prodt=None
    if c_slug != None:
        c_page=get_object_or_404(categ,slug=c_slug)
        prodt=products.objects.filter(category=c_page,available=True)
    else:
        prodt=products.objects.all().filter(available=True)
    cat=categ.objects.all()


    # -----------end----------
    paginator=Paginator(prodt,5)      #6 represent how many items u want to display in home
    try:
        page=int(request.GET.get('page',1))
    except:
        page=1

    try:
        proe=paginator.page(page)

    except(EmptyPage,InvalidPage):
        proe=paginator.page(paginator.num_pages)

    return render(request,'index.html',{'pro':prodt,'ct':cat,'pr':proe})




def detail(request,c_slug,product_slug):
    try:
        prodt=products.objects.get(category__slug=c_slug,slug=product_slug)
    except Exception as e:
        raise e
    return render(request,'product-single.html',{'pr':prodt})



def searching(request):
    prod=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        prod=products.objects.all().filter(Q(name__icontains=query)|Q(desc__icontains=query),available=True)
    if not prod:
        return HttpResponse("<script> alert('not available');window.location='/';</script>")


    return render(request,'search.html',{'qr':query,'pr':prod})


