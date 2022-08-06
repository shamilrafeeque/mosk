from django.db import models
from store.models import Product,Variation
from accounts.models import Account

# Create your models here.

class Wishlist(models.Model):
    wishlist_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.wishlist_id

class WishlistItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist,on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
   
    def _unicode_(self):
        return self.product