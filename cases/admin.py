from django.contrib import admin
from cases.models import *
# Register your models here.

admin.site.register(Case)
admin.site.register(Lawyer)
admin.site.register(Client)

from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'case', 'category', 'uploaded_at')
    list_filter = ('category', 'uploaded_at')
    search_fields = ('title', 'description')
# change in the dashboard
