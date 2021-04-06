from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm,OrderForm,ProductForm,AddressForm,CustomerAddressForm,OrderProductsForm,ProblemForm,ProblemSolutionForm
from .models import Customer,Order,Workflow,Product,Address,OrderProducts,Problems,OrderStatu,Vehicle
from .models import Reservation,ReservationPerson,ReservationVehicle
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib import messages
from user.views import Logla
from user.models import Logging,Employee,Departments
from django.db.models import Q
import datetime
# Create your views here.
#TODO tum işlemler loglanmalı. hatta silem yapılmamalı yada sadece superuser yapabilsin. diğerlerinin yaptıkları inaktif edebilir.


############################################################################
#######################  DASHBOARD         #################################
############################################################################
@login_required(login_url='/user/login/')
def dashboard(request,departman="ope",list_filter="all"):
    
    order = Order.objects.all()
    customer = Customer.objects.all()
    product = Product.objects.all()
    workflow = Workflow.objects.exclude(status=90)
    problems = Problems.objects.exclude(statu=4)
    
    planlama_jobs = Workflow.objects.filter(department=41000)
    if departman =="ope":
        if list_filter == "all":
            operasyon_jobs = Workflow.objects.filter(department=44000)
        elif list_filter == "tamamlandi":
            operasyon_jobs = Workflow.objects.filter(department=44000).filter(status_id=18)
        else: 
            operasyon_jobs = Workflow.objects.filter(department=44000).exclude(status_id=18)
    else:
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
        'workflow':workflow,
        'problems':problems
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
            iskonto = form.cleaned_data.get("iskonto")
            tahmini_tarih_min = form.cleaned_data.get("tahmini_tarih_min")
            tahmini_tarih_max =form.cleaned_data.get("tahmini_tarih_max")

            new_order = Order(customer=customer,order_type=order_type,order_image=order_image,content=order_content,statu_id=23,tahmini_tarih_min=tahmini_tarih_min,tahmini_tarih_max=tahmini_tarih_max,iskonto=iskonto)
            new_order.save()
            Logla(request.user,"yeni satış işlemi girildi",log_type="order",type_id=new_order.pk,status="5")
            """
            # sipariş girişi ile beraber  departmanlara tasklar gonderilir
            #TODO test için hepsine gönderiliyor. fakat ürün ve hizmet seçimine göre task oluşmalı
            #TODO statuler değiştirilebilir yapıldı. buna bağlı olarak workflow unda parametrik yapılması gerekir. status 10 silinirse program bozulur!!!!!!
            
            0 bekleme id 1
            10 -- 2
            20 -- 6
            30 -- 11
            40 -- 15
            50 -- 19
            80 -- 21
            90 -- 22
        
            if stok == "0": # stokta ürün yoksa üretim birimine iş atanır.

                workflow_uretim = Workflow(department="42000",status_id=2,order=new_order)
                workflow_uretim.save()
                Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_uretim",type_id=workflow_uretim.pk,status="10")
            if order_type == "D":
                workflow_depoTeslim = Workflow(department="43000",status_id=19,order=new_order)
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

            """
            #TODO sipariş ıd si bilgi olarak verilebilir mi?
            messages.warning(request," Sipariş girildi. Lütfen Ürünleri ekleyiniz!!!!")   

            #TODO 

            return  redirect('/order/orderView/'+str(new_order.pk))



    return  render(request,'orderAdd.html',{'form':form})


@login_required(login_url='/user/login/')
def orderList(request,list_filter):
    #orders= Order.objects.all()
    #list_filter = request.GET.get("filter")

    print(list_filter)
    if list_filter == "active":
        orders= Order.objects.all().exclude(statu=22).order_by('create_date')
    elif list_filter == "all":
        orders= Order.objects.all().order_by('-create_date')
    elif list_filter == "musteride":
        orders= Order.objects.filter(statu=13)
    elif list_filter == "tamamlandi":
        orders= Order.objects.filter(statu=22)

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
    problems    = Problems.objects.filter(order = order)

    price_sum = sum(orderProducts.values_list('toplam_tutar', flat=True))
    t_tutar = price_sum * ((100 - order.iskonto)/100)
    
    #logs    = Logging.objects.filter(log_type="order",type_id=id)
    logs={}
    
    
    if order :
        return render(request,"orderView.html",{'order':order,'workflows':workflows,'logs':logs,'orderProducts':orderProducts,'problems':problems,'price_sum':price_sum,'t_tutar':t_tutar})
        
    else:
        messages.success(request,"Sipariş bulunamadı!!!!!!")
    return  redirect("/order/orderList")

@login_required(login_url='/user/login/')
def orderAddProduct(request,id):
    #OrderFormSet = inlineformset_factory(Customer,Order, fields('product','amount'),extra=5 )
    order = Order.objects.get(id=id)
    form = OrderProductsForm(initial={'order':order})

    if request.method == 'POST':
            
        form = OrderProductsForm(request.POST)
        if form.is_valid():

            product = form.cleaned_data.get("product")
            amount = form.cleaned_data.get("amount")
            colour = form.cleaned_data.get("colour")
            birim_fiyat = product.birim_fiyat
            toplam_tutar = birim_fiyat * amount
            
            new_orderProduct = OrderProducts(order=order,product=product,amount= amount,colour=colour,birim_fiyat=birim_fiyat,toplam_tutar=toplam_tutar)
            new_orderProduct.save()
            #form.save()
            return redirect('/order/orderView/'+ str(id) )
    
    return render( request,'orderAddProduct.html',{'form':form})
    #return render( request,'orderProductform.html',{'formset':formset})
@login_required(login_url='/user/login/')
def orderDeleteProduct(request,id):
    
    order_product = OrderProducts.objects.get(id=id)
    order_product.delete()
    
    return redirect(request.META['HTTP_REFERER'])
    #return redirect('/order/orderView/'+ str(id) )
    


@login_required(login_url='/user/login/')
def orderApproved(request,id):

    new_order = Order.objects.get(id=id)
    stok = new_order.stok
    order_type = new_order.order_type

    if stok == "0": # stokta ürün yoksa üretim birimine iş atanır.

        workflow_uretim = Workflow(department="42000",status_id=2,order=new_order)
        workflow_uretim.save()
        Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_uretim",type_id=workflow_uretim.pk,status="10")
    if order_type == "D":
        workflow_depoTeslim = Workflow(department="43000",status_id=19,order=new_order)
        workflow_depoTeslim.save()
        Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_depoTeslim",type_id=workflow_depoTeslim.pk,status="50")

    if order_type == "S":
        workflow_planlama_sevk = Workflow(department="41000",status_id=6,order=new_order)
        workflow_planlama_sevk.save()
        Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_depoTeslim",type_id=workflow_planlama_sevk.pk,status="20")

    if order_type == "M":
        workflow_planlama_sevk = Workflow(department="41000",status_id=6,order=new_order)
        workflow_planlama_montaj = Workflow(department="41000",status_id=11,order=new_order)
        workflow_montaj = Workflow(department="44000",status_id=15,order=new_order)
        workflow_planlama_sevk.save()
        workflow_planlama_montaj.save()
        workflow_montaj.save()
        Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_planlama_sevk",type_id=workflow_planlama_sevk.pk,status="20")
        Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_planlama_montaj",type_id=workflow_planlama_montaj.pk,status="30")
        Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_montaj",type_id=workflow_montaj.pk,status="40")

    # orderstatusunu değiştir.
    new_order.statu_id = 1
    new_order.save() 
    return redirect("/order/orderView/"+str(id))

############################################################################
#######################  CUSTOMER          #################################
############################################################################
@login_required(login_url='/user/login/')
def customerAdd(request):
    form = CustomerForm(request.POST or None,request.FILES or None)
    form_adress = AddressForm(request.POST or None,request.FILES or None)
    if form.is_valid() and form_adress.is_valid() :

        new_customer = form.save()
        # new_customer.pk ile formdan id alınır
        # print("********* cusotmer id", new_customer.pk)

        #TODO hata kontrolü try except
        messages.info(request," Müşteri tanımlandı") 
        
        #customer_id = Customer.objects.filter(customer_name=form.cleaned_data.get("customer_name")).values('id')[0]['id']
        customer = Customer.objects.get(customer_name=form.cleaned_data.get("customer_name"))
        
        ################################################### ADRES KAYDI
        #????????????????????????  formu kaydederken birinci formun çıktısı ikincinin girdisi nasıl olur?
        # müşteriyi kaydettikten sonra 

        ulke = form_adress.cleaned_data.get("ulke")
        il = form_adress.cleaned_data.get("il")
        ilce = form_adress.cleaned_data.get("ilce")
        adres = form_adress.cleaned_data.get("adres")
        map_link = form_adress.cleaned_data.get("map_link")
        customer_adres = Address(customer=customer,ulke=ulke,il=il,ilce=ilce,adres=adres,map_link=map_link)
        customer_adres.save()
        #form_adress.save()
        ###################################################
        Logla(request.user,"Müşteri Eklendi","customerAdd",customer.pk,10)
        return redirect(request.META['HTTP_REFERER'])

    return  render(request,'customerAdd.html',{'form':form,'form_address':form_adress})


@login_required(login_url='/user/login/')
def customerAddressAdd(request,id):
    customer = Customer.objects.get(id=id)
    form = CustomerAddressForm(initial = {'customer':customer})
    if request.method == 'POST':
        form = CustomerAddressForm(request.POST)
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
        products = Product.objects.filter(product_name__contains = keyword).filter(active=1)
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
def productDeactive(request,id):
        product = get_object_or_404(Product,id=id)
        product.active=0
        product.save()
        messages.success(request,"Ürün deaktif edildi")
        Logla(request.user,"Ürün deaktif edildi","product",id,10)
        return redirect("/order/productList")

@login_required(login_url='/user/login')
def productActive(request,id):
        product = get_object_or_404(Product,id=id)
        product.active=1
        product.save()
        messages.success(request,"Ürün Aktif edildi")
        Logla(request.user,"Ürün Aktif edildi","product",id,10)
        return redirect("/order/productList")

############################################################################
#######################  WORKFLOW          #################################
############################################################################
@login_required(login_url='/user/login')
def workflowCompleted(request,id):
    #print("referer-----",request.META['HTTP_REFERER'])
    wf = Workflow.objects.get(id=id)
    orderStatus = OrderStatu.objects.get(id=22) ## id:22 Sevk Planlandı anlamına geliyor
    user_id = User.objects.get(username=request.user).id
    if wf :
        wf.status = orderStatus
        wf.completed_user_id = user_id
        wf.completed_date = datetime.datetime.now()
        wf.save()
        messages.success(request,"Görev tamamlandı")
        #TODO loglama eklenecek

    # buraya nereden geldiyse aynı sayfaya yönlendiriyoruz
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='/user/login')
def workflowStatuUpdate(request,id,statu):
    #print("referer-----",request.META['HTTP_REFERER'])
    wf = Workflow.objects.get(id=id)

    #orderStatus = OrderStatu.objects.get(id=22) ## id:22 Sevk Planlandı anlamına geliyor
    user_id = User.objects.get(username=request.user).id
    
    #TODO loglama her bir statu için
    
    if wf :
        order = wf.order
        if statu == 13 : # Montaj için müşteriden haber bekleniyor
            wf.status_id = 13
            #wf.completed_user_id = user_id
            #wf.completed_date = datetime.datetime.now()
            order.statu_id = 13
            order.save()
            wf.save()
            messages.success(request,"statu  müşteriden haber bekleniyor olarak güncellendi")
        if statu == 14 : # Montaj planlandı
            wf.status_id = 14
            wf.completed_user_id = user_id
            wf.completed_date = datetime.datetime.now()
            order.statu_id = 14
            order.save()
            wf.save()
            messages.success(request,"Sipariş Montaj planlandı olarak güncellendi")
        
        if statu == 16 : # Montaj başladı
            wf.status_id = 16
            order.statu_id = 16   
            order.save()
            wf.save()
            messages.success(request,"Montaj başladı")

        if statu == 17 : # Montaj durdu
            wf.status_id = 17
            order.statu_id = 17
            order.save()
            wf.save()
            messages.success(request,"montaj durdu")

        if statu == 18 : # Montaj tamamlandı
            wf.status_id = 18
            wf.completed_user_id = user_id
            wf.completed_date = datetime.datetime.now()
            order.statu_id = 22     # order için tamamlandı
            order.save()
            wf.save()
            messages.success(request,"Sipariş Montaj planlandı olarak güncellendi")
        #TODO loglama eklenecek

    # buraya nereden geldiyse aynı sayfaya yönlendiriyoruz
    return redirect(request.META['HTTP_REFERER'])

class reservationItem:
    @property
    def getPerson(self):
        #print("*********** reservation ID:",reservationID)
        reservationPersons = ReservationPerson.objects.filter(reservation_id="16")
        
        for usta in reservationPersons:
            print (usta.employee.department)
        return reservationPersons


@login_required(login_url='/user/login')
def workflowView(request,id):
    
    wf = Workflow.objects.get(id=id)

    # ekrana çıkarılacaklar workflow statusune göre değişecek

    if wf :
        reservations = Reservation.objects.filter(order=wf.order)
        
        return  render(request,'workflow.html',{'wf':wf,'reservations':reservations})
        
    else:
        messages.warning(request,"Görev bulunamadı")
        # buraya nereden geldiyse aynı sayfaya yönlendiriyoruz
        return redirect(request.META['HTTP_REFERER'])

"""
id
2	10	!!!! değiştirme	Uretim planı bekleni
6	20	!!!! değiştirme	Sevk planı bekliyor
11	30	!!!! değiştirme	Montaj planı bekleniyor
"""
@login_required(login_url='/user/login')
def workflowPlanla(request,id):
    
    wf = Workflow.objects.get(id=id)
    order = Order.objects.get(id = wf.order_id)
    ustalar = request.POST.getlist('ustalar')       # ilk ve ikinci girişte  boş döner. 
    arabalar = request.POST.getlist('arabalar')
    print("==========================================")
    print(ustalar)
    print(order)

    if ustalar or arabalar:
        tarih = request.POST["tarih"]
        zaman = request.POST["zaman"]
        print("***************************************")
        print(tarih,zaman)
        # reservation tablosuna giriş yap
        res = Reservation()
        res.order = order
        res.start_date = tarih
        res.end_date = tarih
        res.description = " deneme kayıt"
        res.save()

        if ustalar:
            for usta in ustalar:
                print(usta)
                employee = Employee.objects.get(user_id = usta)
                res_person = ReservationPerson()
                res_person.employee_id = employee.id
                res_person.reservation_id = res.id
                res_person.save()


        if arabalar:
            for araba in arabalar:
                print(araba)
                res_vehicle = ReservationVehicle()
                res_vehicle.vehicle_id = araba
                res_vehicle.reservation_id = res.id
                res_vehicle.save()
        
        #todo WORKFLOW STATUSU PLANLNADI OLMALI.
        wf.status_id = 14
        wf.save()

        order.statu_id = 14
        order.save()

        return redirect("/order/dashboard/")

    else:   ########   ilk girişte burası çalışır

        if request.method == 'POST':    ############  ikinci girişte tarih seçilip planla butonuna basılınca burası çalışır
            
            tarih = request.POST["planGun"]
            zaman = request.POST["zaman"]
            print(tarih,zaman)

            # uygun araç bilgilerini alıp forma gonder
            # r = ReservationVehicle.objects.filter(reservation__start_date__gt="2021-03-24")
            # v = Vehicle.objects.filter(reservationvehicle__reservation__start_date__gt="2021-03-24")
            #Sample.objects.filter(date__range=["2011-01-01", "2011-01-31"])
            #araclar = Vehicle.objects.exclude(reservationvehicle__reservation__start_date__range=["2021-03-25", "2021-03-26"])
            
            if zaman == "oo":
                requested_start_date = tarih + " 09:00:00"
                requested_end_date = tarih + " 12:00:00"
            
            print(requested_start_date,"------",requested_end_date)
            #araclar = Vehicle.objects.exclude(reservationvehicle__reservation__start_date__range=["2021-03-28", "2021-03-28"])
            #araclar = Vehicle.objects.exclude(reservationvehicle__reservation__start_date__range=[start_date, end_date])
            #araclar = Vehicle.objects.exclude(reservationvehicle__reservation__start_date__lt=requested_end_date ,reservationvehicle__reservation__end_date__gt=requested_start_date)

            #Vehicle.objects.exclude(reservationvehicle__reservation__start_date__range=[requested_start_date, requested_end_date])
            # Rezervasyon zaman planında 3 durum kontrol edilir.

            araclar = Vehicle.objects.exclude(
                Q(reservationvehicle__reservation__start_date__range=[requested_start_date, requested_end_date]) | 
                Q(reservationvehicle__reservation__end_date__range=[requested_start_date, requested_end_date]) |
                Q(Q(reservationvehicle__reservation__end_date__gt=requested_end_date),Q(reservationvehicle__reservation__start_date__lt=requested_start_date) )
            )
            
            ustalar = Employee.objects.filter(department__startswith='4').exclude(

                Q(reservationperson__reservation__start_date__range=[requested_start_date, requested_end_date]) | 
                Q(reservationperson__reservation__end_date__range=[requested_start_date, requested_end_date]) |
                Q(Q(reservationperson__reservation__end_date__gt=requested_end_date),Q(reservationperson__reservation__start_date__lt=requested_start_date) )
            
            )

            content = {
                'order':order,
                'araclar':araclar,
                'ustalar':ustalar,
                'tarih':tarih,
                'zaman':zaman,
                'wf':wf,
            }
            return  render(request,'montaj_plan_adim2.html',content)
            
            
        else:   # ilk girişte çalışır
            if wf :
                return  render(request,'workflow.html',{'wf':wf,'order':order})
            
            else:
                messages.warning(request,"Görev bulunamadı")
                # buraya nereden geldiyse aynı sayfaya yönlendiriyoruz
                return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/user/login')
def reservationList(request):
    res = Reservation.objects.all()

    return render(request,'reservationList.html',{"reservation":res})

@login_required(login_url='/user/login')
def reservationView(request,id):
    res = Reservation.objects.get(id=id)
    res_vehicles = ReservationVehicle.objects.filter(reservation_id=id)
    res_persons = ReservationPerson.objects.filter(reservation_id=id)

    return render(request,'reservationView.html',{"res":res,"res_vehicles":res_vehicles,"res_persons":res_persons})
############################################################################
#######################  PROBLEM           #################################
############################################################################
@login_required(login_url='/user/login')
def problemAdd(request,id):

    order = Order.objects.get(id=id)
    form = ProblemForm(request.POST or None, request.FILES or None,initial={'order':order})

    #TODO statu değişikliklerinin logda tutulması süre raporlaması açısından önemli
    
    if form.is_valid():
        form.save()
        messages.info(request," Müşteri Şikayeti girildi") 
        #Logla(request.user,"Ürün eklendi","productAdd",product_id,10)
        return redirect("/order/orderView/"+str(id))

    return  render(request,'problemAdd.html',{'form':form}) 

@login_required(login_url='/user/login')
def problemList(request):
    """
    keyword = request.GET.get("keyword")
    if keyword:
        problems = Problems.objects.filter(id__contains = keyword)
        return render(request,"problemList.html",{'problems':problems})   
    """
    problems = Problems.objects.all()
    return render(request,"problemList.html",{'problems':problems})

@login_required(login_url='/user/login')
def problemView(request,id):
    problem = Problems.objects.get(id=id)
    solution_form = ProblemSolutionForm(request.POST or None, request.FILES or None,instance=problem)
    
    if solution_form.is_valid() :
        problem = solution_form.save(commit= False)
        problem.closed_date = datetime.datetime.now()
        problem.statu_id = 4
        problem.save()
        return redirect('/order/problemView/'+ str(id) )

    return render(request,"problemView.html",{'problem':problem,'solution_form':solution_form})
