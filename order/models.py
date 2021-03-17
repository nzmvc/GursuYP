from django.db import migrations,models

from ckeditor.fields import RichTextField
# Create your models here.


class Order (models.Model):
    orderTypeChoise = (
        ("U","Uretim"),
        ("S","Sevk"),
        ("M","Montaj"),
        ("D","Depo Teslim"),
    )
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
        ("31","Takvimlendirildi"),
        ("32","Montaj Müşteriden haber bekleniyor"),
        ("34","Montaj planlandı"),
        ("40","Montaj operasyonu bekleniyor."),
        ("42","Montaj başlandı"),
        ("44","Montaj durdu "),
        ("46","Montaj tamamlandı "),
        ("50","Depo teslim alma için müşteriyi bekliyor "),
        ("52","Depo müşteriye teslim etti "),
        ("80","Sorun var"),
        ("90","Tamamlandı"),
    )

    customer = models.ForeignKey("Customer",on_delete=models.CASCADE,verbose_name="Müşteri ID")
    #TODO user bilgisi eklenecek
    create_date = models.DateTimeField(auto_now=True)
    content = RichTextField()
    order_image = models.FileField(blank =True,null=True,verbose_name="Sipariş Formunu Ekleyiniz")
    stok = models.CharField(max_length=1,choices = [('1', 'Var'), ('0', 'Yok')],verbose_name="Stok Durumu",default="0")
    order_type = models.CharField(max_length=1,choices = orderTypeChoise,verbose_name="Sipariş Tipi")
    statu = models.CharField(max_length=2,choices = status,verbose_name="Sipariş Durumu",default="0")

class Customer(models.Model):

    customer_name = models.CharField(max_length=50,verbose_name="MÜŞTERİ ADI")
    telephone = models.CharField(max_length=50,verbose_name="TELEFON")
    email = models.CharField( max_length=254,verbose_name="EMAIL")
    created_date = models.DateTimeField(auto_now=True)
    active = models.CharField(max_length=1,default="1",verbose_name="Aktif")

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
    status = models.CharField(max_length=10,choices = workflow_status,verbose_name="Durum",default="10")
    comment = models.CharField(max_length=50,verbose_name="Açıklama",default="test")
    created_date =models.DateTimeField(auto_now=True)
    planed_date =models.DateTimeField(blank=True, null=True)
    completed_date =models.DateTimeField(blank=True, null=True)
    started_date =models.DateTimeField(blank=True, null=True)

class Product(models.Model):
    product_name = models.CharField(max_length=20,verbose_name="Ürün adı")
    title = models.CharField(max_length=150, unique=True,verbose_name="Kısa ad(kod)")
    #category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    marka = models.CharField(max_length=15,verbose_name="Marka")
    product_type = models.CharField(max_length=15,verbose_name="Cinsi",help_text="xxx gibi bilgiler")
    unit = models.CharField(max_length=10,verbose_name="Birim",default="Adet")
    montaj_sabiti = models.IntegerField(verbose_name="Montaj Sabiti")
    created_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    

class Category(models.Model):
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
    # renk marka vs eklenebilir
    def __str__(self):
        return self.product.product_name
        