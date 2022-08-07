from django import forms
from category.models import Category
from store.models import Product
from store.models import Variation

class CategoryForm(forms.ModelForm):
    class Meta:
        model  = Category
        fields = ['category_name','description']

    def __init__(self,*args,**kwargs):
        super(CategoryForm,self).__init__(*args,**kwargs)

        # self.fields['main_category'].widget.attrs['class']='form-control form-control-user'

        self.fields['category_name'].widget.attrs['placeholder']='Enter Category name'
        self.fields['category_name'].widget.attrs['class']='form-control form-control-user'
        self.fields['category_name'].widget.attrs['type']='text'

        self.fields['description'].widget.attrs['placeholder']='Enter Category discription'
        self.fields['description'].widget.attrs['class']='form-control form-control-user'
        self.fields['description'].widget.attrs['type']='text'
        self.fields['description'].widget.attrs['row']=3

# class ProductForm(forms.ModelForm):
#     images = forms.ImageField(required=False, error_messages = {'invalid':("image files only")}, widget=forms.FileInput)
#     class Meta:
#         model = Product
#         fields = ['product_name','slug', 'description','price', 'discount_percent', 'images', 'stock', 'is_available', 'category',]

class ProductForm(forms.ModelForm):
    images = forms.ImageField(required=False, error_messages = {'invalid':("image files only")}, widget=forms.FileInput)
    class Meta:
        model = Product
        fields = ['product_name','description','price','images','is_available','stock','category']

    def __init__(self,*args,**kwargs):
        super(ProductForm,self).__init__(*args,**kwargs)

        self.fields['product_name'].widget.attrs['placeholder']='Enter Product name'
        self.fields['product_name'].widget.attrs['class']='form-control form-control-user'
        self.fields['product_name'].widget.attrs['type']='text'

        self.fields['description'].widget.attrs['placeholder']='Enter Product discription'
        self.fields['description'].widget.attrs['class']='form-control form-control-user'
        self.fields['description'].widget.attrs['type']='text'
        self.fields['description'].widget.attrs['row']=3

        self.fields['price'].widget.attrs['placeholder']='Enter Product Price'
        self.fields['price'].widget.attrs['class']='form-control form-control-user'
        self.fields['price'].widget.attrs['type']='text'

        self.fields['stock'].widget.attrs['placeholder']='Enter Product Stock'
        self.fields['stock'].widget.attrs['class']='form-control form-control-user'
        self.fields['stock'].widget.attrs['type']='text'

class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ['product', 'variation_category', 'variation_value', 'is_active', ]     

    def _init_(self, *args, **kwargs):
        super(VariationForm, self)._init_(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model=ProductGallery
#         fields=['product','iamge']

#     def _init_(self, *args, **kwargs):
#         super(ProductForm, self)._init_(*args, **kwargs)
#         for field in self.fields:
#             self.fields['fiel'].widget.attr['class']='form-control'