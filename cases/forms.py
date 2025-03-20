from django import forms
from .models import Case, Client, Lawyer, CaseDocument
from django.forms.widgets import ClearableFileInput

# class CaseForm(forms.ModelForm):
#     class Meta:
#         model = Case
#         fields = ['title', 'description', 'status', 'client', 'lawyer', "document"]
#         # template_name = 'cases/case_form.html'


# class CaseDocumentMultiForm(forms.Form):
#     files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['title', 'description']


class CaseDocumentForm(forms.Form):
    documents = forms.FileField(
        widget=ClearableFileInput(attrs={'multiple': True}),
        required=False
    )


# class CaseDocumentForm(forms.Form):
#     files = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False)


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone']
        # template_name = 'clients/client_form.html'


class LawyerForm(forms.ModelForm):
    class Meta:
        model = Lawyer
        fields = ['first_name', 'last_name', 'email', 'phone']
        # template_name = 'lawyers/lawyer_form.html'
