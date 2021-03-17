from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Workflow(models.Model):
    
    order_id= models.CharField(max_length=10,verbose_name="Order ID")
    department = models.CharField(max_length=10,verbose_name="Order ID")
    revision    = models.IntegerField(max_length=2,verbose_name="Revizyon")
    approve_user_id = models.IntegerField(max_length=6,verbose_name="İşi onaylayan kullanıcı")
    completed_user_id = models.IntegerField(max_length=6,verbose_name="İşi yapan Kullanıcı")
    status = models.CharField(max_length=10,verbose_name="Order ID")
    created_date =models.DateField(auto_now=True)
    planed_date =models.DateField(blank=True, null=True)
    completed_date =models.DateField(blank=True, null=True)



