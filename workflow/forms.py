from django import forms
from django.contrib.auth.models import User

class WorkflowForm(forms.Form){

    departments = (
        ("11","Satış"),
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


}