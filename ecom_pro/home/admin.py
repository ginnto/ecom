from django.contrib import admin
from . models import *
from django.contrib import messages
# Register your models here.


class catadmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields ={'slug':('name',)}
admin.site.register(categ,catadmin)

class product(admin.ModelAdmin):
    list_display = ['name','slug','price','stock','img','available']
    list_editable = ['price','stock','img','available']
    prepopulated_fields ={'slug':('name',)}


    def save_model(self, request, obj, form, change):
        if obj.stock <= 1:
            messages.error(request, "Out of stock: ou of stock.add products.")
        obj.save()




admin.site.register(products,product)



