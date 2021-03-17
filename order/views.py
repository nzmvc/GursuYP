from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm,OrderForm,ProductForm,AddressForm,OrderProductsForm
from .models import Customer,Order,Workflow,Product,Address,OrderProducts
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib import messages
from user.views import Logla
from user.models import Logging
import datetime
# Create your views here.
#TODO tum işlemler loglanmalı. hatta silem yapılmamalı yada sadece superuser yapabilsin. diğerlerinin yaptıkları inaktif edebilir.


############################################################################
#######################  DASHBOARD         #################################
############################################################################
@login_required(login_url='/user/login/')
def dashboard(request):
    
    order = Order.objects.all()
    customer = Customer.objects.all()
    product = Product.objects.all()
    workflow = Workflow.objects.all()
    
    planlama_jobs = Workflow.objects.filter(department=41000)
    operasyon_jobs = Workflow.objects.filter(department=44000)
    uretim_jobs = Workflow.objects.filter(department=42000)
    depo_jobs = Workflow.objects.filter(department=43000)
    
    content = {
        'planlama_jobs':planlama_jobs,
        'operasyon_jobs' : operasyon_jobs,
        'uretim_jobs':uretim_jobs,
        'depo_jobs' : depo_jobs,
        'order':order,
        'customer' :customer,
        'product':product,
        'workflow':workflow
        }
    return  render(request,'dashboard.html',content)


def dashboard2(request):
    
    planlama_jobs = Workflow.objects.filter(department=41000)
    operasyon_jobs = Workflow.objects.filter(department=44000)
    uretim_jobs = Workflow.objects.filter(department=42000)
    depo_jobs = Workflow.objects.filter(department=43000)
    
    content = {
        'planlama_jobs':planlama_jobs,
        'operasyon_jobs' : operasyon_jobs,
        'uretim_jobs':uretim_jobs,
        'depo_jobs' : depo_jobs
        }
    return  render(request,'dashboard2.html',content)



def about(request):
    #return HttpResponse("Merhaba ana sayfa")
    return render(request,"about.html")



############################################################################
#######################  ORDER             #################################
############################################################################
@login_required(login_url='/user/login/')
def orderAdd(request):
    form = OrderForm(request.POST or None,request.FILES or None)

    if form.is_valid():
            
            #form.save()
            # fields = ['customer','content','order_image','order_type' ]
            customer = form.cleaned_data.get("customer")
            order_type = form.cleaned_data.get("order_type")
            order_image = form.cleaned_data.get("order_image")
            order_content = form.cleaned_data.get("content")
            stok = form.cleaned_data.get("stok")

            
            
            new_order = Order(customer=customer,order_type=order_type,order_image=order_image,content=order_content)
            new_order.save()
            Logla(request.user,"yeni satış işlemi girildi",log_type="order",type_id=new_order.pk,status="10")

            # sipariş girişi ile beraber  departmanlara tasklar gonderilir
            #TODO test için hepsine gönderiliyor. fakat ürün ve hizmet seçimine göre task oluşmalı
            if stok == "0": # stokta ürün yoksa üretim birimine iş atanır.
                workflow_uretim = Workflow(department="42000",status="10",order=new_order)
                workflow_uretim.save()
                Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_uretim",type_id=workflow_uretim.pk,status="10")
            if order_type == "D":
                workflow_depoTeslim = Workflow(department="43000",status="50",order=new_order)
                workflow_depoTeslim.save()
                Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_depoTeslim",type_id=workflow_depoTeslim.pk,status="50")

            if order_type == "S":
                workflow_planlama_sevk = Workflow(department="41000",status="20",order=new_order)
                workflow_planlama_sevk.save()
                Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_depoTeslim",type_id=workflow_planlama_sevk.pk,status="20")

            if order_type == "M":
                workflow_planlama_sevk = Workflow(department="41000",status="20",order=new_order)
                workflow_planlama_montaj = Workflow(department="41000",status="30",order=new_order)
                workflow_montaj = Workflow(department="44000",status="40",order=new_order)
                workflow_planlama_sevk.save()
                workflow_planlama_montaj.save()
                workflow_montaj.save()
                Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_planlama_sevk",type_id=workflow_planlama_sevk.pk,status="20")
                Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_planlama_montaj",type_id=workflow_planlama_montaj.pk,status="30")
                Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_montaj",type_id=workflow_montaj.pk,status="40")


            #TODO sipariş ıd si bilgi olarak verilebilir mi?
            messages.warning(request," Sipariş girildi. Lütfen Ürünleri ekleyiniz!!!!")   

            #TODO 

            return  redirect('/order/orderView/'+str(new_order.pk))



    return  render(request,'orderAdd.html',{'form':form})


@login_required(login_url='/user/login/')
def orderList(request):
    orders= Order.objects.all()
    return  render(request,'orderList.html',{'orders':orders})


@login_required(login_url='/user/login/')
def orderUpdate(request,id):
    order = get_object_or_404(Order,id=id)
    form = OrderForm(request.POST or None, request.FILES or None,instance=order)
    if form.is_valid() :
        order = form.save(commit= False)
        order.save()
        messages.success(request,"sipariş bilgileri güncellendi")
        Logla(request.user,"sipariş güncellendi","orderUpdate",order.id,10)
        return redirect("/order/orderList")
    return  render(request,'orderUpdate.html',{'form':form})

@login_required(login_url='/user/login/')
def orderDelete(request,id):
    order = get_object_or_404(Order,id=id)
    if order :
        order.delete()
        Logla(request.user,"sipariş silindi","orderDelete",id,10)
        
        messages.success(request,"Sipariş silindi")
    else:
        messages.success(request,"Sipariş bulunamadı!!!!!!")
    return  redirect("/order/orderList")

@login_required(login_url='/user/login/')
def orderView(request,id):
    order = get_object_or_404(Order,id=id)
    workflows = Workflow.objects.filter(order_id=id)
    orderProducts = OrderProducts.objects.filter(order =order)
   
    #logs    = Logging.objects.filter(log_type="order",type_id=id)
    logs={}
    print(order.order_image)
    
    if order :
        return render(request,"orderView.html",{'order':order,'workflows':workflows,'logs':logs,'orderProducts':orderProducts})
        
    else:
        messages.success(request,"Sipariş bulunamadı!!!!!!")
    return  redirect("/order/orderList")

@login_required(login_url='/user/login/')
def orderAddProduct(request,id):
    #OrderFormSet = inlineformset_factory(Customer,Order, fields('product','amount'),extra=5 )
    order = Order.objects.get(id=id)
    form = OrderProductsForm(initial={'order':order})

    #formset = OrderFormSet(instance= customer)

    if request.method == 'POST':
        """
        formset = OrderFormSet(instance= customer)
        if formset.is_valid():
            formset.save()
            return redirect('/order/orderList')
        """
        form = OrderProductsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/order/orderView/'+ str(id) )
    
    return render( request,'orderAddProduct.html',{'form':form})
    #return render( request,'orderProductform.html',{'formset':formset})
    

############################################################################
#######################  CUSTOMER          #################################
############################################################################
@login_required(login_url='/user/login/')
def customerAdd(request):
    form = CustomerForm(request.POST or None,request.FILES or None)
    form_adress = AddressForm(request.POST or None,request.FILES or None)
    if form.is_valid() and form_adress.is_valid() :
        form.save()
        
        #TODO hata kontrolü try except
        messages.info(request," Müşteri tanımlandı") 
        #customer_id = Customer.objects.filter(customer_name=form.cleaned_data.get("customer_name")).values('id')[0]['id']
        customer = Customer.objects.filter(customer_name=form.cleaned_data.get("customer_name"))
        
        ################################################### ADRES KAYDI
        #????????????????????????  formu kaydederken birinci formun çıktısı ikincinin girdisi nasıl olur?
        # müşteriyi kaydettikten sonra 

        ulke = form_adress.cleaned_data.get("ulke")
        il = form_adress.cleaned_data.get("il")
        ilce = form_adress.cleaned_data.get("ilce")
        adres = form_adress.cleaned_data.get("adres")
        map_link = form_adress.cleaned_data.get("map_link")
        customer_adres = Address(customer,il,ilce,adres,map_link)
        customer_adres.save()
        #form_adress.save()
        ###################################################
        Logla(request.user,"Müşteri Eklendi","customerAdd",customer_id,10)
        return redirect("/order/orderAdd")

    return  render(request,'customerAdd.html',{'form':form,'form_address':form_adress})


@login_required(login_url='/user/login/')
def customerAddressAdd(request,id):
    customer = Customer.objects.get(id=id)
    form = AddressForm(initial = {'customer':customer})
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/order/customerView/'+ str(id) )
    
    return render( request,'customerAddressAdd.html',{'form':form})

"""
    form_adress = AddressForm(request.POST or None,request.FILES or None)
    if form_adress.is_valid() :
        form_adress.save()
        
        return redirect("/order/orderAdd")

    return  render(request,'customerAddressAdd.html',{'form_address':form_adress})
"""


@login_required(login_url='/user/login/')
def customerAdd2(request):


    return  render(request,'customerAdd2.html')


@login_required(login_url='/user/login/')
def customerList(request):
    keyword = request.GET.get("keyword")
    if keyword:
        customers = Customer.objects.filter(username_name__contains = keyword)
        return  render(request,'customerList.html',{'customers':customers})    

    customers = Customer.objects.all()
    return  render(request,'customerList.html',{'customers':customers}) 

@login_required(login_url='/user/login')
def customerView(request,id):
    
    customer = Customer.objects.get(id=id)
    address = Address.objects.filter(customer=customer)
    orders = Order.objects.filter(customer=customer)
    if customer :
        return  render(request,'customerView.html',{'customer':customer,'address':address,'orders':orders})
        
    else:
        messages.warning(request,"müşteri bulunamadı")
        
        return redirect("/order/customerList")


@login_required(login_url='/user/login/')
def customerUpdate(request,id):
    customer = get_object_or_404(Customer,id=id)
    form = CustomerForm(request.POST or None, request.FILES or None,instance=customer)
    if form.is_valid() :
        customer = form.save(commit= False)
        customer.save()
        Logla(request.user,"Müşteri güncellendi","customerUpdate",id,10)
        messages.success(request,"müşteri bilgileri güncellendi")
        return redirect("/order/customerList")

    return  render(request,'customerUpdate.html',{'form':form})

@login_required(login_url='/user/login/')
def customerDelete(request,id):
    customer = get_object_or_404(Customer,id=id)
    customer.delete()
    Logla(request.user,"Müşteri silindi","customerDelete",id,10)
    return  redirect("/order/customerList")


############################################################################
#######################  PRODUCT           #################################
############################################################################
@login_required(login_url='/user/login/')
def productAdd(request):
    form = ProductForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        form.save()
        #TODO hata kontrolü try except
        messages.info(request," Ürün tanımlandı") 
        #TODO product_id cekilecek
        product_id = Product.objects.filter(product_name=form.cleaned_data.get("product_name")).values('id')[0]['id']
        
        Logla(request.user,"Ürün eklendi","productAdd",product_id,10)
        return redirect("/order/productList")

    return  render(request,'productAdd.html',{'form':form})

@login_required(login_url='/user/login/')
def productList(request):
    keyword = request.GET.get("keyword")
    if keyword:
        products = Product.objects.filter(product_name__contains = keyword)
        return  render(request,'productList.html',{'products':products})    

    products = Product.objects.all()
    return  render(request,'productList.html',{'products':products}) 

@login_required(login_url='/user/login/')
def productUpdate(request,id):
    product = get_object_or_404(Product,id=id)
    form = ProductForm(request.POST or None, request.FILES or None,instance=product)
    if form.is_valid() :
        product = form.save(commit= False)
        product.save()
        messages.success(request,"Ürün güncellendi")
        Logla(request.user,"Ürün güncellendi","productUpdate",id,10)
        return redirect("/order/productList")

    return  render(request,'productUpdate.html',{'form':form})

@login_required(login_url='/user/login')
def productDelete(request,id):
        product = get_object_or_404(Product,id=id)
        product.delete()
        messages.success(request,"Ürün silindi")
        Logla(request.user,"Ürün silindi","productDelete",id,10)
        return redirect("/order/productList")

############################################################################
#######################  WORKFLOW          #################################
############################################################################
@login_required(login_url='/user/login')
def workflowCompleted(request,id):
    #print("referer-----",request.META['HTTP_REFERER'])
    wf = Workflow.objects.get(id=id)
    user_id = User.objects.get(username=request.user).id
    if wf :
        wf.status = 90
        wf.completed_user_id = user_id
        wf.completed_date = datetime.datetime.now()
        wf.save()
        messages.success(request,"Görev tamamlandı")
        #TODO loglama eklenecek

    # buraya nereden geldiyse aynı sayfaya yönlendiriyoruz
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='/user/login')
def workflowView(request,id):
    
    wf = Workflow.objects.get(id=id)

    if wf :
        return  render(request,'workflow.html',{'wf':wf})
        
    else:
        messages.warning(request,"Görev bulunamadı")
        # buraya nereden geldiyse aynı sayfaya yönlendiriyoruz
        return redirect(request.META['HTTP_REFERER'])
