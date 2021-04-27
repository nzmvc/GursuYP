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
    satisKanalSecenek = (
        ("Perakende","Perakende"),
        ("Toptan","Toptan"),
        ("Proje","Proje")
    )
    planlamaSecenek = (
        ("En Hızlı","En Hızlı"),
        ("Müş.den Haber Bekle","Müş.den Haber Bekle"),
        ("Müsaitliğimize Göre","Müsaitliğimize Göre")
    )
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE,verbose_name="Müşteri")
    #TODO user bilgisi eklenecek
    create_date = models.DateTimeField(auto_now=True)
    content = RichTextField(verbose_name="Açıklama")
    order_image = models.FileField(blank =True,null=True,verbose_name="Sipariş Formunu Ekleyiniz")
    stok = models.CharField(max_length=1,choices = [('1', 'Var'), ('0', 'Yok')],verbose_name="Stok Durumu",default="0")
    order_type = models.CharField(max_length=1,choices = orderTypeChoise,verbose_name="Sipariş Tipi")
    #statu = models.CharField(max_length=2,choices = status,verbose_name="Sipariş Durumu",default="0")
    statu = models.ForeignKey(OrderStatu,on_delete=models.PROTECT,default=23)
    iskonto = models.IntegerField(default=0,verbose_name="İskonto Oranı(%)")
    tahmini_tarih_min = models.DateField(null=True,verbose_name="En erken teslim (yyyy-mm-dd)")
    tahmini_tarih_max = models.DateField(null=True,verbose_name="En geç teslim (yyyy-mm-dd)")
    sevk_adres = models.ForeignKey("Address",on_delete=models.PROTECT,verbose_name="Sevk Adresi",null=True)
    satis_kanali = models.CharField(max_length=10,choices = satisKanalSecenek,verbose_name="Satış Kanalı")
    planlama_sekli = models.CharField(max_length=20,choices = planlamaSecenek,verbose_name="Planlama Şekli",default="En Hızlı")
    #
    # fatura_adres = models.ManyToManyField("Address",verbose_name="Fatura Adresi")

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
    aciklama = models.CharField( max_length=10,verbose_name="Açıklama(kısa/kod)")
    active = models.BooleanField(default=True)
    def __str__(self):  # listelerken gözükmesini istediğimiz isim
        return self.aciklama

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

class ProductCategory(models.Model):
    title = models.CharField(max_length=150, unique=True)
    main_category = models.CharField(max_length=2,default=1)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

class UrunGrubu(models.Model):
    title = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.title

class ProductType(models.Model):
    title = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.title

class Marka(models.Model):
    title = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.title

class Product(models.Model):
    unit_type = (
            ("AD","AD"),
            ("TN","TN"),
            ("M2","M2"),
            ("PK","PK"),
            ("TK","TK"),
            ("MT","MT"),
            ("BY","BY"),
            ("M3","M3"),
            ("KG","KG"),
       )
    
    urun_kodu = models.CharField(max_length=100,verbose_name="Ürün Kodu",blank=True, null=True)
    product_name = models.CharField(max_length=200,verbose_name="Ürün adı")
    marka = models.ForeignKey(Marka,on_delete=models.CASCADE,verbose_name="Urun Grubu",default=1)
    unit = models.CharField(max_length=10,choices=unit_type,verbose_name="Birim",default="AD")
    urun_grubu = models.ForeignKey(UrunGrubu,on_delete=models.CASCADE,verbose_name="Urun Grubu",default=1)
    product_type =models.ForeignKey(ProductType,on_delete=models.CASCADE,verbose_name="Product Type",default=1)
    montaj_sabiti = models.IntegerField(verbose_name="Montaj Sabiti",default=0)
    birim_fiyat = models.IntegerField(verbose_name="Birim Fiyat" ,default=0)
    product_category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE,verbose_name="Kategori",default=1)
    
    #title = models.CharField(max_length=150, unique=True,verbose_name="Kısa ad(kod)")
    #category = models.ForeignKey(ProductCategory, null=True, on_delete=models.SET_NULL)
    
    created_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    #def __str__(self):    
    #    return self.product_category.title +"-"+ self.product_name
    

class OrderProducts(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    colour = models.CharField(max_length=20,verbose_name="Renk",blank=True)
    amount  = models.IntegerField(default=0)
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
    urun_grubu = models.ForeignKey(UrunGrubu,on_delete=models.CASCADE)
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
    urun_grubu = models.ForeignKey(UrunGrubu,on_delete=models.CASCADE,default=1)
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