from django.urls import path

from . import views

app_name = 'mailer'

urlpatterns = [
    path('', views.index, name='index'),
    path('add-customer/', views.add_customer, name='add-customer'),
    path('upload-customer/', views.upload_customer, name='upload-customer'),
    path('all-customers/', views.customer_list, name='all-customers'),
    path('send-mail/', views.email_customers, name='send-mail'),
    path('select-columns/', views.select_columns, name='select_columns'),
    path('select-sheet/', views.select_sheet, name='select_sheet'),
    path('delete-customer/<int:pk>/', views.delete_customer, name='delete-customer'),
]