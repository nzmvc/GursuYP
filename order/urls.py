from django.contrib import admin
from django.urls import path
from . import views

app_name="order"

urlpatterns = [
    path('dashboard/<str:departman>/<str:list_filter>', views.dashboard, name='dashboard'),
 #   path('dashboard2/', views.dashboard2, name='dashboard2'),
    
    path('orderAdd3/', views.orderAdd3, name='orderAdd3'),
    path('orderList/<str:list_filter>', views.orderList, name='orderList'),
    path('orderView/<int:id>', views.orderView, name='orderView'),
    path('orderUpdate/<int:id>', views.orderUpdate, name='orderUpdate'),
    path('orderDelete/<int:id>', views.orderDelete, name='orderDelete'),
    path('orderAddProduct/<int:id>', views.orderAddProduct, name='orderAddProduct'),
    path('orderDeleteProduct/<int:id>', views.orderDeleteProduct, name='orderDeleteProduct'),
    path('orderApproved/<int:id>', views.orderApproved, name='orderApproved'),
    path('orderAdresSecim/<str:fs>/<str:es>/<int:order_id>/<int:address_id>', views.orderAdresSecim, name='orderAdresSecim'),
    path('orderSiparisFisi/<int:id>', views.orderSiparisFisi, name='orderSiparisFisi'),
    path('dosyaEkle/<int:order_id>/<int:workflow_id>', views.dosyaEkle, name='dosyaEkle'),
    path('siparisPaketi/<int:order_id>/<int:workflow_id>', views.siparisPaketi, name='siparisPaketi'),
    path('orderPacketDelete/<int:order_product_id>', views.orderPacketDelete, name='orderPacketDelete'),
    path('orderPaketOnayla/<int:order_id>/<int:workflow_id>', views.orderPaketOnayla, name='orderPaketOnayla'),
    path('uretim_depo', views.uretim_depo, name='uretim_depo'),

    path('customerAdd/',views.customerAdd,name='customerAdd'),
    path('customerAddressAdd/<int:id>',views.customerAddressAdd,name='customerAddressAdd'),
    path('customerAddressUpdate/<int:id>',views.customerAddressUpdate,name='customerAddressUpdate'),
    path('customerAddressActivation/<int:id>',views.customerAddressActivation,name='customerAddressActivation'),
   # path('customerAdd2/',views.customerAdd2,name='customerAdd2'),
    path('customerList/',views.customerList,name='customerList'),
    path('customerView/<int:id>',views.customerView,name='customerView'),
    path('customerUpdate/<int:id>',views.customerUpdate,name='customerUpdate'),
    path('customerDelete/<int:id>',views.customerDelete,name='customerDelete'),
    
    path('productAdd/',views.productAdd,name='productAdd'),
    path('productList/',views.productList,name='productList'),
    path('productUpdate/<int:id>',views.productUpdate,name='productUpdate'),
    path('productDeactive/<int:id>',views.productDeactive,name='productDeactive'),
    path('productActive/<int:id>',views.productActive,name='productActive'),
    path('ajax/productDropList/', views.productDropList, name='ajax_productDropList'),
    path('ajax/orderDropList/', views.orderDropList, name='ajax_orderDropList'),
    path('ajax/colorList/', views.colorList, name='ajax_colorList'),
    path('ajax/categoryDropList/', views.categoryDropList, name='ajax_categoryDropList'),
    
    path('planlama/<str:list_filter>',views.planlama,name='planlama'),
    

    path('reservationList/',views.reservationList,name='reservationList'),
    path('takvim/<int:day>',views.takvim,name='takvim'),
    path('takvim_v2/',views.takvim_v2,name='takvim_v2'),
    path('events/',views.events,name='events'),
    path('events_data/',views.events_data,name='events_data'),
    path('reservationView/<int:id>',views.reservationView,name='reservationView'),
    path('reservationDelete/<int:reservation_id>',views.reservationDelete,name='reservationDelete'),

    #path('workflowCompleted/<int:id>',views.workflowCompleted,name='workflowCompleted'),
    path('workflowView/<int:id>',views.workflowView,name='workflowView'),
    path('workflowPlanla/<int:id>',views.workflowPlanla,name='workflowPlanla'),
    path('workflowStatuUpdate/<int:id>/<int:statu>',views.workflowStatuUpdate,name='workflowStatuUpdate'),
    path('yeniWorkflow/<int:workflow_id>',views.yeniWorkflow,name='yeniWorkflow'),

    path('problemAdd/<int:id>',views.problemAdd,name='problemAdd'),
    path('problemAddFull/',views.problemAddFull,name='problemAddFull'),
    path('problemList/',views.problemList,name='problemList'),
    path('problemView/<int:id>',views.problemView,name='problemView'),

    path('rapor', views.rapor, name='rapor'),
    path('data_aylik_satis',views.data_aylik_satis,name='data_aylik_satis'),
    path('data_aylik_satis_tutar',views.data_aylik_satis_tutar,name='data_aylik_satis_tutar'),

    path('test/',views.test,name='test'),
]
