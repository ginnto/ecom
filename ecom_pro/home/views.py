from django.core.paginator import Paginator,EmptyPage,InvalidPage

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from . models import *
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def home(request,c_slug=None):
    if c_slug  != None:
        c_page=get_object_or_404(categ,slug=c_slug) # c_page=men
        prodt=products.objects.filter(category=c_page,available=True) #select * from product where category=men,available=true;
    else:
        prodt=products.objects.all().filter(available=True)




    cat=categ.objects.all()

#-------------------------------page------------------
    p=Paginator(prodt,5)     #6 represent how many items u want to display in home #para-objlist,item for each page

    pageNum=int(request.GET.get('page',1))  #fetch page num from url(href-page)

    print(pageNum)

    # proe = p.page(pageNum)
    # print(proe)

    try:
        proe = p.page(pageNum)               #
        print(proe)
    except(EmptyPage, InvalidPage):
        proe = p.page(p.num_pages)
        print('hlo',proe)
#--------------------------------------------page end----------------------------


    return render(request,'index.html',{'pro':prodt,'ct':cat,'pr':proe})



def detail(request,c_slug,product_slug):

    prodt=products.objects.get(category__slug=c_slug,slug=product_slug)

    return render(request,'product-single.html',{'pr':prodt})











def searching(request):
    if 'q' in request.GET:
        print('hai')
        query=request.GET.get('q')
        prod=products.objects.all().filter(Q(name__icontains=query)|Q(desc__icontains=query),available=True)
    if not prod:
        return HttpResponse("<script> alert('not available');window.location='/';</script>")

    return render(request,'search.html',{'pr':prod})



def contact(request):
    return render(request,'contact.html')
















    # if not prod:
    #     # return HttpResponse("<script> alert('not available');window.location='/';</script>")