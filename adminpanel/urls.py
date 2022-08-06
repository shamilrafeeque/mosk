from django.urls import path
from .import views

urlpatterns = [
    path('',views.adminpanel,name='adminpanel'),
    path('admin_login/',views.admin_login,name="admin_login"),
    
    path('user_details/',views.user_acconnt_table,name="user_details_table"),
    path('banuser/<int:id>/',views.banuser,name="ban_user"),
    path('unbanuser/<int:id>/',views.unban,name="unban_user"),

    path('category_tabel/',views.categorytable,name="categorytable"),
    path('add_category/',views.addcategory,name="add_category"),
    path('editcategory/<int:id>/',views.editcategory,name="edicategory"),
    path('delete/<int:id>/',views.deletecategory,name="deletecategory"),

    path('cart_item/<int:id>/',views.admincartitem,name="cart_items_admin"),
    path('order_table/<int:id>',views.ordertable,name="ordertable"),
    path('cart_table/<int:id>/',views.storetable,name="storetable"),

    path('add_product/',views.add_product,name="add_product"),
    path('editproduct/<int:id>/',views.Editproduct,name="editproduct"),
    path('deleteproduct/<int:id>/',views.productdelete,name="deleteproduct"),

    path('add_variation/',views.add_variation,name="add_variation"),
    path('edit_variation/<int:id>/',views.edit_variation,name="edit_variation"),
    path('variationdelete/<int:id>/',views.variationdelete,name="variationdelete"),

    path('order_accepted/<int:order_id>',views.order_accepted,name="order_accepted"),
    path('order_completed/<int:order_id>',views.order_completed,name="order_completed"),
    path('order_cancelled/<int:order_id>',views.order_cancelled,name="order_cancelled"),

    path('admin_search/',views.admin_search,name="admin_search"),
    path('variation_search/',views.variationsearch,name="variationsearch"),
    path('adminuserdetails/',views.adminuserdetails,name="adminuserdetails"),
    path('ordersearch/',views.ordersearch,name="ordersearch"),
]