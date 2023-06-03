from . models import *
from . views import *
from home.views import *




def cate(request):
    cat=categ.objects.all()
    return {'ct':cat}







# def count(request):
#     tot=0
#     count=0
#     try:
#         cart_id = request.session.get('cart_id')
#         ct = cartlist.objects.filter(cart_id=cart_id).latest('date_added')
#
#         ct_items = items.objects.filter(cart=ct, active=True)
#         for i in ct_items:
#             tot += (i.prod.price * i.quan)
#             count += i.quan
#     except ObjectDoesNotExist:
#         return HttpResponse("<script> alert('Empty Cart');window.location='/';</script>")
#     return {'cn': count}























