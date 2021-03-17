from django import forms
from django.contrib.auth.models import User
from .models import Employee


class LoginForm(forms.Form):
    username = forms.CharField(label = "Username")
    password = forms.CharField(label = "Password",widget=forms.PasswordInput)

#class RegisterForm(forms.Form):
class RegisterForm(forms.ModelForm):
    subeChoice = CHOICES =( 
    ("1", "Fethiye"), 
    ("2", "Muğla"), 
    ("3", "Bodrum"), 
    ("4", "Marmaris"), 
    ("5", "Antalya"), 
    ) 

    userType = CHOICES =( 
    ("1", "Yönetici"), 
    ("2", "Satış"), 
    ("3", "Taşeron"), 
    
    ) 
    beceri_choice = (
        ('n/a','n/a'),
        ('ADOKAPI','ADOKAPI'),
        ('PARKE','PARKE'),
        ('ÇELİKKAPI','ÇELİKKAPI'),
        ('YANGIN KAPISI','YANGIN KAPISI'),
        ('MONTAJCI','MONTAJCI'),
        ('MARANGOZ','MARANGOZ'),
    )
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

    username = forms.CharField(max_length=50, label="Kullanıcı Adı")
    password = forms.CharField(max_length=20,label="Sifre",widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20,label="Parola doğrula",widget=forms.PasswordInput)
    telephone = forms.CharField(max_length=50, label="Telefon")
    email = forms.EmailField(max_length=100,label="email")
    sube = forms.ChoiceField(choices=subeChoice,label="Şube")
    first_name = forms.CharField(max_length=20, label="İsim")
    last_name = forms.CharField(max_length=20, label="Soyad")
    user_type =  forms.ChoiceField(choices=userType,label="Kullanıcı tipi")
    department = forms.ChoiceField(choices=departments,label="Departmant")
    beceri = forms.ChoiceField(choices=beceri_choice,label="Ustalık")
    
    def clean(self):
        username    = self.cleaned_data.get("username")
        password    = self.cleaned_data.get("password")
        first_name  = self.cleaned_data.get("first_name")
        last_name   = self.cleaned_data.get("last_name")
        confirm     = self.cleaned_data.get("confirm")
        telephone   = self.cleaned_data.get("telephone")
        email       = self.cleaned_data.get("email")
        sube        = self.cleaned_data.get("sube")
        user_type   = self.cleaned_data.get("user_type")
        department  = self.cleaned_data.get("department")
        beceri      = self.cleaned_data.get("beceri")
        #if username and password and password != confirm:
        if password != confirm:
            
            raise forms.ValidationError("parolalar eşleşmiyor")

        values = {
            "username":username,
            "password":password,
            "telephone":telephone,
            "email":email,
            "sube":sube,
            "first_name":first_name,
            "last_name":last_name,
            "user_type":user_type,
            "department":department,
            "beceri":beceri,
        }
        return values

    class Meta:
        model = Employee
        fields = ['username','password','email','telephone','first_name','last_name']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        #fields = ['username','password','email','telephone','first_name','last_name']
        fields = ['username','password','email','first_name','last_name']
