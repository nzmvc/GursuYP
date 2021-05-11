from django import forms
from .models import Customer,Order,Product,Workflow,Address,OrderProducts,Problems,ProductCategory,UrunGrubu,Marka
from crispy_forms.layout import Layout, Fieldset,Field
from django.forms import ModelChoiceField

class CustomerForm(forms.ModelForm):
    
    class Meta:

        model = Customer
        fields = ['customer_name','telephone','email','customer_type','vergi_no','vergi_dairesi']

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        #stok = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('1', 'Var'), ('0', 'Yok')])
        fields = ['customer','content','planlama_sekli','order_image','order_type','stok','iskonto','tahmini_tarih_min','tahmini_tarih_max','satis_kanali' ]
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        #self.fields['dosyaVarYok'] = forms.ChoiceField(label='Ölçüm Dosyası',choices=[('VAR','VAR'),('YOK','YOK')], widget=forms.RadioSelect)

        self.fields['tahmini_tarih_min'].widget.attrs['class'] = 'datepicker'
        self.fields['content'].widget.attrs['class'] = 'content_css'
        self.fields['content'].widget.attrs['rows'] = 5

class OrderProductsForm(forms.ModelForm):
    class Meta:
        model = OrderProducts
        fields = ['product','amount','colour']

    def __init__(self, *args, **kwargs):
        super(OrderProductsForm, self).__init__(*args, **kwargs)
        self.fields['urun_grubu'] =  ModelChoiceField(queryset=UrunGrubu.objects.all(),empty_label="Ürün Grubunu sec",
                                    widget=forms.Select(attrs={"onChange":'myFunction(this.value,this.id)'}))
        self.fields['marka'] =  ModelChoiceField(queryset=Marka.objects.all(),empty_label="Marka sec",
                                    widget=forms.Select(attrs={"onChange":'myFunction(this.value,this.id)'}))
        
        #TODO aşağıdaki satırı aktif edince form girişinde hata veriyor. Çözmek gerekiyor. 
        #self.fields['product'].queryset = Product.objects.none()

class OrderProductsForm2(forms.ModelForm):
    class Meta:
        model = OrderProducts
        fields = ['product','amount','colour']
"""
    def __init__(self, *args, **kwargs):
        super(OrderProductsForm, self).__init__(*args, **kwargs)
        self.fields['urun_grubu'] =  ModelChoiceField(queryset=UrunGrubu.objects.all(),empty_label="Ürün Grubunu sec",
                                    widget=forms.Select(attrs={"onChange":'myFunction(this.value,this.id)'}))
        self.fields['marka'] =  ModelChoiceField(queryset=Marka.objects.all(),empty_label="Marka sec")
        #self.fields['product'].queryset = Product.objects.none()
"""
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        #fields = ['product_name','product_category','title','montaj_sabiti','marka','product_type','unit','birim_fiyat']
        fields = ['urun_kodu','product_name','urun_grubu','marka','montaj_sabiti','unit','product_type','birim_fiyat']



class AddressForm(forms.ModelForm):
    class  Meta:
        model = Address
        fields = ['ulke','il','ilce','adres','map_link','aciklama']

class CustomerAddressForm(forms.ModelForm):
    class  Meta:
        model = Address
        fields = ['customer','ulke','il','ilce','adres','mahalle','map_link','aciklama']

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problems
        fields = ['order','description','statu','created_user','urun_grubu']

class ProblemSolutionForm(forms.ModelForm):
    class Meta:
        model = Problems
        fields = ['solution','root_cause']

class ProblemAddForm(forms.ModelForm):
    class Meta:
        model = Problems
        fields=['order','description','statu','created_user','urun_grubu']
    
    def __init__(self, *args, **kwargs):
        super(ProblemAddForm,self).__init__(*args, **kwargs)
        self.fields['customer'] = ModelChoiceField(queryset=Customer.objects.all(),empty_label="Müşteri sec",
                                    widget=forms.Select(attrs={"onChange":'myProblemFunction(this.value,this.id)'}))
