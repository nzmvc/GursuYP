from django.db import migrations,models
from user.models import User,Employee
from ckeditor.fields import RichTextField
# Create your models here.


class OrderStatu(models.Model):
    number = models.IntegerField(verbose_name="Durum Numarası")
    title =  models.CharField(verbose_name="Order Statu",max_length=50)
    aciklama =  models.CharField(verbose_name="Açıklama",max_length=50,null=True)
    def __str__(self):
        return self.title

class Order (models.Model):
    orderTypeChoise = (
        ("U","Uretim"),
        ("S","Sevk"),
        ("M","Montaj"),
        ("D","Depo Teslim"),
    )
 
    """
    status = (
        ("00","Beklemede"),
        ("10","Uretim planı bekleniyor"),
        ("12","Uretim planlandı"),
        ("14","Uretimde"),
        ("16","Uretim tamamlandı"),
        ("20","Sevk planı bekleniyor"),
        ("22","Sevk planlandı"),
        ("24","Sevk alanında"),
        ("26","Sevk edildi"),
        ("28","Sevk teslim edildi"),
        ("30","Montaj planı bekleniyor"),
        ("32","Takvimlendirildi"),
        ("34","Montaj Müşteriden haber bekleniyor"),
        ("36","Montaj planlandı"),
        ("40","Montaj operasyonu bekleniyor."),
        ("42","Montaj başlandı"),
        ("44","Montaj durdu "),
        ("46","Montaj tamamlandı "),
        ("50","Depo teslim alma için müşteriyi bekliyor "),
        ("52","Depo müşteriye teslim etti "),
        ("80","Sorun var"),
        ("90","Tamamlandı"),
    )
    """
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE,verbose_name="Müşteri ID")
    #TODO user bilgisi eklenecek
    create_date = models.DateTimeField(auto_now=True)
    content = RichTextField()
    order_image = models.FileField(blank =True,null=True,verbose_name="Sipariş Formunu Ekleyiniz")
    stok = models.CharField(max_length=1,choices = [('1', 'Var'), ('0', 'Yok')],verbose_name="Stok Durumu",default="0")
    order_type = models.CharField(max_length=1,choices = orderTypeChoise,verbose_name="Sipariş Tipi")
    #statu = models.CharField(max_length=2,choices = status,verbose_name="Sipariş Durumu",default="0")
    statu = models.ForeignKey(OrderStatu,on_delete=models.PROTECT,default=23)
    iskonto = models.IntegerField(default=0,verbose_name="İskonto Oranı(%)")
    tahmini_tarih_min = models.DateField(null=True,verbose_name="En erken teslim (yyyy-mm-dd)")
    tahmini_tarih_max = models.DateField(null=True,verbose_name="En geç teslim (yyyy-mm-dd)")

    def __str__(self):
        #return self.customer.customer_name
        title= self.customer.customer_name+"_"+str(self.create_date)[:10]
        return title

class Customer(models.Model):
    # customer type vergi yada tc no için gerekli
    customer_type=(("Şahıs","Şahıs"),("Kurumsal","Kurumsal")    )
    customer_name = models.CharField(max_length=50,verbose_name="MÜŞTERİ ADI")
    telephone = models.CharField(max_length=50,verbose_name="TELEFON")
    email = models.CharField( max_length=254,verbose_name="EMAIL")
    created_date = models.DateTimeField(auto_now=True)
    active = models.CharField(max_length=1,default="1",verbose_name="Aktif")
    vergi_no = models.IntegerField(verbose_name="Vergi/TC no",default=0,null=True)
    customer_type = models.CharField(max_length=10,choices = customer_type,verbose_name="Şahıs/Kurumsal",default=customer_type[0][1])
    vergi_dairesi = models.CharField(max_length=70,verbose_name="Vergi Dairesi",default="Fethiye VD.")
    def __str__(self):  # müşterileri listelerken gözükmesini istediğimiz isim
        return self.customer_name

class Address (models.Model):
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE,verbose_name="Müşteri ID")
    ulke = models.CharField( max_length=30,verbose_name="ULKE",default="Türkiye")
    il = models.CharField( max_length=30,verbose_name="IL")
    ilce = models.CharField( max_length=30,verbose_name="İLÇE")
    adres = models.CharField( max_length=100,verbose_name="ADRES")
    map_link = models.CharField( max_length=100,verbose_name="GOOGLE MAP")
    active = models.BooleanField(default=True)

class Workflow(models.Model):
    departments = (
        
        ("10000","Finans"),
        ("20000","Mali ve İdari işler"),
        ("30000","Satış"),
        ("31000","Saha Görevlisi"),
        ("40000","Operasyon"),
        ("41000","Planlama"),
        ("42000","Üretim"),
        ("43000","Depo"),
        ("44000","Montaj"),
        
    )
    workflow_status = (
            ("10","Beklemede"),
            ("20","Çalışılıyor"),
            ("30","İptal edildi"),
            ("40","Tamamlandı"),
            
    )
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE,default=1)
    department = models.CharField(max_length=10,choices = departments,verbose_name="Departman")
    revision    = models.IntegerField(verbose_name="Revizyon",default=1)
    approve_user_id = models.IntegerField(verbose_name="İşi onaylayan kullanıcı",blank=True, null=True)
    completed_user_id = models.IntegerField(verbose_name="İşi yapan Kullanıcı",blank=True, null=True)
    #status = models.CharField(max_length=10,choices = workflow_status,verbose_name="Durum",default="10")
    status = models.ForeignKey(OrderStatu,on_delete=models.PROTECT)
    comment = models.CharField(max_length=50,verbose_name="Açıklama",default="test")
    created_date =models.DateTimeField(auto_now=True)
    planed_date =models.DateTimeField(blank=True, null=True)
    completed_date =models.DateTimeField(blank=True, null=True)
    started_date =models.DateTimeField(blank=True, null=True)
    fisNo = models.IntegerField(verbose_name="Fiş NO",default=1,null=True)

class Product(models.Model):
    product_name = models.CharField(max_length=20,verbose_name="Ürün adı")
    title = models.CharField(max_length=150, unique=True,verbose_name="Kısa ad(kod)")
    #category = models.ForeignKey(ProductCategory, null=True, on_delete=models.SET_NULL)
    marka = models.CharField(max_length=15,verbose_name="Marka")
    product_type = models.CharField(max_length=15,verbose_name="Cinsi",help_text="xxx gibi bilgiler")
    unit = models.CharField(max_length=10,verbose_name="Birim",default="Adet")
    montaj_sabiti = models.IntegerField(verbose_name="Montaj Sabiti")
    birim_fiyat = models.IntegerField(verbose_name="Birim Fiyat" ,default=0)
    created_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.title
    

class ProductCategory(models.Model):
    title = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

class OrderProducts(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    colour = models.CharField(max_length=20,verbose_name="Renk",blank=True)
    amount  = models.IntegerField(default=1)
    birim_fiyat = models.IntegerField(default=0)
    toplam_tutar = models.IntegerField(default=0)
    # renk marka vs eklenebilir
    def __str__(self):
        return self.product.product_name

class RootCause(models.Model):
    title = models.CharField(max_length=30,verbose_name="Durum")
    def __str__(self):
        return self.title

class ProblemStatu(models.Model):
    title = models.CharField(max_length=30,verbose_name="Durum")
    def __str__(self):
        return self.title
        
class Problems(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    statu = models.ForeignKey(ProblemStatu,on_delete=models.CASCADE,default=1)
    closed_date = models.DateTimeField(blank=True,null=True)
    root_cause = models.ForeignKey(RootCause,on_delete=models.CASCADE,blank=True,null=True)
    description = RichTextField(null=True)
    solution = RichTextField(null=True)
    created_user = models.ForeignKey(Employee,on_delete=models.CASCADE)

class Vehicle(models.Model):
    vehicle_type = (
        ("Araba","Araba"),
        ("Kamyonet","Kamyonet"),
        ("Kamyon","Kamyon"),
    )
    type_name = models.CharField(choices=vehicle_type, max_length=10,verbose_name="Araç Tipi")
    type_id = models.CharField(verbose_name="Plaka",max_length=10)
    description = models.CharField(verbose_name="Açıklama",max_length=50,null=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.type_id
    
class Reservation(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    start_date = models.DateTimeField(verbose_name="Başlangıç Zamanı")
    end_date = models.DateTimeField(verbose_name="Bitiş Zamanı")
    version = models.IntegerField(default=1)
    description = models.CharField(verbose_name="Açıklama",max_length=100,null=True)

class ReservationPerson(models.Model):
    reservation = models.ForeignKey(Reservation,on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)

class ReservationVehicle(models.Model):
    reservation = models.ForeignKey(Reservation,on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE)