from django.urls import path
from . import views

urlpatterns = [
    path('place_order/',views.place_order,name="palce_order"),
    path('payments/',views.payments,name="payments"),
    path('order_complete/',views.ordercomplete,name='order_complete'),
    

]