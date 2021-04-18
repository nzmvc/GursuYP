from django import forms
from .models import Customer,Order,Product,Workflow,Address,OrderProducts,Problems


class CustomerForm(forms.ModelForm):
    
    class Meta:

        model = Customer
        fields = ['customer_name','telephone','email','customer_type','vergi_no','vergi_dairesi']

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        #stok = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('1', 'Var'), ('0', 'Yok')])
        fields = ['customer','content','order_image','order_type','stok','iskonto','tahmini_tarih_min','tahmini_tarih_max','satis_kanali' ]
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['tahmini_tarih_min'].widget.attrs['class'] = 'datepicker'
        self.fields['content'].widget.attrs['class'] = 'content_css'
        self.fields['content'].widget.attrs['rows'] = 5

class OrderProductsForm(forms.ModelForm):
    class Meta:
        model = OrderProducts
        #fields = ['order','product','amount','colour']
        fields = ['product','amount','colour']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','product_category','title','montaj_sabiti','marka','product_type','unit','birim_fiyat']


class AddressForm(forms.ModelForm):
    class  Meta:
        model = Address
        fields = ['ulke','il','ilce','adres','map_link','aciklama']

class CustomerAddressForm(forms.ModelForm):
    class  Meta:
        model = Address
        fields = ['customer','ulke','il','ilce','adres','map_link','aciklama']

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problems
        fields = ['order','description','statu','created_user',]

class ProblemSolutionForm(forms.ModelForm):
    class Meta:
        model = Problems
        fields = ['solution','root_cause']