from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Departments(models.Model):
    department_number = models.CharField(max_length=150, unique=True)
    title = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.title

class Sube(models.Model):
    
    title = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.title

class Yetenek(models.Model):
    
    title = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.title

class Yetki(models.Model):
    
    title = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.title

class Employee(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Departments,on_delete=models.PROTECT,verbose_name="Departman",default="1")
    role = models.CharField(max_length=20,blank=True,default="Kullanıcı")
    telephone = models.CharField(max_length=30,verbose_name="Telefon",default="0",blank=True)
    sube = models.ForeignKey(Sube,on_delete=models.PROTECT,verbose_name="Şube",default="1")
    yetenek = models.ManyToManyField(Yetenek)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    
    if created:
        Employee.objects.create(user=instance)
        
        

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.employee.save()


class Logging(models.Model):
    #log type = workflow,order,user,customer,general
    
    date = models.DateTimeField( auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    log_type = models.CharField(max_length=20,verbose_name="Açıklama",default="genel")
    type_id = models.IntegerField(verbose_name="Order ID",default=1)
    aciklama = models.CharField(max_length=100,verbose_name="Açıklama")
    status = models.CharField(max_length=3, verbose_name="Status",default="10",blank=True,null=True)

class Yetkilendirme(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        permissions = (
                        ("siparis_yonetimi", "Satış girişi için gerekli yetki"),
                        ("siparis_listele","Satışları listeleme"),
                        ("urun_listele","Ürün Listeleme"),
                        ("urun_yonetim","Ürün ekleme,güncelleme,deaktif etme"),
                        ("musteri_listele","Müşteri listeleme"),
                        ("musteri_yonetim","Müşteri ekleme,güncelleme,silme"),
                        ("kullanici_listeleme", "Kullanıcı listeleme"),
                        ("kullanici_yonetim", "Kullanıcı yönetimi"),
                        ("rezervasyon_listele","Rezervasyonları listeleme görüntüleme"),
                        ("rezervasyon_yonetim","Rezervasyon yönetim işlemleri"),
                        ("rapor_listele","Rapor listeleme"),
                        ("log_listeleme","Logları görme"),
                        ("musterisikayet_listeleme","Müşteri şikayetleri listele gör"),
                        ("musterisikayet_yonetim","Müşteri şikayetleri yönetimi"),
                        ("workflow_operasyon","Workflow Operasyon "),
                        ("workflow_planlama","Workflow Planlama  "),
                        ("workflow_depo","Workflow Depo "),
                        ("workflow_uretim","Workflow Uretim "),
                        ("test","test yetkisi"),
                       
                      )

    