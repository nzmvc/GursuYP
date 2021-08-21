from re import VERBOSE
from django import forms
from .models import Customer,Order,Product,Workflow,Address,OrderProducts,Problems,ProductCategory,UrunGrubu,Marka
from crispy_forms.layout import Layout, Fieldset,Field
from django.forms import ModelChoiceField

class CustomerForm(forms.ModelForm):
    
    class Meta:

        model = Customer
        fields = ['customer_name','telephone','email','customer_type','vergi_no','vergi_dairesi','satis_kanali']
        
class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        #stok = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('1', 'Var'), ('0', 'Yok')])
        fields = ['customer','content','planlama_sekli','order_image','stok','iskonto','tahmini_tarih_min','tahmini_tarih_max', ]
        #field_order=["customer"]
        ordered_field_names = ['customer']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['customer'].queryset = self.fields['customer'].queryset.order_by('customer_name')
        #self.fields['dosyaVarYok'] = forms.ChoiceField(label='Ölçüm Dosyası',choices=[('VAR','VAR'),('YOK','YOK')], widget=forms.RadioSelect)

        self.fields['tahmini_tarih_min'].widget.attrs['class'] = 'datepicker'
        self.fields['content'].widget.attrs['class'] = 'content_css'
        self.fields['content'].widget.attrs['rows'] = 5

class OrderDosya(forms.ModelForm):
    class Meta:
        model=Order
        fields = ['order_image']


class OrderProductsForm(forms.ModelForm):
    class Meta:
        model = OrderProducts
        fields = ['amount','colour']

    def __init__(self, *args, **kwargs):  # fieldlar change olduğunda çalışacak fonksiyon ve gonderilecek parametreler belirleniyor
        super(OrderProductsForm, self).__init__(*args, **kwargs)
        self.fields['urun_grubu'] =  ModelChoiceField(queryset=UrunGrubu.objects.all(),empty_label="Ürün Grubunu sec",
                                    widget=forms.Select(attrs={"onChange":'showCategoryFunction(this.value,this.id)'}))
        """self.fields['marka'] =  ModelChoiceField(queryset=Marka.objects.all(),empty_label="Marka sec",
                                    widget=forms.Select(attrs={"onChange":'myFunction(this.value,this.id)'}))
        """
        self.fields['product_category'] = ModelChoiceField(queryset=ProductCategory.objects.all(),empty_label="Ürün Grubunu sec",
                                    widget=forms.Select(attrs={"onChange":'myFunction(this.value,this.id)'}))
        self.fields['product'] = forms.CharField(widget=forms.Select(attrs={"onChange":'colorFunction(this.value,this.id)'}))
        

class OrderProductsForm2(forms.ModelForm):
    class Meta:
        model = OrderProducts
        fields = ['product','amount','colour']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['urun_kodu','product_name','urun_grubu','marka','montaj_sabiti','unit','birim_fiyat']

class AddressForm(forms.ModelForm):
    class  Meta:
        model = Address
        fields = ['ulke','il','ilce','adres','map_link','aciklama','mahalle']

class CustomerAddressForm(forms.ModelForm):
    class  Meta:
        model = Address
        fields = ['customer','ulke','il','ilce','adres','mahalle','map_link','aciklama']

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problems
        #fields = ['order','created_user','description','problem_file']
        fields = ['description','problem_file']

class ProblemSolutionForm(forms.ModelForm):
    class Meta:
        model = Problems
        fields = ['solution','root_cause']

class ProblemAddForm(forms.ModelForm):
    class Meta:
        model = Problems
        fields=['order','description','statu','created_user','problem_file']
    '''
    def __init__(self, *args, **kwargs):
        super(ProblemAddForm,self).__init__(*args, **kwargs)
        self.fields['customer'] = ModelChoiceField(queryset=Customer.objects.all(),empty_label="Müşteri sec",
                                    widget=forms.Select(attrs={"onChange":'myProblemFunction(this.value,this.id)'}))
    '''