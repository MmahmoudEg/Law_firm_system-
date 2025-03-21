from django import forms
from .models import Case, Client, Lawyer
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)
       
class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['title', 'description', 'status', 'client', 'lawyer', "document"]
        # template_name = 'cases/case_form.html'


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