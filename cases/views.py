from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Client, Case, Lawyer
from .forms import ClientForm, LawyerForm, CaseForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CaseForm
from .models import Case
from django.forms import inlineformset_factory
from .models import Case, Document
from .forms import CaseForm, DocumentFormSet


def add_case(request):
    if request.method == 'POST':
        form = CaseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('case_list')  # Adjust the redirect as needed
    else:
        form = CaseForm()
    return render(request, 'add_case.html', {'form': form})

def edit_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if request.method == 'POST':
        form = CaseForm(request.POST, request.FILES, instance=case)
        if form.is_valid():
            form.save()
            return redirect('case_detail', case_id=case.id)  # Adjust the redirect as needed
    else:
        form = CaseForm(instance=case)
    return render(request, 'edit_case.html', {'form': form})

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients_count'] = Client.objects.count()
        context['lawyers_count'] = Lawyer.objects.count()
        context['cases_count'] = Case.objects.count()
        return context


# Client views

class ClientListView(ListView):
    model = Client
    template_name = "clients/client_list.html"


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("cases:client_list")


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("cases:client_list")


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "clients/client_confirm_delete.html"
    success_url = reverse_lazy("cases:client_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Client"
        return context


# Lawyer Views

class LawyerListView(ListView):
    model = Lawyer
    template_name = "lawyers/lawyer_list.html"


class LawyerCreateView(CreateView):
    model = Lawyer
    form_class = LawyerForm
    template_name = "lawyers/lawyer_form.html"
    success_url = "/lawyers/"


class LawyerUpdateView(UpdateView):
    model = Lawyer
    form_class = LawyerForm
    template_name = "lawyers/lawyer_form.html"
    success_url = "/lawyers/"


class LawyerDeleteView(DeleteView):
    model = Lawyer
    template_name = "lawyers/lawyer_confirm_delete.html"
    success_url = reverse_lazy("cases:lawyer_list")


class CaseListView(ListView):
    model = Case
    template_name = "cases/case_list.html"
    context_object_name = 'cases'
    paginate_by = 10  # Optional pagination

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')

        if search_query:
            return queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(status__icontains=search_query) |

                # Client related searches
                Q(client__first_name__icontains=search_query) |
                Q(client__last_name__icontains=search_query) |
                Q(client__email__icontains=search_query) |
                Q(client__phone__icontains=search_query) |

                # Lawyer related searches
                Q(lawyer__first_name__icontains=search_query) |
                Q(lawyer__last_name__icontains=search_query) |
                Q(lawyer__email__icontains=search_query) |
                Q(lawyer__phone__icontains=search_query)
            ).distinct()
        return queryset


# class CaseCreateView(CreateView):
#     model = Case
#     form_class = CaseForm
#     template_name = "cases/case_form.html"
#     success_url = "/cases/"


# def case_create(request):
#     DocumentFormSet = inlineformset_factory(
#         Case, 
#         Document, 
#         form=DocumentForm,
#         extra=3,
#         can_delete=True,
#         fields=('file',)
#     )
    
#     if request.method == 'POST':
#         form = CaseForm(request.POST)
#         formset = DocumentFormSet(request.POST, request.FILES)
        
#         if form.is_valid() and formset.is_valid():
#             case = form.save()
#             documents = formset.save(commit=False)
#             for document in documents:
#                 document.case = case
#                 document.save()
#             return redirect('cases:case_list')
def case_create(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            # Add debug print before saving
            print("Form is valid. Attempting to save...")
            try:
                case = form.save()
                print(f"Successfully saved case ID {case.id}")
                return redirect('cases:case_list')
            except Exception as e:
                print(f"Error saving case: {str(e)}")
                form.add_error(None, f"Error saving case: {str(e)}")
        else:
            # Print detailed form errors
            print("Form invalid. Errors:")
            for field, errors in form.errors.items():
                print(f"{field}: {', '.join(errors)}")
    else:
        form = CaseForm()
    
    return render(request, 'cases/case_form.html', {'form': form})
def case_documents(request, pk):
    case = get_object_or_404(Case, pk=pk)
    documents = case.documents.all()
    return render(request, 'cases/case_documents.html', {
        'case': case,
        'documents': documents
    })
# Similarly update case_update view
class CaseUpdateView(UpdateView):
    model = Case
    form_class = CaseForm
    template_name = "cases/case_form.html"
    success_url = "/cases/"


class CaseDeleteView(DeleteView):
    model = Case
    template_name = "cases/case_confirm_delete.html"
    success_url = reverse_lazy("cases:case_list")

class CaseCreateView(CreateView):
    model = Case
    form_class = CaseForm
    template_name = 'cases/case_form.html'
    success_url = reverse_lazy('cases:case_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = DocumentFormSet(self.request.POST, self.request.FILES)
        else:
            context['formset'] = DocumentFormSet()
        return context


    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)