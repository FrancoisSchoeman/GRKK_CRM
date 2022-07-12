from django.contrib import admin
from .models import Customer, TypeOfCustomer, EmailAccount

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'date_created']
    list_filter = ['date_created', 'type_of_customer']
    search_fields = ['name', 'phone', 'email']

class TypeOfCustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_type']
    list_filter = ['customer_type']
    search_fields = ['customer_type']

class EmailAccountAdmin(admin.ModelAdmin):
    list_display = ['email_account', 'email_password', 'email_host', 'email_port']
    list_filter = ['email_account', 'email_host', 'email_port']
    search_fields = ['email_account', 'email_host', 'email_port']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(TypeOfCustomer, TypeOfCustomerAdmin)
admin.site.register(EmailAccount, EmailAccountAdmin)
