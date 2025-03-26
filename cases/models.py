from django.db import models


# Create your models here.

class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Lawyer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Case(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'قيد الانتظار'),
        ('OPEN', 'مفتوح'),
        ('CLOSED', 'مغلق')
    )
    COURT_CHOICES = (
        ('CAIRO_COURT', 'محكمة القاهرة'),
        ('ALEX_COURT', 'محكمة الإسكندرية'),
        ('GIZA_COURT', 'محكمة الجيزة'),
        ('LUXOR_COURT', 'محكمة الأقصر'),
        ('ASWAN_COURT', 'محكمة أسوان'),
    )
    CASE_TYPE_CHOICES = (
        ('LEGAL', 'شرعي'),
        ('CRIMINAL', 'جنائي'),
        ('CIVIL', 'مدني'),
        ('ADMIN', 'اداري'),
    )

    case_number = models.CharField(max_length=20, unique=True, blank=False, null=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    court = models.CharField(max_length=20, choices=COURT_CHOICES, default='CAIRO_COURT')
    case_type = models.CharField(max_length=20, choices=CASE_TYPE_CHOICES, default='Legal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
# Add Document model

class Document(models.Model):
    case = models.ForeignKey(
        Case, 
        on_delete=models.CASCADE,
        related_name='documents'
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/", null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title