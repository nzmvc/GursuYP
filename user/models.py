from django.db import models
from django.contrib.auth.models import User
from order.models import Order
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Employee(models.Model):
    beceri_choice = (
        ('ADOKAPI','ADOKAPI'),
        ('PARKE','PARKE'),
        ('ÇELİKKAPI','ÇELİKKAPI'),
        ('YANGIN KAPISI','YANGIN KAPISI'),
        ('MONTAJCI','MONTAJCI'),
        ('MARANGOZ','MARANGOZ'),
    )
    subeChoice = ( 
    ("Fethiye", "Fethiye"), 
    ("Muğla", "Muğla"), 
    ("Bodrum", "Bodrum"), 
    ("Marmaris", "Marmaris"), 
    ("Antalya", "Antalya"), 
    ) 

    userType =( 
    ("1", "Yönetici"), 
    ("2", "Satış"), 
    ("3", "Taşeron"), 
    
    )
    
    departments = (
        
        ("10000","Finans"),
        ("20000","Mali ve İdari işler"),
        ("30000","Satış"),
        ("31000","Saha Görevlisi"),
        ("40000","Operasyon"),
        ("41000","Planlama"),
        
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100,choices = departments,blank=True)
    role = models.CharField(max_length=20,blank=True)
    telephone = models.CharField(max_length=30,verbose_name="Telefon",default="0",blank=True)
    user_type = models.CharField(max_length=30,choices = userType,verbose_name="Kullanıcı Tipi",default="0",blank=True)
    sube = models.CharField(max_length=30,choices = subeChoice,verbose_name="Şube",default="0",blank=True)
    beceri = models.CharField(max_length=30,choices = beceri_choice,verbose_name="Beceri",default="0",blank=True)

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

class Departments(models.Model):
    department_number = models.CharField(max_length=150, unique=True)
    title = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.title

    """    departments = (
        
        ("10000","Finans"),
        ("20000","Mali ve İdari işler"),
        ("30000","Satış"),
        ("31000","Saha Görevlisi"),
        ("40000","Operasyon"),
        ("41000","Planlama"),
        ("42000","Üretim"),
        ("43000","Depo"),
        ("44000","Montaj"),
        
    )"""