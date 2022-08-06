from itertools import product
from django.contrib import admin
from .models import Payment,Order,OrderProduct

class OrderProductInline(admin.TabularInline):
    model=OrderProduct
    extra= 0
    readonly_fields=['user','payment','product','quantity','product_price','ordered']

class orderAdmin(admin.ModelAdmin):
    list_display= ['order_number','full_name','phone','email','order_total','status','is_ordered','created_at']
    list_filter=['status','is_ordered']
    search_fields= ['order_number','first_name','last_name','email','phone']
    list_per_page=20
    inlines=[OrderProductInline]

admin.site.register(Payment)
admin.site.register(Order,orderAdmin)
admin.site.register(OrderProduct)
# Register your models here.
