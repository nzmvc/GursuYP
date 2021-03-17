from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .forms import RegisterForm,LoginForm,UserUpdateForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import  Logging
# Create your views here.
from user.models import Employee,Logging

def Logla(user,message,log_type,type_id,status):
    entry = Logging(user=user,aciklama=message,log_type=log_type,type_id=type_id,status=status)
    entry.save()

def loginPage(request):
    form = LoginForm(request.POST or None)
    context = {'form':form}

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, password=password, username=username,is_active=1)
        if user is None:
            messages.info(request,"Kullanıcı adı veya parola hatalı")
            return render(request,"login.html",context)
        messages.success(request,"başarıyla giriş yaptınız")
        login(request, user)
        return redirect("/order/dashboard")


    return  render(request,'login.html',context)

def logoutPage(request):
    logout(request)
    return  redirect("/user/login")


@login_required(login_url='/user/login/')
def userAdd(request):
    form = RegisterForm(request.POST or None)
    

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        telephone = form.cleaned_data.get("telephone")
        email = form.cleaned_data.get("email")
        sube = form.cleaned_data.get("sube")
        department = form.cleaned_data.get("department")
        user_type = form.cleaned_data.get("user_type")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        beceri = form.cleaned_data.get("beceri")
        newUser = User( username = username,email=email,first_name=first_name,last_name=last_name)
        #newUser = form.save(commit= False)
        

        newUser.set_password(password)
        newUser.save()
        newEmployee = Employee.objects.get(user = newUser)
        newEmployee.department = department
        newEmployee.sube = sube
        newEmployee.telephone = telephone
        newEmployee.user_type = user_type
        newEmployee.beceri = beceri
        
        
        
        
        try:
            
            newEmployee.save()
            Logla(request.user,"kayit yapıldı","user islem",1,"1")
        
        except:
            #TODO   employee save edilemezse kullanıcının da silinmesi gerekir
            newUser.delete()
            messages.warning(request,"!!! HATA girdiğiniz bilgilerde bir problem var")

        #return redirect("/user/userList")
        
        #login(request,newUser)
        
        
    
    context = {'form':form}
    return  render(request,'userAdd.html',context)

@login_required(login_url='/user/login/')
def userView(request,id):
    user = get_object_or_404(User,id=id)
    print("user detay ",user.first_name)
    return  render(request,'userView.html',{'user':user})

@login_required(login_url='/user/login/')
def userList(request):
    keyword = request.GET.get("keyword")
    if keyword:
        users = User.objects.filter(username__contains = keyword)
        return  render(request,'userList.html',{'users':users})    

    users = User.objects.all().select_related('employee')
    return  render(request,'userList.html',{'users':users})

@login_required(login_url='/user/login/')
def userUpdate(request,id):
    #TODO kullanıcı güncellemede form bilgilerinin tamamına erişemedim. form ile model arası bir uyumsuzluk olabilir
    # güncelleme için farklı bir form tanımlayarak kısıtlı verilerle güncelleme yapılıyor
    # password güncellemesi için  ayrı bir buton koyalım
    user = get_object_or_404(User,id=id)
    print( user)
    #form = RegisterForm(request.POST or None, request.FILES or None,instance=user)
    form = UserUpdateForm(request.POST or None, request.FILES or None,instance=user)
    
    if form.is_valid() :
        user = form.save(commit= False)
        #user.department =
        user.save()
        messages.success(request,"kullanıcı güncellendi")
        return redirect("/user/userList")
    
    return  render(request,'userUpdate.html',{'form':form})

@login_required(login_url='/user/login/')
def userDelete(request,id):
    print("silinecek id:",id)
    user = get_object_or_404(User,id=id)
    if user :
        user.delete()
        messages.success(request,"Kullanıcı silindi")
    else:
        messages.success(request,"Kullanıcı bulunamadı!!!!!!")
    return  redirect("/user/userList")


@login_required(login_url='/user/login/')
def logView(request):
    keyword = request.GET.get("keyword")
    if keyword:
        loglar = Logging.objects.filter(aciklama__contains = keyword) | Logging.objects.filter(log_type__contains=keyword)
    else:
        loglar = Logging.objects.all()

    return  render(request,"loglar.html",{'loglar':loglar})