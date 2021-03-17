from django import forms
from .models import Customer,Order,Product,Workflow,Address,OrderProducts


class CustomerForm(forms.ModelForm):
    
    class Meta:

        model = Customer
        fields = ['customer_name','telephone','email']

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        #stok = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('1', 'Var'), ('0', 'Yok')])
        fields = ['customer','content','order_image','order_type','stok' ]

class OrderProductsForm(forms.ModelForm):
    class Meta:
        model = OrderProducts
        fields = ['order','product','amount','colour']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','title','montaj_sabiti','marka','product_type','unit']


class AddressForm(forms.ModelForm):
    class  Meta:
        model = Address
        fields = ['customer','ulke','il','ilce','adres','map_link']

