from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    type_of_customer = models.ManyToManyField('TypeOfCustomer')

    def __str__(self):
        return self.name

class TypeOfCustomer(models.Model):
    customer_type = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.customer_type


class EmailAccount(models.Model):
    email_account = models.EmailField(max_length=200, null=True)
    email_password = models.CharField(max_length=200, null=True)
    email_host = models.CharField(max_length=200, null=True)
    email_port = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.email_account