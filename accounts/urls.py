from django.urls import path
from accounts import views
urlpatterns = [
    path('',views.index,name="index"),
    path('login/',views.user_login,name="login"),
    path('register/',views.user_registeration,name="register"),
    path('logout/',views.user_logout,name="logout"),
    path('activate/<uidb64>/<token>/',views.activate,name="activate"),
    path('forgotPassword/',views.forgotPassword,name="forgotPassword"),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name="resetpassword_validate"),
    path('resetPassword/',views.resetPassword,name="resetPassword"),

    #path('cart/',views.cart,name="cart"),
    path('profile/',views.profile,name="profile"),
    path('my_orders/',views.my_orders,name="my_orders"),
    path('edit_profile/',views.edit_profile,name="edit_profile"),
    path('change_password/',views.change_password,name="change_password"),
    path('order_details/<int:order_id>/',views.order_details,name="order_details"),
]
