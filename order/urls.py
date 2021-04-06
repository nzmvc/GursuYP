from django.contrib import admin
from django.urls import path
from . import views

app_name="order"

urlpatterns = [
    path('dashboard/<str:departman>/<str:list_filter>', views.dashboard, name='dashboard'),
    path('dashboard2/', views.dashboard2, name='dashboard2'),
    
    path('orderAdd/', views.orderAdd, name='orderAdd'),
    path('orderList/<str:list_filter>', views.orderList, name='orderList'),
    path('orderView/<int:id>', views.orderView, name='orderView'),
    path('orderUpdate/<int:id>', views.orderUpdate, name='orderUpdate'),
    path('orderDelete/<int:id>', views.orderDelete, name='orderDelete'),
    path('orderAddProduct/<int:id>', views.orderAddProduct, name='orderAddProduct'),
    path('orderDeleteProduct/<int:id>', views.orderDeleteProduct, name='orderDeleteProduct'),
    path('orderApproved/<int:id>', views.orderApproved, name='orderApproved'),
    
    
    path('customerAdd/',views.customerAdd,name='customerAdd'),
    path('customerAddressAdd/<int:id>',views.customerAddressAdd,name='customerAddressAdd'),
    path('customerAdd2/',views.customerAdd2,name='customerAdd2'),
    path('customerList/',views.customerList,name='customerList'),
    path('customerView/<int:id>',views.customerView,name='customerView'),
    path('customerUpdate/<int:id>',views.customerUpdate,name='customerUpdate'),
    path('customerDelete/<int:id>',views.customerDelete,name='customerDelete'),
    
    path('productAdd/',views.productAdd,name='productAdd'),
    path('productList/',views.productList,name='productList'),
    path('productUpdate/<int:id>',views.productUpdate,name='productUpdate'),
    path('productDeactive/<int:id>',views.productDeactive,name='productDeactive'),
    path('productActive/<int:id>',views.productActive,name='productActive'),
    
    path('reservationList/',views.reservationList,name='reservationList'),
    path('reservationView/<int:id>',views.reservationView,name='reservationView'),

    path('workflowCompleted/<int:id>',views.workflowCompleted,name='workflowCompleted'),
    path('workflowView/<int:id>',views.workflowView,name='workflowView'),
    path('workflowPlanla/<int:id>',views.workflowPlanla,name='workflowPlanla'),
    path('workflowStatuUpdate/<int:id>/<int:statu>',views.workflowStatuUpdate,name='workflowStatuUpdate'),
    
    path('problemAdd/<int:id>',views.problemAdd,name='problemAdd'),
    path('problemList/',views.problemList,name='problemList'),
    path('problemView/<int:id>',views.problemView,name='problemView'),
]
