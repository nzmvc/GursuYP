from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from .forms import CustomerForm,OrderForm,ProductForm,AddressForm,CustomerAddressForm,OrderProductsForm,OrderProductsForm2,ProblemForm,ProblemSolutionForm,ProblemAddForm,OrderDosya
from .models import Customer,Order,Workflow,Product,Address,OrderProducts,Problems,OrderStatu,Vehicle,ProductCategory
from .models import Reservation,ReservationPerson,ReservationVehicle,OrderPackets,ProductColor
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
    
    labels = ["Fethiye","Muğla","Marmaris","Bodrum"]
    data = [150,65,110,90]

    user = User.objects.get(username=request.user)
    print(user.id , user.employee.id)
    order = Order.objects.all().exclude(statu_id=22)
    customer = Customer.objects.all()
    product = Product.objects.all()     
    
    # 22 > tamamlandı. 25 >olcumdosyası girildi 14>montaj planlandı
    workflow = Workflow.objects.exclude(status_id__in= (22,25,27,14))
    problems = Problems.objects.exclude(statu_id=4).exclude(statu_id=5)
    islerim = Reservation.objects.filter(id__in = ReservationPerson.objects.values_list('id',flat=True).filter(employee=user.employee))

    ##############################################
    today = datetime.date.today()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    res_today = Reservation.objects.filter(start_date__year=today.year, start_date__month=today.month, start_date__day=today.day)
    res_tomorrow = Reservation.objects.filter(start_date__year=tomorrow.year, start_date__month=tomorrow.month, start_date__day=tomorrow.day)

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
            planlama_jobs = Workflow.objects.filter(department=41000).filter(status_id__in=(22,25,27,14) )  # statusu tamamladı olanların workflow ID leri 
        else: 
            planlama_jobs = Workflow.objects.filter(department=41000).exclude(status_id__in= (22,25,27,14))        
    else:
        planlama_jobs = Workflow.objects.filter(department=41000).exclude(status_id__in= (22,25,27,14))

    
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
        "res_tomorrow":res_tomorrow,        ####
        'labels': labels,
        'data': data,
        'islerim':islerim,
        }
    return  render(request,'dashboard.html',content)


@login_required(login_url='/user/login/')
def planlama(request,departman="ope",list_filter="all"):   
    
    order = Order.objects.all().exclude(statu_id=22)
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

    planned_jobs = Workflow.objects.filter(status_id__in=(3,7,14) )  # planlanmış işler

    if list_filter == "all":
        planlama_jobs = Workflow.objects.filter(department=41000)
    elif list_filter == "tamamlandi":
        planlama_jobs = Workflow.objects.filter(department=41000).filter(status_id__in=(22,25,27,14) )  # statusu tamamladı olanların workflow ID leri 
    else: # active durumunda bu çalışır
        planlama_jobs = Workflow.objects.filter(department=41000).exclude(status_id__in= (22,25,27,14))
        

    content = {
        'planlama_jobs':planlama_jobs,      ####
        'order':order,                      ####
        "res_today":res_today,              ####
        "res_tomorrow":res_tomorrow         ####
        }

    return  render(request,'planlama.html',content)



def about(request):
    
    return render(request,"about.html")



############################################################################
#######################  ORDER             #################################
############################################################################

def categoryDropList(request):
    ug = request.GET.get('urun_grubu')
    kategoriler = ProductCategory.objects.filter(id__in = Product.objects.values_list('product_category_id',flat=True).filter(urun_grubu=ug).distinct() )

    http_data ="<option value="">---------</option>"
    for kt in kategoriler:
        http_data = http_data + "<option value="+  str(kt.id) +" title ="+kt.title +">"+kt.title+"</option>"

    print(http_data)
    return HttpResponse(http_data)

def productDropList(request):
    ug = request.GET.get('urun_grubu')
    kategori = request.GET.get('kategori')
    products = Product.objects.all().filter(urun_grubu=ug).filter(product_category=kategori).order_by('product_name')
    return render(request, 'productDropList.html', {'products': products})


def colorList(request):
    product_id = request.GET.get('product_id')
    """
    http://localhost:8000/order/ajax/colorList/?product_id=1
    şeklinde liste test edilebilir.
    """
    colors = ProductColor.objects.filter(product_category_id__in= Product.objects.values_list('product_category_id',flat=True).filter(id=product_id) )
    return render(request, 'colorList.html', {'colors': colors}) 

def orderDropList(request):
    """
    http://localhost:8000/order/ajax/orderDropList/?customer=26
    şeklinde liste test edilebilir.
    """
    customer = request.GET.get('customer')
    #print("dddd",customer)
    orders = Order.objects.all().filter(customer_id=customer).order_by('create_date')
    return render(request, 'orderDropList.html', {'orders': orders})



@login_required(login_url='/user/login/')
def test(request):
    products = Product.objects.all()
    category = ProductCategory.objects.all()
    
    form = OrderProductsForm(request.POST or None,request.FILES or None)

    if request.method == "POST":
       # print("post sonrası")

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
                order_image = form.cleaned_data.get("order_image")
                order_content = form.cleaned_data.get("content")
                iskonto = form.cleaned_data.get("iskonto")
                tahmini_tarih_min = form.cleaned_data.get("tahmini_tarih_min")
                tahmini_tarih_max = form.cleaned_data.get("tahmini_tarih_max")
                planlama_sekli = form.cleaned_data.get("planlama_sekli")
    
                new_order = Order(customer=customer,order_image=order_image,content=order_content,statu_id=23,tahmini_tarih_min=tahmini_tarih_min,tahmini_tarih_max=tahmini_tarih_max,iskonto=iskonto,planlama_sekli=planlama_sekli,sube=user.employee.sube)
                new_order.save()
                
                Logla(request.user,"order","yeni satış işlemi girildi",new_order.pk,"start")

                for pro_form in formset:
                    
                    if pro_form.cleaned_data.get("amount"):
                        print(pro_form.cleaned_data.get("amount") )
                        amount = pro_form.cleaned_data.get("amount")
                        colour = pro_form.cleaned_data.get("colour")
                                                
                        product = Product.objects.get( id = pro_form.cleaned_data.get("product"))
                        birim_fiyat = product.birim_fiyat
                        toplam_tutar = birim_fiyat * amount
                        
                        new_product = OrderProducts(order=new_order,product=product,amount=amount,birim_fiyat=birim_fiyat,toplam_tutar=toplam_tutar,colour=colour,orderpackets_id = 0)
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
def dosyaEkle(request,order_id,workflow_id):  #olcumDosyası girilir
    order = get_object_or_404(Order,id=order_id)
    form = OrderDosya(request.POST or None, request.FILES or None,instance=order)
    if form.is_valid() :
        
        form.save()
        messages.success(request,"Dosya Eklendi")
    
        
        wf = Workflow.objects.get(id=workflow_id)
        wf.status_id = 25       ## workflow güncellenerek işlem tamamlandı statusune çekilir.
        wf.save()
        Logla(request.user,"workflow","ölcüm dosyası eklendi",wf.id,"end")

        order.save()

        workflow_uretim = Workflow(department="42000",status_id=2,order_id=order_id,comment="Üretim yapılacak")
        workflow_uretim.save()
        
        order.save()

        return redirect("/order/dashboard/ope/active")
    return  render(request,'dosyaEkle.html',{'form':form})


@login_required(login_url='/user/login/')
def siparisPaketi(request,order_id,workflow_id): #alt paket altpaket ilk sayfa
    order = get_object_or_404(Order,id=order_id)
    products = OrderProducts.objects.filter(order_id = order_id).filter( orderpackets_id = 0)
    products_selected = OrderProducts.objects.filter(order_id = order_id).exclude( orderpackets_id = 0)

    if request.method == "POST":
        # orderpacket e kayıt girilir.
        opack = OrderPackets(order_type= request.POST.getlist('order_type')[0], status = 0,uretim=request.POST.get('uretim'))
        opack.save()  
        """  many to many için 
        # yeni kayda bağlanacak productlar  for ile eklenir
        for i in request.POST.getlist('to'):
            print ("---", i , request.POST.getlist('order_type')[0] )
            oproduct = OrderProducts.objects.get(id =i)
            opack.order_product.add( oproduct )         #!!!! manyto many relation da bu şekilde kayıt yapıyoruz.
        """
        for i in request.POST.getlist('to'):
            #print ("---", i , request.POST.getlist('order_type')[0] )
            oproduct = OrderProducts.objects.get(id =i)
            oproduct.orderpackets_id = opack.id         # oluşturulan paket id si orderproducts içindeki ilgili satıra eklenir.
            oproduct.order_id = order_id
            oproduct.save()
        

    return render(request,'siparisPaketi.html',{'products':products,'products_selected':products_selected,'order':order,'workflow_id':workflow_id})


@login_required(login_url='/user/login/')
@permission_required('user.siparis_yonetimi',login_url='/user/yetkiYok/')
def orderPacketDelete(request,order_product_id):
    #product = OrderProducts.objects.filter(id = order_product_id)
    product= get_object_or_404(OrderProducts,id=order_product_id)
    print(product.orderpackets)
    product.orderpackets_id = 0
    product.save()

    return redirect(request.META['HTTP_REFERER'])



@login_required(login_url='/user/login/')
@permission_required('user.siparis_yonetimi',login_url='/user/yetkiYok/')
def orderPaketOnayla(request,order_id,workflow_id): #alt paket altpaket onay buton
    # siperiş kaydı onaylandı anlamına gelen  sipariş_paketi = True yapılır.
    # bu onaylama sonrasında sip paketleri silinemez yada yeniden paket oluşturulamaz. paketleme sayfasında sil ve paketle butonları gözükmez
    new_order = get_object_or_404(Order,id=order_id)
    new_order.siparis_paketi = True
    

    # planlama ekibine sipariş paketlemesi için açılan akış tamamlandı statusune alınır.
    wf = get_object_or_404(Workflow,id=workflow_id)
    wf.status_id = 27
    wf.completed_date = datetime.datetime.now()
    wf.save()

    # urungrubu 1 celikkapı , 2 ic kapı, 3 zemin    #####
    # eğer ic kapı ise (urungrubu 2) planlama ekibine ölcüm dosyası girilmesi için  is akışı oluşturulur.
    orderProductType = OrderProducts.objects.filter(product__urun_grubu=2).filter(order_id =order_id)
    if not new_order.order_image and orderProductType.count() > 0 :
        workflow_planlama_olcumDosyasi = Workflow(department="41000",status_id=24,order=new_order,comment="Ölçüm dosyası işlemi")
        workflow_planlama_olcumDosyasi.save()
        
    ##################################################

    # order id bilgisine göre sipariş paket id ve tipi bilgisi alınır.
    oPacks = OrderPackets.objects.filter(id__in= OrderProducts.objects.filter(order_id=order_id).values_list('orderpackets', flat=True) )

    for sip_pack in oPacks :
        # order a ait tüm sipariş paketleri için  order type a göre iş akışları üretilir.
        # 4 ürün vardır ama 2 paket olarak tanımlanmış olabilir. bu durumda 1 order ın 4 ürünü için tanımlanmış 2 paket için, 2 workflow oluşur.
        print(sip_pack.id , " sipariş paketi içn ilem yapılıyor. sip tipi", sip_pack.order_type)
        
        if sip_pack.order_type == "U" or sip_pack.uretim == True:  # Uretim ekibine iş akışı gider 
            #TODO su an uretim planlandı olarak akış başlatılıyor.
            # daha sonra üretim planlama modulu çalışılacak
            workflow_uretim = Workflow(department="42000",status_id=3,order=new_order,comment="Üretim yapılacak",siparis_paketi_id=sip_pack.id)
            workflow_uretim.save()
            
            Logla(request.user,"workflow","workflow_uretim olusturuldu",workflow_uretim.id,"start")
        if sip_pack.order_type == "D":
            workflow_depoTeslim = Workflow(department="43000",status_id=19,order=new_order,comment="Depo teslimi",siparis_paketi_id=sip_pack.id)
            workflow_depoTeslim.save()
            
            Logla(request.user,"workflow","workflow_depoteslim olusturuldu",workflow_depoTeslim.id,"start")

        if sip_pack.order_type == "S":
            workflow_planlama_sevk = Workflow(department="41000",status_id=6,order=new_order,comment="Sevk Planlama",siparis_paketi_id=sip_pack.id)
            workflow_planlama_sevk.save()
            
            Logla(request.user,"workflow","workflow_planlama_sevk olusturuldu",workflow_planlama_sevk.id,"start")

        if sip_pack.order_type == "M":
            
            workflow_planlama_montaj = Workflow(department="41000",status_id=11,order=new_order,comment="Montaj Planlama",siparis_paketi_id=sip_pack.id)
            workflow_montaj = Workflow(department="44000",status_id=15,order=new_order,comment="Montaj işlemi",siparis_paketi_id=sip_pack.id)
            
            workflow_planlama_montaj.save()
            workflow_montaj.save()
            
            
            Logla(request.user,"workflow","workflow_planlama_montaj olusturuldu",workflow_planlama_montaj.id,"start")
            Logla(request.user,"workflow","workflow_montaj olusturuldu",workflow_montaj.id,"start")
        
        new_order.save()
    return redirect("/order/dashboard/ope/active")


@login_required(login_url='/user/login/')
@permission_required('user.siparis_yonetimi',login_url='/user/yetkiYok/')
def orderDelete(request,id):
    order = get_object_or_404(Order,id=id)
    if order :
        order.delete()
        Logla(request.user,"order","orderDelete",id,"end")
        
        messages.success(request,"Sipariş silindi")
    else:
        messages.success(request,"Sipariş bulunamadı!!!!!!")
    return  redirect("/order/orderList/active")


@login_required(login_url='/user/login/')
#@permission_required('user.siparis_yonetimi',login_url='/user/yetkiYok/')
def orderView(request,id):
    form    = OrderProductsForm()
    order   = get_object_or_404(Order,id=id)
    user = User.objects.get(username=request.user)

    workflows = Workflow.objects.filter(order_id=id)
    orderProducts = OrderProducts.objects.filter(order =order).order_by('orderpackets_id')
    problems    = Problems.objects.filter(order = order)
    adresler =  Address.objects.filter(customer = order.customer) 
    fatura_adres = Address.objects.filter(id = order.fatura_adres)
    sevk_adres = Address.objects.filter(id = order.sevk_adres) 
    price_sum = sum(orderProducts.values_list('toplam_tutar', flat=True))
    t_tutar = price_sum * ((100 - order.iskonto)/100)
    reservations = Reservation.objects.filter(order = order)
    wf_closed = Workflow.objects.filter(order=order).filter(completed_date__isnull=False)
    if ( workflows.count() > 0 ):
        tamamlanma_oranı = int ( wf_closed.count() / workflows.count() * 100 )
    else:
        tamamlanma_oranı = 0
    logs={}
    
    content ={'form':form, 'order':order,'workflows':workflows,'tamamlanma_oranı':tamamlanma_oranı,'reservations':reservations,
                'logs':logs,'orderProducts':orderProducts,'problems':problems,
                'price_sum':price_sum,'t_tutar':t_tutar,'fatura_adres':fatura_adres,'sevk_adres':sevk_adres,'adresler':adresler}
    
    if order :  ##### kullanıcı yetkisine göre farklı sayfalara yönlendirilir

        if user.has_perm('siparis_yonetimi') :
            return render(request,"orderView.html",content)
        else:
            return render(request,"orderView_usta.html",content)
    else:
        messages.success(request,"Sipariş bulunamadı!!!!!!")



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

            
            product = Product.objects.get( id = form.cleaned_data.get("product"))
            amount = form.cleaned_data.get("amount")
            colour = form.cleaned_data.get("colour")
            birim_fiyat = product.birim_fiyat
            toplam_tutar = birim_fiyat * amount
            
            # ilk order da orderpaket boş ise ilk kayıt oluşturulur.
            opid = OrderPackets.objects.get(id=0)
            if opid is None :
                new_opid = OrderPackets(id=0)
                new_opid.save()
            
            new_orderProduct = OrderProducts(order=order,product=product,amount= amount,colour=colour,birim_fiyat=birim_fiyat,toplam_tutar=toplam_tutar,orderpackets_id = 0)
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
        #stok = new_order.stok
        #order_type = new_order.order_type
        
        # sureç değişikliği. sipariş paketleri oluşturulacak
        # TODO tek ürün olması durumunda sip paketi oluşturulmayabilir. yada otomatik oluşturulabilir.
        workflow_planlama_sipPaketi = Workflow(department="41000",status_id=26,order=new_order,comment="Sipariş paketlerini oluştur")
        workflow_planlama_sipPaketi.save()
        
        Logla(request.user,"workflow","workflow_planlama_sipPaketi olusturuldu",workflow_planlama_sipPaketi.id,"start")
        
        # orderstatusunu değiştir.
        new_order.statu_id = 1
        new_order.save() 
        Logla(request.user,"order","sipariş onaylandı",id,"approved")  #,siparis_paketi_id=sip_pack.id
           
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
        #customer = Customer.objects.get(customer_name=form.cleaned_data.get("customer_name"))
        
        ################################################### ADRES KAYDI
 
        ulke = form_adress.cleaned_data.get("ulke")
        il = form_adress.cleaned_data.get("il")
        ilce = form_adress.cleaned_data.get("ilce")
        adres = form_adress.cleaned_data.get("adres")
        mahalle = form_adress.cleaned_data.get("mahalle")
        map_link = form_adress.cleaned_data.get("map_link")
        #customer_adres = Address(customer=customer,ulke=ulke,il=il,ilce=ilce,adres=adres,map_link=map_link,mahalle=mahalle)
        customer_adres = Address(customer=new_customer,ulke=ulke,il=il,ilce=ilce,adres=adres,map_link=map_link,mahalle=mahalle)
        customer_adres.save()
        #form_adress.save()
        ###################################################
        Logla(request.user,"Müşteri Eklendi","customerAdd",new_customer.pk,10)
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
@permission_required('user.musteri_listele',login_url='/user/yetkiYok/')
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
        product = form.save()
        #TODO hata kontrolü try except
        messages.info(request," Ürün tanımlandı") 
        #product_id = Product.objects.filter(product_name=form.cleaned_data.get("product_name")).values('id')[0]['id']
        
        Logla(request.user,"Ürün eklendi","productAdd",product.pk,10)
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
#@permission_required('user.workflow_islem',login_url='/user/yetkiYok/')
def workflowCompleted(request,id):
    #print("referer-----",request.META['HTTP_REFERER'])
    wf = Workflow.objects.get(id=id)
    #orderStatus = OrderStatu.objects.get(id=22) ## id:22 Sevk Planlandı anlamına geliyor
    user_id = User.objects.get(username=request.user).id
    if wf :
        print(wf.department)
        if wf.department == "40000":        #operasyon
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

        Logla(request.user,"workflow","workflow tamamlandı",wf.id,"end")
        orderCompleteControl(request,wf.order)


    # buraya nereden geldiyse aynı sayfaya yönlendiriyoruz
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='/user/login')
def orderCompleteControl(request,order):
    #TODO sorgu çalıştırılacak. order a bağlı wf lardan end date girilmemiş  var mı?
    blank_end_date = Workflow.objects.filter(order=order).filter(completed_date__isnull=True)
    print(" tamamlanmamış wf sayısı" +  str( blank_end_date.count()) )
    if blank_end_date.count() == 0:  # tum akışlar tamamlanmış anlamına gelir. 
        order.status_id = 22   # tamamlandı statusu güncellendi
        order.completed_date = datetime.datetime.now() # order ın tamamlanma tarihi girildi.
        order.save()
        Logla(request.user,"order","order tamamlandı",order.id,"end")
        messages.success(request,"Order tamamlandı.")
        #TODO müşteri geri arama taskı oluşturulabilir.

@login_required(login_url='/user/login')
def workflowStatuUpdate(request,id,statu):
 
    wf = Workflow.objects.get(id=id)
    user_id = User.objects.get(username=request.user).id
    
    if wf :
        order = wf.order
        if statu == 4 : # üretime başlandı
            wf.status_id = 4
            order.statu_id = 4
            order.save()
            wf.save()
            messages.success(request,"statu  üretime başlandı olarak güncellendi")
            Logla(request.user,"workflow","wf id:"+str (wf.id)+" uretim başladı",wf.id,statu)

        if statu == 5 : # üretim tamamlandı
            wf.status_id = 5
            wf.completed_user_id = user_id
            wf.completed_date = datetime.datetime.now()
            order.statu_id = 5
            order.save()
            wf.save()
            messages.success(request,"statu  üretim tamamlandı olarak güncellendi")
            Logla(request.user,"workflow","wf id:"+str (wf.id)+" uretim tamamlandı",wf.id,"end")
            orderCompleteControl(request,order)

        if statu == 13 : # Montaj için müşteriden haber bekleniyor
            wf.status_id = 13
            order.statu_id = 13
            order.save()
            wf.save()
            messages.success(request,"statu  müşteriden haber bekleniyor olarak güncellendi")
            Logla(request.user,"workflow","wf id:"+str (wf.id)+" Montaj için müşteriden haber bekleniyor",wf.id,statu)

        if statu == 14 : # Montaj planlandı
            wf.status_id = 14
            wf.completed_user_id = user_id
            wf.completed_date = datetime.datetime.now()
            order.statu_id = 14
            order.save()
            wf.save()
            messages.success(request,"Sipariş Montaj planlandı olarak güncellendi")
            Logla(request.user,"workflow","wf id:"+str (wf.id)+" montaj planlandı",wf.id,"end")
            orderCompleteControl(request,order)

        if statu == 16 : # Montaj başladı
            wf.status_id = 16
            order.statu_id = 16   
            order.save()
            wf.save()
            messages.success(request,"Montaj başladı")
            Logla(request.user,"workflow","wf id:"+str (wf.id)+" montaj basladı",wf.id,statu)

        if statu == 17 : # Montaj durdu
            wf.status_id = 17
            order.statu_id = 17
            order.save()
            wf.save()
            messages.success(request,"montaj durdu")
            Logla(request.user,"workflow","wf id:"+str (wf.id)+" montaj durdu",wf.id,statu)

        if statu == 18 : # Montaj tamamlandı
            wf.status_id = 18
            wf.completed_user_id = user_id
            wf.completed_date = datetime.datetime.now()
            order.statu_id = 22     # order için tamamlandı
            order.save()
            wf.save()
            messages.success(request,"Sipariş Montaj planlandı olarak güncellendi")
            Logla(request.user,"workflow","wf id:"+str (wf.id)+" montaj tamamlandı",wf.id,"end")
            orderCompleteControl(request,order)

        #########  tüm değişiklik statuleri loglanır. bir il veya order ile iligli işlemlerin hepsi görüntülenebilir.
        
        

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

@login_required(login_url='/user/login')
def workflowPlanla(request,id):
    
    wf = Workflow.objects.get(id=id)
    order = Order.objects.get(id = wf.order_id)
    ustalar = request.POST.getlist('ustalar')       # ilk ve ikinci girişte  boş döner. 
    arabalar = request.POST.getlist('arabalar')
    orderproducts = OrderProducts.objects.filter(orderpackets_id = wf.siparis_paketi_id)
    print(orderproducts)

    if ustalar or arabalar:
        tarih = request.POST["tarih"]
        tarih_end = request.POST["tarih_end"]
        stime = request.POST["stime"]
        etime = request.POST["etime"]

        res = Reservation()
        res.order = order
        res.workflow = wf
        res.order_packet = wf.siparis_paketi
        res.start_date = tarih + " " + stime
        res.end_date = tarih_end+ " " + etime
        res.description = " deneme kayıt"    #TODO: descriptpon güncellenmeli
        res.urun_grubu_id = 1               #TODO: ürün grubu neye göre girlecek ??????
        #TODO: tablodaki versiyon degeri default 1. güncelleme yapılacaksa bu arttırılmalı  
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
        
        # WORKFLOW STATUSU PLANLNADI OLMALI.
        # workflow  statusuna göre tipi belirlenerek güncelleme yapılır
        # 2 üretim , 6 sevk , 11 montaj 
        if wf.status_id == 11 or wf.status_id == 13:
            wf.status_id = 14
            order.statu_id = 14
            Logla(request.user,"workflow","wf montaj id:"+str(wf.id)+" planlandı",wf.id,"end")
        elif wf.status_id == 6:
            wf.status_id = 7
            order.statu_id = 7
            Logla(request.user,"workflow","wf sevk id:"+str(wf.id)+" planlandı",wf.id,"end")
        elif wf.status_id == 2:
            wf.status_id = 3
            order.statu_id = 3
            Logla(request.user,"workflow","wf uretim id:"+str(wf.id)+" planlandı",wf.id,"end")
        
        wf.completed_date = datetime.datetime.now()
        wf.save()
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

            requested_start_date = tarih +" "+ stime
            requested_end_date = tarih_end +" "+ etime

            araclar = Vehicle.objects.exclude(
                Q(reservationvehicle__reservation__start_date__range=[requested_start_date, requested_end_date]) | 
                Q(reservationvehicle__reservation__end_date__range=[requested_start_date, requested_end_date]) |
                Q(Q(reservationvehicle__reservation__end_date__gt=requested_end_date),Q(reservationvehicle__reservation__start_date__lt=requested_start_date) )
            )
            
            ustalar = Employee.objects.filter(department__department_number__startswith='31').exclude(
                # ustanın rezervasyon aralıgı , planlanan tarih aralıgına dokunursa listelenmez.
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
                'orderproducts':orderproducts,
            }
            return  render(request,'montaj_plan_adim2.html',content)
            
            
        else:   # ilk girişte çalışır
            if wf :
                return  render(request,'workflow.html',{'wf':wf,'order':order,'orderproducts':orderproducts})
            
            else:
                messages.warning(request,"Görev bulunamadı")
                # buraya nereden geldiyse aynı sayfaya yönlendiriyoruz
                return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/user/login')
def takvim(request,day):

    gunler=[]
    reservations=[]
    gunler.append(datetime.date.today())
    
    for i in range(1,day):
        gunler.append( datetime.date.today() + datetime.timedelta(days=i))

    for i in range(day):
        print( gunler[i])
        reservations.append ( Reservation.objects.filter(start_date__year=gunler[i].year, start_date__month=gunler[i].month, start_date__day=gunler[i].day) )

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
        start_date = datetime.datetime.strftime(d.start_date, '%Y-%m-%d %H:%M')
        end_date = datetime.datetime.strftime(d.end_date, '%Y-%m-%d %H:%M')
        ustalar_id = ReservationPerson.objects.filter(reservation = d)
        ustalar=""
        description = d.order.customer.customer_name +"__"+d.order.content+"__"+d.order.planlama_sekli
        for usta in ustalar_id:
            ustalar  = ustalar + "\nUsta: " + usta.employee.user.username 
        events_arr.append( { 'id':d.order_id,'title': d.order.customer.customer_name + ustalar , 'start': start_date,'end': end_date,'description':description })
    
    #y = json.dumps(events_arr ,sort_keys=True,  indent=1,  default=default)    # array i json formatına donusturduk
    serialized= json.dumps(events_arr, sort_keys=True, indent=3)   # array i json formatına donusturduk
    return HttpResponse(serialized)

@login_required(login_url='/user/login')
def reservationList(request):
    today = datetime.date.today()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    res_today = Reservation.objects.filter(start_date__year=today.year, start_date__month=today.month, start_date__day=today.day)
    #print(res_today)
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
def reservationDelete(request,reservation_id):

    #TODO işlem yapılmışsa silinmemeli!!!! kontrol düşün

    res = Reservation.objects.get(id=reservation_id)
    
    # workflow güncelleme yapılmalı
    wf = res.workflow

    if wf.status_id == 14:   # montaj planlandı statusunde ise 
        wf.status_id = 11   # bunu montaj planla statusune çekiyoruz.
    elif wf.status_id == 7:   # sevk planlandı statusunde ise 
        wf.status_id = 6   # sevk  planla statusune çekiyoruz.
    
    res.delete()    # rezervasyon silinir
    wf.save()       # workflow güncellenir.

    return redirect(request.META['HTTP_REFERER'])

############################################################################
#######################  PROBLEM           #################################
############################################################################
@login_required(login_url='/user/login')
def problemAdd(request,id):

    order = Order.objects.get(id=id)
    user = User.objects.get(username=request.user)
    form = ProblemForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
       
        if form.is_valid() :
            description = form.cleaned_data.get("description")
            problem_file = form.cleaned_data.get("problem_file")
            print(problem_file)

            problem = Problems(order = order, created_user =user,description = description, problem_file = problem_file)
            problem.save()
            return redirect("/order/dashboard/ope/all")

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
#######################  RAPOR           #################################
############################################################################
@login_required(login_url='/user/login')
def rapor(request):
    
    labels = ["Fethiye","Muğla","Marmaris","Bodrum"]
    data = [150,65,110,90]


    # datalar elle oluşturuldu bunlar veri tabanından alınacak

    '''
    queryset = City.objects.order_by('-population')[:5]
    for city in queryset:
        labels.append(city.name)
        data.append(city.population)
    '''
    return render(request, 'rapor.html', {
        'labels': labels,
        'data': data,
    })

@login_required(login_url='/user/login')
def data_aylik_satis(request):
    labels=[]
    data=[]
    
    labels = ["Ocak","Şubat","Mart","Nisan","Mayıs"]
    data = [45,65,110,90,159]
    
    # datalar elle oluşturuldu bunlar veri tabanından alınacak
    '''
    queryset = City.objects.values('country__name').annotate(country_population=Sum('population')).order_by('-country_population')
    for entry in queryset:
        labels.append(entry['country__name'])
        data.append(entry['country_population'])
    '''
    # veriler json olarak gonderiliyor html içinden
    return JsonResponse(data={'labels':labels,'data':data})

############################################################################
#######################             #################################
############################################################################
@login_required(login_url='/user/login')
def uretim_depo (request):

    uretim_planlandi = Workflow.objects.filter(status_id__in = (2,3))
    uretimde= Workflow.objects.filter(status_id = 4 )
    diger = Workflow.objects.filter(status_id__in = (7,8,19))

    content ={"uretim_planlandi_jobs":uretim_planlandi, "uretimde_jobs":uretimde,"diger_jobs":diger}

    return render(request, 'uretim_depo.html', content )