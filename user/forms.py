from django import forms
from django.contrib.auth.models import User
from .models import Employee


class LoginForm(forms.Form):
    username = forms.CharField(label = "Username")
    password = forms.CharField(label = "Password",widget=forms.PasswordInput)

#class RegisterForm(forms.Form):
class RegisterForm(forms.ModelForm):

    username = forms.CharField(max_length=50, label="Kullanıcı Adı")
    password = forms.CharField(max_length=20,label="Sifre",widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20,label="Parola doğrula",widget=forms.PasswordInput)
    telephone = forms.CharField(max_length=50, label="Telefon")
    email = forms.EmailField(max_length=100,label="email")
    #sube = forms.ChoiceField(label="Şube")
    first_name = forms.CharField(max_length=20, label="İsim")
    last_name = forms.CharField(max_length=20, label="Soyad")
    
    #department = forms.ChoiceField(label="Departmant")
    
    def clean(self):
        username    = self.cleaned_data.get("username")
        password    = self.cleaned_data.get("password")
        first_name  = self.cleaned_data.get("first_name")
        last_name   = self.cleaned_data.get("last_name")
        confirm     = self.cleaned_data.get("confirm")
        telephone   = self.cleaned_data.get("telephone")
        email       = self.cleaned_data.get("email")
        sube        = self.cleaned_data.get("sube")
        department  = self.cleaned_data.get("department")
        yetenek      = self.cleaned_data.get("yetenek")
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
            "department":department,
            "yetenek":yetenek,
        }
        return values

    class Meta:
        model = Employee
        #fields = ['username','password','first_name','last_name','sube','department','yetenek']
        fields = ['username','password','sube','department','yetenek','telephone']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
        #fields = ['username','email','first_name','last_name','telephone','sube','department','yetenek']


class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['sube','department','telephone']

class ChangePassword(forms.ModelForm):

    password = forms.CharField(max_length=20,label="Sifre",widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20,label="Parola doğrula",widget=forms.PasswordInput)

    def clean(self):
        password    = self.cleaned_data.get("password")
        confirm     = self.cleaned_data.get("confirm")

        if password != confirm:
            
            raise forms.ValidationError("parolalar eşleşmiyor")

        values = {
            "password":password,
            "confirm":confirm
        }
        return values