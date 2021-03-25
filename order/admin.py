from django.contrib import admin
from .models import Vehicle,RootCause,ProblemStatu,OrderStatu,Reservation

# Register your models here.


admin.site.register(Vehicle)
admin.site.register(RootCause)
admin.site.register(OrderStatu) 
admin.site.register(Reservation) 