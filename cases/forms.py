from django import forms
from .models import Case, Client, Lawyer
from .models import Document
from django.forms import inlineformset_factory


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)
       
# class CaseForm(forms.ModelForm):
#     class Meta:
#         model = Case
#         fields = ['title', 'description', 'status', 'client', 'lawyer', "document"]
#         # template_name = 'cases/case_form.html'

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['title', 'client', 'lawyer', 'status',  'description']

# Create the formset
# In forms.py
# DocumentFormSet = inlineformset_factory(
#     Case,
#     Document,
#     fields=('title', 'file'),  # Add title here
#     extra=1,
#     can_delete=True,
#     widgets={
#         'title': forms.TextInput(attrs={'class': 'form-control'}),
#         'file': forms.FileInput(attrs={'class': 'form-control-file'})
#     }
# )
DocumentFormSet = inlineformset_factory(
    Case,
    Document,
    fields=('title', 'file'),
    extra=1,
    can_delete=True,
    widgets={
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'file': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    }
)
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