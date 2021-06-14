from django.contrib import admin
from .models import Vehicle,RootCause,ProblemStatu,OrderStatu,Reservation,ProductColor
from .models import OrderStatu,Order,Customer,Address,Workflow,ProductCategory,UrunGrubu,ProductType,Marka,Product,OrderProducts,RootCause,ProblemStatu,Problems,Vehicle,Reservation,ReservationPerson,ReservationVehicle
# Register your models here.


admin.site.register(Vehicle)
admin.site.register(RootCause)
admin.site.register(OrderStatu) 
admin.site.register(Reservation) 
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Workflow)
admin.site.register(ProductCategory)
admin.site.register(UrunGrubu)
admin.site.register(ProductType)
admin.site.register(Marka)
admin.site.register(Product)
admin.site.register(OrderProducts)
admin.site.register(ProblemStatu)
admin.site.register(Problems)
admin.site.register(ReservationPerson)
admin.site.register(ReservationVehicle)
admin.site.register(ProductColor)