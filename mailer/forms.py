from django.forms import ModelForm
from mailer.models import TypeOfCustomer, Customer, EmailAccount
from django import forms
from tinymce.widgets import TinyMCE

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'type_of_customer']

    name = forms.CharField(max_length=200, required=True, label='Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=200, required=True, label='Phone', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=200, required=True, label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    type_of_customer = forms.ModelMultipleChoiceField(queryset=TypeOfCustomer.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-label'}), required=True, label='Type of Customer')


class UploadForm(forms.Form):
    file = forms.FileField(label='Upload either CSV or Excel Files (.csv or .xlsx)', widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .csv', "enctype": "multipart/form-data"}))


class EmailCustomersForm(forms.Form):
    email_from = forms.ModelChoiceField(queryset=EmailAccount.objects.all().order_by('email_account'), label='Email From', widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    type_of_customer = forms.ModelMultipleChoiceField(queryset=TypeOfCustomer.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-label'}), required=True, label='Type of Customer')
    email_subject = forms.CharField(max_length=200, required=True, label='Subject', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email_body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))


class FilterByCustomerTypeForm(forms.Form):
    type_of_customer = forms.ModelMultipleChoiceField(queryset=TypeOfCustomer.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-label'}), required=True, label='Type of Customer')


class CustomerSearchForm(forms.Form):
    search_term = forms.CharField(max_length=200, required=True, label='Search', widget=forms.TextInput(attrs={'class': 'form-control'}))
