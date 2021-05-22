from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from .forms import CustomerForm,OrderForm,ProductForm,AddressForm,CustomerAddressForm,OrderProductsForm,OrderProductsForm2,ProblemForm,ProblemSolutionForm,ProblemAddForm,OrderDosya
from .models import Customer,Order,Workflow,Product,Address,OrderProducts,Problems,OrderStatu,Vehicle,ProductCategory
from .models import Reservation,ReservationPerson,ReservationVehicle
from django.forms import inlineformset_factory
from django.forms.formsets import formset_factory
from django.contrib.auth.models import User
from django.contrib import messages
from user.views import Logla
from user.models import Logging,Employee,Departments
from django.db.models import Q
import datetime
from django.http import JsonResponse
import json
#import simplejson


from django import template

register = template.Library()

@register.filter
def days_until(date):
    delta = datetime.date(date) - datetime.now().date()
    return delta.days


############################################################################
#######################  DASHBOARD         #################################
############################################################################
@login_required(login_url='/user/login/')
def dashboard(request,departman="ope",list_filter="all"):
    
    order = Order.objects.all().exclude(statu_id=22)
    customer = Customer.objects.all()
    product = Product.objects.all()
    workflow = Workflow.objects.exclude(status_id=22).exclude(status_id=25)
    problems = Problems.objects.exclude(statu_id=4).exclude(statu_id=5)
    

    ##############################################
    today = datetime.date.today()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
   
    print("today",today)
    print("tomorrow",tomorrow)
    #res_today = Reservation.objects.filter(start_date__startswith=datetime.date.today())
    res_today = Reservation.objects.filter(start_date__year=today.year, start_date__month=today.month, start_date__day=today.day)
    print(res_today)
    res_tomorrow = Reservation.objects.filter(start_date__year=tomorrow.year, start_date__month=tomorrow.month, start_date__day=tomorrow.day)
    #res_nextweek = 
    #return render(request,'reservationList.html',{"res_today":res_today,"res_tomorrow":res_tomorrow})
    ###############################################

    #planlama_jobs = Workflow.objects.filter(department=41000)
    if departman =="ope":
        if list_filter == "all":
            operasyon_jobs = Workflow.objects.filter(department=44000)
        elif list_filter == "tamamlandi":
            operasyon_jobs = Workflow.objects.filter(department=44000).filter(status_id=18)
        else: 
            operasyon_jobs = Workflow.objects.filter(department=44000).exclude(status_id=18)
    else:
        operasyon_jobs = Workflow.objects.filter(department=44000).exclude(status_id=18)

    if departman =="plan":
        if list_filter == "all":
            planlama_jobs = Workflow.objects.filter(department=41000)
        elif list_filter == "tamamlandi":
            planlama_jobs = Workflow.objects.filter(department=41000).filter(status_id=22)
        else: 
            planlama_jobs = Workflow.objects.filter(department=41000).exclude(status_id=22).exclude(status_id=25)
    else:
        planlama_jobs = Workflow.objects.filter(department=41000).exclude(status_id=22).exclude(status_id=25)

    if departman =="uretim":
        if list_filter == "all":
            uretim_jobs = Workflow.objects.filter(department=42000)
        elif list_filter == "tamamlandi":
            uretim_jobs = Workflow.objects.filter(department=42000).filter(status_id=5)
        else: 
            uretim_jobs = Workflow.objects.filter(department=42000).exclude(status_id=5)
    else:
        uretim_jobs = Workflow.objects.filter(department=42000).exclude(status_id=5)

    if departman =="depo":
        if list_filter == "all":
            depo_jobs = Workflow.objects.filter(department=43000)
        elif list_filter == "tamamlandi":
            depo_jobs = Workflow.objects.filter(department=43000).filter(status_id=10)
        else: 
            depo_jobs = Workflow.objects.filter(department=43000).exclude(status_id=10)
    else:
        depo_jobs = Workflow.objects.filter(department=43000).exclude(status_id=10)


    #uretim_jobs = Workflow.objects.filter(department=42000)
    #depo_jobs = Workflow.objects.filter(department=43000)
    
    content = {
        'planlama_jobs':planlama_jobs,      ####
        'operasyon_jobs' : operasyon_jobs,
        'uretim_jobs':uretim_jobs,
        'depo_jobs' : depo_jobs,
        'order':order,                      ####
        'customer' :customer,
        'product':product,
        'workflow':workflow,
        'problems':problems,
        "res_today":res_today,              ####
        "res_tomorrow":res_tomorrow         ####
        }
    return  render(request,'dashboard.html',content)


@login_required(login_url='/user/login/')
def planlama(request,departman="ope",list_filter="all"):   

    workflow = Workflow.objects.exclude(status_id=22)
    order = Order.objects.all().exclude(statu_id=22)
    problems = Problems.objects.exclude(statu_id=4).exclude(statu_id=5)


    ##############################################
    today = datetime.date.today()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
   
    print("today",today)
    print("tomorrow",tomorrow)
    #res_today = Reservation.objects.filter(start_date__startswith=datetime.date.today())
    res_today = Reservation.objects.filter(start_date__year=today.year, start_date__month=today.month, start_date__day=today.day)
    print(res_today)
    res_tomorrow = Reservation.objects.filter(start_date__year=tomorrow.year, start_date__month=tomorrow.month, start_date__day=tomorrow.day)
    #res_nextweek = 
    #return render(request,'reservationList.html',{"res_today":res_today,"res_tomorrow":res_tomorrow})
    ###############################################

    if list_filter == "all":
        planlama_jobs = Workflow.objects.filter(department=41000)
    elif list_filter == "tamamlandi":
        planlama_jobs = Workflow.objects.filter(department=41000).filter(status_id=22)
    else: 
        planlama_jobs = Workflow.objects.filter(department=41000).exclude(status_id=22)

    content = {
        'planlama_jobs':planlama_jobs,      ####
        'order':order,                      ####
        "res_today":res_today,              ####
        "res_tomorrow":res_tomorrow         ####
        }

    return  render(request,'planlama.html',content)



def about(request):
    #return HttpResponse("Merhaba ana sayfa")
    return render(request,"about.html")



############################################################################
#######################  ORDER             #################################
############################################################################

@login_required(login_url='/user/login/')
@permission_required('user.siparis_yonetimi',login_url='/user/yetkiYok/')
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
  
            """

            messages.warning(request," Sipariş girildi. Lütfen Ürünleri ekleyiniz!!!!")   
            return  redirect('/order/orderView/'+str(new_order.pk))



    return  render(request,'orderAdd.html',{'form':form})

@login_required(login_url='/user/login/')
@permission_required('user.siparis_yonetimi',login_url='/user/yetkiYok/')
def orderAdd2(request):
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
            tahmini_tarih_max = form.cleaned_data.get("tahmini_tarih_max")
            satis_kanali = form.cleaned_data.get("satis_kanali")
            print(form)
            print(tahmini_tarih_min)
            new_order = Order(customer=customer,order_type=order_type,order_image=order_image,content=order_content,statu_id=23,tahmini_tarih_min=tahmini_tarih_min,tahmini_tarih_max=tahmini_tarih_max,iskonto=iskonto,satis_kanali=satis_kanali)
            new_order.save()
            Logla(request.user,"yeni satış işlemi girildi",log_type="order",type_id=new_order.pk,status="5")
            """
            # sipariş girişi ile beraber  departmanlara tasklar gonderilir
            #TODO test için hepsine gönderiliyor. fakat ürün ve hizmet seçimine göre task oluşmalı
            #TODO statuler değiştirilebilir yapıldı. buna bağlı olarak workflow unda parametrik yapılması gerekir. status 10 silinirse program bozulur!!!!!!
  
            """

            messages.warning(request," Sipariş girildi. Lütfen Ürünleri ekleyiniz!!!!")   
            return  redirect('/order/orderView/'+str(new_order.pk))

    else:
        print("form valid değil")

    return  render(request,'orderAdd2.html',{'form':form})


def findProduct(request, qs=None):
    if qs is None:
        qs = Product.objects.values_list('product_name', flat=True).all()
    if request.GET.get('urun_grubu'):
        urun_grubu=request.GET.get('urun_grubu')
        marka=request.GET.get('marka')
        print("!!!!!!!",urun_grubu)
        qs = Product.objects.values_list('product_name', flat=True).filter(urun_grubu=urun_grubu).filter(marka = marka).order_by('product_name')
    else:
        print("urun grubu bilgisi yok")
    # create an empty list to hold the results
    results = []
    
    # iterate over each city and append to results list 
    for product_name in qs:
        results.append(product_name)
    # if no results found then append a relevant message to results list
    if not results:
        # if no results then dispay empty message
        results.append(_("ürün bulunamadı")) 
    # return JSON object
    return HttpResponse(simplejson.dumps(results))


def productDropList(request):
    ug = request.GET.get('urun_grubu')
    marka = request.GET.get('marka')
    print("dddd",ug,marka)
    #products = Product.objects.values_list('product_name', flat=True).filter(urun_grubu=ug).order_by('product_name')
    products = Product.objects.all().filter(urun_grubu=ug).filter(marka=marka).order_by('product_name')
    return render(request, 'productDropList.html', {'products': products})
    

def orderDropList(request):
    """
    http://localhost:8000/order/ajax/orderDropList/?customer=26
    şeklinde liste test edilebilir.
    """
    customer = request.GET.get('customer')
    print("dddd",customer)
    orders = Order.objects.all().filter(customer_id=customer).order_by('create_date')
    return render(request, 'orderDropList.html', {'orders': orders})

@login_required(login_url='/user/login/')
def test(request):
    products = Product.objects.all()
    category = ProductCategory.objects.all()
    
    form = OrderProductsForm(request.POST or None,request.FILES or None)

    if request.method == "POST":
        print("post sonrası")

        if form.cleaned_data.get("amount"):
            print(form.cleaned_data.get("amount") )
    
    return  render(request,'test.html',{'products':products,'category':category,'form':form} )


@login_required(login_url='/user/login/')
@permission_required('user.siparis_yonetimi',login_url='/user/yetkiYok/')
def orderAdd3(request):
    form = OrderForm(request.POST or None,request.FILES or None)
    product_formset = formset_factory(OrderProductsForm,extra=10)
    
    user = User.objects.get(username=request.user)
    #sube=user.employee.sube

    if request.method == "POST":
        formset = product_formset(request.POST)

        if form.is_valid() and formset.is_valid():

                customer = form.cleaned_data.get("customer")
                order_type = form.cleaned_data.get("order_type")
                order_image = form.cleaned_data.get("order_image")
                order_content = form.cleaned_data.get("content")
                stok = form.cleaned_data.get("stok")
                iskonto = form.cleaned_data.get("iskonto")
                tahmini_tarih_min = form.cleaned_data.get("tahmini_tarih_min")
                tahmini_tarih_max = form.cleaned_data.get("tahmini_tarih_max")
                satis_kanali = form.cleaned_data.get("satis_kanali")
                planlama_sekli = form.cleaned_data.get("planlama_sekli")
    
                new_order = Order(customer=customer,order_type=order_type,order_image=order_image,content=order_content,statu_id=23,tahmini_tarih_min=tahmini_tarih_min,tahmini_tarih_max=tahmini_tarih_max,iskonto=iskonto,satis_kanali=satis_kanali,planlama_sekli=planlama_sekli,sube=user.employee.sube)
                new_order.save()
                
                Logla(request.user,"yeni satış işlemi girildi",log_type="order",type_id=new_order.pk,status="5")

                for pro_form in formset:
                    
                    if pro_form.cleaned_data.get("amount"):
                        print(pro_form.cleaned_data.get("amount") )
                        amount = pro_form.cleaned_data.get("amount")
                        urun_grubu = pro_form.cleaned_data.get("urun_grubu")
                        marka = pro_form.cleaned_data.get("marka")
                        product = pro_form.cleaned_data.get("product")
                        colour = pro_form.cleaned_data.get("colour")
                        birim_fiyat = product.birim_fiyat
                        toplam_tutar = birim_fiyat * amount

                        new_product = OrderProducts(order=new_order,product=product,amount=amount,birim_fiyat=birim_fiyat,toplam_tutar=toplam_tutar)
                        new_product.save()
             
                return  redirect('/order/orderView/'+str(new_order.pk))

        else:
            print("form valid değil")
            for er in formset.errors:
                print(er)

    return  render(request,'orderAdd3.html',{'form':form,'product_formset':product_formset})


@login_required(login_url='/user/login/')
@permission_required('user.siparis_listele',login_url='/user/yetkiYok/')
def orderList(request,list_filter):
    #orders= Order.objects.all()
    #list_filter = request.GET.get("filter")

    user = User.objects.get(username=request.user)
    sube = user.employee.sube
    dep  = user.employee.department.id

    print(list_filter)
    if dep == 1 :   #  1 finans departmanı anlamına geliyor. tüm siparişleri görebilmeli
        if list_filter == "active":
            orders= Order.objects.all().exclude(statu=22).order_by('create_date')
        elif list_filter == "all":
            orders= Order.objects.all().order_by('-create_date')
        elif list_filter == "musteride":
            orders= Order.objects.filter(statu=13)
        elif list_filter == "tamamlandi":
            orders= Order.objects.filter(statu=22)
    else:
        if list_filter == "active":
            orders= Order.objects.all().filter(sube=sube).exclude(statu=22).order_by('create_date')
        elif list_filter == "all":
            orders= Order.objects.all().filter(sube=sube).order_by('-create_date')
        elif list_filter == "musteride":
            orders= Order.objects.filter(statu=13).filter(sube=sube)
        elif list_filter == "tamamlandi":
            orders= Order.objects.filter(statu=22).filter(sube=sube)

    return  render(request,'orderList.html',{'orders':orders})


@login_required(login_url='/user/login/')
@permission_required('user.siparis_yonetimi',login_url='/user/yetkiYok/')
def orderUpdate(request,id):
    order = get_object_or_404(Order,id=id)
    form = OrderForm(request.POST or None, request.FILES or None,instance=order)
    if form.is_valid() :
        order = form.save(commit= False)
        order.save()
        messages.success(request,"sipariş bilgileri güncellendi")
        Logla(request.user,"sipariş güncellendi","orderUpdate",order.id,10)
        return redirect("/order/orderList/active")
    return  render(request,'orderUpdate.html',{'form':form})

@login_required(login_url='/user/login/')
def dosyaEkle(request,order_id,workflow_id):
    order = get_object_or_404(Order,id=order_id)
    form = OrderDosya(request.POST or None, request.FILES or None,instance=order)
    if form.is_valid() :
        
        form.save()
        messages.success(request,"Dosya Eklendi")
        Logla(request.user,"sipariş güncellendi","dosyaEkle",order.id,10)

        wf = Workflow.objects.get(id=workflow_id)
        wf.status_id = 25
        wf.save()

        return redirect("/order/dashboard/ope/active")
    return  render(request,'dosyaEkle.html',{'form':form})

@login_required(login_url='/user/login/')
@permission_required('user.siparis_yonetimi',login_url='/user/yetkiYok/')
def orderDelete(request,id):
    order = get_object_or_404(Order,id=id)
    if order :
        order.delete()
        Logla(request.user,"sipariş silindi","orderDelete",id,10)
        
        messages.success(request,"Sipariş silindi")
    else:
        messages.success(request,"Sipariş bulunamadı!!!!!!")
    return  redirect("/order/orderList/active")

@login_required(login_url='/user/login/')
@permission_required('user.siparis_yonetimi',login_url='/user/yetkiYok/')
def orderView(request,id):
    form    = OrderProductsForm()
    order   = get_object_or_404(Order,id=id)
    
    workflows = Workflow.objects.filter(order_id=id)
    orderProducts = OrderProducts.objects.filter(order =order)
    problems    = Problems.objects.filter(order = order)
    adresler =  Address.objects.filter(customer = order.customer) 
    fatura_adres = Address.objects.filter(id = order.fatura_adres)
    sevk_adres = Address.objects.filter(id = order.sevk_adres) 
    price_sum = sum(orderProducts.values_list('toplam_tutar', flat=True))
    t_tutar = price_sum * ((100 - order.iskonto)/100)
    
    #logs    = Logging.objects.filter(log_type="order",type_id=id)
    logs={}
    
    content ={'form':form, 'order':order,'workflows':workflows,
                'logs':logs,'orderProducts':orderProducts,'problems':problems,
                'price_sum':price_sum,'t_tutar':t_tutar,'fatura_adres':fatura_adres,'sevk_adres':sevk_adres,'adresler':adresler}
    
    if order :
        return render(request,"orderView.html",content)
        
    else:
        messages.success(request,"Sipariş bulunamadı!!!!!!")
    #return  redirect("/order/orderList")

@login_required(login_url='/user/login/')
@permission_required('user.siparis_yonetimi',login_url='/user/yetkiYok/')
def orderSiparisFisi(request,id):
    order = get_object_or_404(Order,id=id)
    orderProducts = OrderProducts.objects.filter(order =order)
    fatura_adres = Address.objects.filter(id = order.fatura_adres) 
    sevk_adres = Address.objects.filter(id = order.sevk_adres)  
    price_sum = sum(orderProducts.values_list('toplam_tutar', flat=True))
    t_tutar = price_sum * ((100 - order.iskonto)/100)
    #print(orderProducts.count())
    if order :
        return render(request,"orderSiparis2.html",{'order':order,'orderProducts':orderProducts,'price_sum':price_sum,'t_tutar':t_tutar,'fatura_adres':fatura_adres,'sevk_adres':sevk_adres,'range':range(15-orderProducts.count())})
        
    else:
        messages.success(request,"Sipariş bulunamadı!!!!!!")
    return  redirect("/order/orderList")

@login_required(login_url='/user/login/')
def orderAddProduct(request,id):
    #OrderFormSet = inlineformset_factory(Customer,Order, fields('product','amount'),extra=5 )
    order = Order.objects.get(id=id)
    #form = OrderProductsForm2(initial={'order':order})

    form = OrderProductsForm(initial={'order':order})
    
    # coklu ekleme için bunu kullanacağız
    #product_formset = formset_factory(OrderProductsForm,extra=10)

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
    #return render( request,'orderProductform.html',{'formset':formset}

@login_required(login_url='/user/login/')
@permission_required('user.siparis_yonetimi',login_url='/user/yetkiYok/')
def orderDeleteProduct(request,id):
    
    order_product = OrderProducts.objects.get(id=id)
    order_product.delete()
    
    return redirect(request.META['HTTP_REFERER'])
    #return redirect('/order/orderView/'+ str(id) )
    
@login_required(login_url='/user/login/')
def orderAdresSecim(request,fs,es,order_id,address_id):
    # fs : fatura / sevk
    # es : ekle / sil
    order = Order.objects.get(id=order_id)
   
    if fs == "fatura":
        if es == "ekle":
            order.fatura_adres = address_id
        else:
            order.fatura_adres = 0
            #order.fatura_adres.remove()
    else:                                       # sevk adres işlemleri için buraya gelir
        if es == "ekle":
            order.sevk_adres = address_id
        else:
            order.sevk_adres = 0
    
    order.save()

    return redirect(request.META['HTTP_REFERER'])     



@login_required(login_url='/user/login/')
@permission_required('user.siparis_yonetimi',login_url='/user/yetkiYok/')
def orderApproved(request,id):

    new_order = Order.objects.get(id=id)
    if new_order.sevk_adres and new_order.fatura_adres:
        stok = new_order.stok
        order_type = new_order.order_type

        #urungrubu 1 celikkapı , 2 ic kpaı, 3 zemin
        #eğer ic kapı ise planlama ekibine is akışı oluşturulur.
        orderProductType = OrderProducts.objects.filter(product__urun_grubu=2).filter(order_id =id)

        if not new_order.order_image and orderProductType.count() > 0 :
            workflow_planlama_olcumDosyasi = Workflow(department="41000",status_id=24,order=new_order,comment="Ölçüm dosyası işlemi")
            workflow_planlama_olcumDosyasi.save()

        if stok == "0": # stokta ürün yoksa üretim birimine iş atanır.

            workflow_uretim = Workflow(department="42000",status_id=2,order=new_order,comment="Üretim yapılacak")
            workflow_uretim.save()
            Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_uretim",type_id=workflow_uretim.pk,status="10")
        if order_type == "D":
            workflow_depoTeslim = Workflow(department="43000",status_id=19,order=new_order,comment="Depo teslimi")
            workflow_depoTeslim.save()
            Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_depoTeslim",type_id=workflow_depoTeslim.pk,status="50")

        if order_type == "S":
            workflow_planlama_sevk = Workflow(department="41000",status_id=6,order=new_order,comment="Sevk Planlama")
            workflow_planlama_sevk.save()
            Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_depoTeslim",type_id=workflow_planlama_sevk.pk,status="20")

        if order_type == "M":
            #montajlı işte sevk planına gerek olmadığı için kaldırıldı
            #workflow_planlama_sevk = Workflow(department="41000",status_id=6,order=new_order,comment="Sevk Planlama")
            workflow_planlama_montaj = Workflow(department="41000",status_id=11,order=new_order,comment="Montaj Planlama")
            workflow_montaj = Workflow(department="44000",status_id=15,order=new_order,comment="Montaj işlemi")
            #workflow_planlama_sevk.save()
            workflow_planlama_montaj.save()
            workflow_montaj.save()
            #Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_planlama_sevk",type_id=workflow_planlama_sevk.pk,status="20")
            Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_planlama_montaj",type_id=workflow_planlama_montaj.pk,status="30")
            Logla(request.user,"yeni satış işlemi girildi",log_type="workflow_montaj",type_id=workflow_montaj.pk,status="40")

        # orderstatusunu değiştir.
        new_order.statu_id = 1
        new_order.save() 
    else:
        messages.warning(request," Adres seçimi yapılmamış") 
    return redirect("/order/orderView/"+str(id))

############################################################################
#######################  CUSTOMER          #################################
############################################################################
@login_required(login_url='/user/login/')
@permission_required('user.musteri_yonetim',login_url='/user/yetkiYok/')
def customerAdd(request):
    print(request.META['HTTP_REFERER'])
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
        mahalle = form_adress.cleaned_data.get("mahalle")
        map_link = form_adress.cleaned_data.get("map_link")
        customer_adres = Address(customer=customer,ulke=ulke,il=il,ilce=ilce,adres=adres,map_link=map_link,mahalle=mahalle)
        customer_adres.save()
        #form_adress.save()
        ###################################################
        Logla(request.user,"Müşteri Eklendi","customerAdd",customer.pk,10)
        return redirect(request.META['HTTP_REFERER'])
        

    return  render(request,'customerAdd.html',{'form':form,'form_address':form_adress})


@login_required(login_url='/user/login/')
@permission_required('user.musteri_yonetimi',login_url='/user/yetkiYok/')
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
'''

@login_required(login_url='/user/login/')
def customerAdd2(request):
    return  render(request,'customerAdd2.html')
'''

@login_required(login_url='/user/login/')
@permission_required('user.musteri_listele',login_url='/user/yetkiYok/')
def customerList(request):
    keyword = request.GET.get("keyword")
    if keyword:
        customers = Customer.objects.filter(username_name__contains = keyword)
        return  render(request,'customerList.html',{'customers':customers})    

    customers = Customer.objects.all()
    return  render(request,'customerList.html',{'customers':customers}) 

@login_required(login_url='/user/login')
@permission_required('user.musteri_yonetimi',login_url='/user/yetkiYok/')
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
@permission_required('user.musteri_yonetimi',login_url='/user/yetkiYok/')
def customerAddressUpdate(request,id):
    address = get_object_or_404(Address,id=id)
    form = CustomerAddressForm(request.POST or None, request.FILES or None,instance=address)
    if form.is_valid() :
        customerAddress = form.save(commit= False)
        customerAddress.save()
        Logla(request.user,"Müşteri adresi güncellendi","customerAddressUpdate",id,10)
        messages.success(request,"müşteri bilgileri güncellendi")
        return redirect('/order/customerView/'+ str(address.customer.id) )

    return  render(request,'customerAddressUpdate.html',{'form':form})

@login_required(login_url='/user/login/')
@permission_required('user.musteri_yonetimi',login_url='/user/yetkiYok/')
def customerAddressActivation(request,id):
    
    address = get_object_or_404(Address,id=id)
    address.activate = False

    if address.active:            # adress aktfi ise deaktif edilir
        address.active = False    
    else:                           # adress deaktif ise aktif edilir
        address.active = True

    address.save()
    Logla(request.user,"Müşteri adresi deaktif edildi","customerAddressUpdate",id,10)

    return redirect(request.META['HTTP_REFERER'])   # geldiği sayfaya önüş yapması için


@login_required(login_url='/user/login/')
@permission_required('user.musteri_yonetimi',login_url='/user/yetkiYok/')
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
@permission_required('user.musteri_yonetimi',login_url='/user/yetkiYok/')
def customerDelete(request,id):
    customer = get_object_or_404(Customer,id=id)
    customer.delete()
    Logla(request.user,"Müşteri silindi","customerDelete",id,10)
    return  redirect("/order/customerList")


############################################################################
#######################  PRODUCT           #################################
############################################################################
@login_required(login_url='/user/login/')
@permission_required('user.urun_yonetim',login_url='/user/yetkiYok/')
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
@permission_required('user.urun_listele',login_url='/user/yetkiYok/')
def productList(request):
    keyword = request.GET.get("keyword")
    if keyword:
        products = Product.objects.filter(product_name__contains = keyword).filter(active=1)
        return  render(request,'productList.html',{'products':products})    

    products = Product.objects.all()
    return  render(request,'productList.html',{'products':products}) 

@login_required(login_url='/user/login/')
@permission_required('user.urun_yonetim',login_url='/user/yetkiYok/')
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
@permission_required('user.urun_yonetim',login_url='/user/yetkiYok/')
def productDeactive(request,id):
        product = get_object_or_404(Product,id=id)
        product.active=0
        product.save()
        messages.success(request,"Ürün deaktif edildi")
        Logla(request.user,"Ürün deaktif edildi","product",id,10)
        return redirect("/order/productList")

@login_required(login_url='/user/login')
@permission_required('user.urun_yonetim',login_url='/user/yetkiYok/')
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
@permission_required('user.urun_yonetim',login_url='/user/yetkiYok/')
def workflowCompleted(request,id):
    #print("referer-----",request.META['HTTP_REFERER'])
    wf = Workflow.objects.get(id=id)
    #orderStatus = OrderStatu.objects.get(id=22) ## id:22 Sevk Planlandı anlamına geliyor
    user_id = User.objects.get(username=request.user).id
    if wf :
        print(wf.department)
        if wf.department == "40000":   #operasyon
            wf.status_id = 18
        elif wf.department == "41000":     #planlama
            wf.status_id = 22
        elif wf.department == "42000":     #uretim
            wf.status_id = 5
        elif wf.department == "43000":     #depo
            wf.status_id = 10
            print("status güncelendi")


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
    
    if ustalar or arabalar:
        tarih = request.POST["tarih"]
        tarih_end = request.POST["tarih_end"]
        stime = request.POST["stime"]
        etime = request.POST["etime"]
        #print("***************************************")
        #print(tarih,stime,etime)
        # reservation tablosuna giriş yap
        res = Reservation()
        res.order = order
        res.start_date = tarih + " " + stime
        res.end_date = tarih_end+ " " + etime
        res.description = " deneme kayıt"    #TODO: descriptpon güncellenmeli
        res.urun_grubu_id = 1               #TODO: ürün grubu neye göre girlecek ??????
        res.save()

        if ustalar:
            for usta in ustalar:
                #print(usta)
                employee = Employee.objects.get(user_id = usta)
                res_person = ReservationPerson()
                res_person.employee_id = employee.id
                res_person.reservation_id = res.id
                res_person.save()


        if arabalar:
            for araba in arabalar:
                #print(araba)
                res_vehicle = ReservationVehicle()
                res_vehicle.vehicle_id = araba
                res_vehicle.reservation_id = res.id
                res_vehicle.save()
        
        #todo WORKFLOW STATUSU PLANLNADI OLMALI.
        wf.status_id = 14
        wf.save()

        order.statu_id = 14
        order.save()

        return redirect("/order/dashboard/ope/all")

    else:   ########   ilk girişte burası çalışır

        if request.method == 'POST':    ############  ikinci girişte tarih seçilip planla butonuna basılınca burası çalışır
            
            tarih = request.POST["planGun"]
            tarih_end = request.POST["planGun_end"]
            stime = request.POST["stime"]
            etime = request.POST["etime"]
            print(tarih,stime,etime)

            # uygun araç bilgilerini alıp forma gonder
            # r = ReservationVehicle.objects.filter(reservation__start_date__gt="2021-03-24")
            # v = Vehicle.objects.filter(reservationvehicle__reservation__start_date__gt="2021-03-24")
            #Sample.objects.filter(date__range=["2011-01-01", "2011-01-31"])
            #araclar = Vehicle.objects.exclude(reservationvehicle__reservation__start_date__range=["2021-03-25", "2021-03-26"])
            
            '''
            if zaman == "oo":
                requested_start_date = tarih + " 09:00:00"
                requested_end_date = tarih + " 12:00:00"
            '''
            requested_start_date = tarih +" "+ stime
            requested_end_date = tarih_end +" "+ etime

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
            
            ustalar = Employee.objects.filter(department__department_number__startswith='31').exclude(

                Q(reservationperson__reservation__start_date__range=[requested_start_date, requested_end_date]) | 
                Q(reservationperson__reservation__end_date__range=[requested_start_date, requested_end_date]) |
                Q(Q(reservationperson__reservation__end_date__gt=requested_end_date),Q(reservationperson__reservation__start_date__lt=requested_start_date) )
            
            )

            content = {
                'order':order,
                'araclar':araclar,
                'ustalar':ustalar,
                'tarih':tarih,
                'tarih_end':tarih_end,
                'stime':stime,
                'etime':etime,
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
def takvim(request,day):
    #today = datetime.date.today()
    #tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    gunler=[]
    reservations=[]
    gunler.append(datetime.date.today())
    
    for i in range(1,day):
        gunler.append( datetime.date.today() + datetime.timedelta(days=i))

    for i in range(day):
        print( gunler[i])
        reservations.append ( Reservation.objects.filter(start_date__year=gunler[i].year, start_date__month=gunler[i].month, start_date__day=gunler[i].day) )

    #res_today = Reservation.objects.filter(start_date__startswith=datetime.date.today())
    #res_today = Reservation.objects.filter(start_date__year=today.year, start_date__month=today.month, start_date__day=today.day)
    #print(res_today)
    #res_tomorrow = Reservation.objects.filter(start_date__year=tomorrow.year, start_date__month=tomorrow.month, start_date__day=tomorrow.day)
    #res_nextweek = 
    return render(request,'takvim.html',{"gunler":gunler,"reservations":reservations})

@login_required(login_url='/user/login')
def events(request):
   
    return render(request,'events.html')

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

@login_required(login_url='/user/login')
def events_data(request):
    
    events_arr =[]
    res = Reservation.objects.all()
    
    
    for d in res:
        #print(d.order.customer.customer_name)
        
        start_date = datetime.datetime.strftime(d.start_date, '%Y-%m-%d %H:%M')
        end_date = datetime.datetime.strftime(d.end_date, '%Y-%m-%d %H:%M')
        events_arr.append( { 'id':d.order_id,'title': d.order.customer.customer_name , 'start': start_date,'end': end_date })
    
    print(events_arr)

    #events_arr = [ {'title': 'All Day Event','start': '2020-09-01'},{'title': 'kurulum','start': '2020-09-01 10:00:00','end':'2020-09-01 12:00:00'}, {'title': 'Long Event','start': '2020-09-07','end': '2020-09-10'} ]
    
    #y = json.dumps(events_arr ,indent=4)    # array i json formatına donusturduk
    y = json.dumps(events_arr ,sort_keys=True,  indent=1,  default=default)    # array i json formatına donusturduk

    serialized= json.dumps(events_arr, sort_keys=True, indent=3)   # array i json formatına donusturduk


    """
    json to array
    jsonStr = '[{"a":1, "b":2}, {"c":3, "d":4}]'
    aList = json.loads(jsonStr)
    print(aList[0]['b'])

    """
    return HttpResponse(serialized)
    #return HttpResponse(events_arr)


@login_required(login_url='/user/login')
def reservationList(request):
    today = datetime.date.today()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
   
    print("today",today)
    print("tomorrow",tomorrow)
    #res_today = Reservation.objects.filter(start_date__startswith=datetime.date.today())
    res_today = Reservation.objects.filter(start_date__year=today.year, start_date__month=today.month, start_date__day=today.day)
    print(res_today)
    res_tomorrow = Reservation.objects.filter(start_date__year=tomorrow.year, start_date__month=tomorrow.month, start_date__day=tomorrow.day)
    #res_nextweek = 
    return render(request,'reservationList.html',{"res_today":res_today,"res_tomorrow":res_tomorrow})

@login_required(login_url='/user/login')
def reservationView(request,id):
    res = Reservation.objects.get(id=id)
    res_vehicles = ReservationVehicle.objects.filter(reservation_id=id)
    res_persons = ReservationPerson.objects.filter(reservation_id=id)

    return render(request,'reservationView.html',{"res":res,"res_vehicles":res_vehicles,"res_persons":res_persons})

@login_required(login_url='/user/login')
def reservationDelete(request,id):
    res = Reservation.objects.get(id=id)
    res.delete()

    return redirect(request.META['HTTP_REFERER'])

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

@login_required(login_url="/user/login")
def problemAddFull(request):
    customers = Customer.objects.all()
    form = ProblemAddForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        messages.info(request," Müşteri Şikayeti girildi") 
        #Logla(request.user,"Ürün eklendi","productAdd",product_id,10)
        return redirect("/order/problemList")
    return render(request,"problemAddFull.html",{'customers':customers,'form':form})

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

############################################################################
#######################  PROBLEM           #################################
############################################################################
@login_required(login_url='/user/login')
def rapor(request):
    

    return render(request,"rapor.html")