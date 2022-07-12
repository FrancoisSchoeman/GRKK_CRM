from multiprocessing import context
from os import read
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import CustomerForm, UploadForm, EmailCustomersForm, FilterByCustomerTypeForm, CustomerSearchForm
from .models import Customer, TypeOfCustomer, EmailAccount
from django.views.generic import ListView
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages as msgs
from django.db.models import Q
import pandas as pd
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'mailer/index.html')

@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/mailer/')
    else:
        form = CustomerForm()
        context = {
            'form': form,
        }
    return render(request, 'mailer/add-customer.html', context)


@login_required
def customer_list(request):
    if request.method == 'POST':
        form = FilterByCustomerTypeForm(request.POST)
        search_form = CustomerSearchForm(request.POST)
        if form.is_valid():
            type_of_customer = form.cleaned_data['type_of_customer']
            customers = Customer.objects.filter(type_of_customer__id__in=type_of_customer)
            context = {
                'customers': customers,
                'form': form,
                'search_form': search_form,
            }
            return render(request, 'mailer/all-customers.html', context)
        if search_form.is_valid():
            search_term = search_form.cleaned_data['search_term']
            customers = Customer.objects.filter(Q(name__icontains=search_term) | Q(email__icontains=search_term) | Q(phone__icontains=search_term))
            context = {
                'customers': customers,
                'form': form,
                'search_form': search_form,
            }
            return render(request, 'mailer/all-customers.html', context)
    else:
        form = FilterByCustomerTypeForm()
        search_form = CustomerSearchForm()
    
    customers = Customer.objects.all()
    context = {
        'customers': customers,
        'form': form,
        'search_form': search_form,
    }
    return render(request, 'mailer/all-customers.html', context)


# DEFINITELY NEEDS TO BE REFACTORED
@login_required
def email_customers(request):
    if request.method == 'POST':
        form = EmailCustomersForm(request.POST)
        if form.is_valid():
            email_subject = form.cleaned_data['email_subject']
            email_body = form.cleaned_data['email_body']
            plain_message = strip_tags(email_body)
            email_from = form.cleaned_data['email_from']
            type_of_customer = form.cleaned_data['type_of_customer']

            settings.EMAIL_HOST_USER = EmailAccount.objects.get(email_account=email_from).email_account
            settings.EMAIL_HOST_PASSWORD = EmailAccount.objects.get(email_account=email_from).email_password
            settings.EMAIL_HOST = EmailAccount.objects.get(email_account=email_from).email_host
            settings.EMAIL_PORT = EmailAccount.objects.get(email_account=email_from).email_port

            email_recipients_duplicate = []
            for type in type_of_customer:
                for customer in Customer.objects.filter(type_of_customer=type):
                    email_recipients_duplicate.append(customer.email)

            email_recipients = []
            [email_recipients.append(email) for email in email_recipients_duplicate if email not in email_recipients]

            messages = [[email_subject, plain_message, email_from, email, email_body] for email in email_recipients]
            for message in messages:
                # COMMENT/UNCOMMENT TO TOGGLE EMAIL SENDING!!!
                send_mail(subject=message[0], message=message[1], from_email=message[2], recipient_list=[message[3]], html_message=message[4])
                print(message)
            msgs.add_message(request, msgs.INFO, 'Emails sent successfully.')
            return redirect('/mailer/')

    else:
        form = EmailCustomersForm()
    return render(request, 'mailer/send-mail.html', {'form': form})


@login_required
def upload_customer(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                print('Excel file detected')
                request.session['is_csv'] = False
                excel_file = pd.ExcelFile(file)
                sheets = excel_file.sheet_names
                request.session['sheets'] = sheets
                for sheet in sheets:
                    df = pd.read_excel(file, sheet_name=sheet)
                    request.session[f'sheet_{sheet}'] = df.to_json()
                return redirect('mailer:select_sheet')

            elif file.content_type == "text/csv":
                print('CSV file detected')
                data = pd.read_csv(file)
                request.session['data'] = data.to_json()
                request.session['is_csv'] = True
                return redirect('mailer:select_columns')
            msgs.add_message(request, msgs.INFO, 'File uploaded successfully.')



        else:
            msgs.add_message(request, msgs.INFO, 'File upload unsuccessful.')
            return HttpResponseRedirect('/mailer/upload-customer/')
    else:
        form = UploadForm()
    
    if request.method == 'GET':
        return render(request, 'mailer/upload-customer.html', {'form': form})


@login_required
def select_columns(request):
    types_of_customers = TypeOfCustomer.objects.all()
    if request.session['is_csv']:
        data = pd.read_json(request.session.get('data'))
    else:
        type = request.session.get('type_of_customer')
        data = pd.read_json(request.session.get(f'sheet_{type}'))

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        type_of_customer_list = request.POST.getlist('type_of_customer')

        # get ids of selected types of customers
        type_of_customer_ids = []
        for type in type_of_customer_list:
            type_of_customer_ids.append(TypeOfCustomer.objects.get(customer_type=type).id)
        
        # Loop through the dataframe and create a new customer for each row
        for index, row in data.iterrows():
            new_customer = Customer()
            new_customer.name = row[name]
            new_customer.phone = row[phone]
            new_customer.email = row[email]
            new_customer.save()
            
            for id in type_of_customer_ids:
                new_customer.type_of_customer.add(id)



        return redirect('/mailer/all-customers/')
    
    if request.method == 'GET':
        
        columns = list(data.columns)
        context = {
            'columns': columns,
            'is_csv': request.session.get('is_csv'),
            'types_of_customers': types_of_customers,
        }
        return render(request, 'mailer/select-columns.html', context)


@login_required
def select_sheet(request):
    if request.method == 'POST':
        sheet = request.POST.get('sheet-selection')
        request.session['type_of_customer'] = sheet

        return redirect('/mailer/select-columns/')
    
    if request.method == 'GET':
        sheets = request.session.get('sheets')
        return render(request, 'mailer/select-sheet.html', {"sheets": sheets})


@login_required
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('mailer:all-customers')
        
    if request.method == 'GET':
        return render(request, 'mailer/delete-customer.html', {'customer': customer})