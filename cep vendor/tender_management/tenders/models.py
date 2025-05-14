from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('clerk', 'Clerk'),
        ('hod', 'HOD'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    

# Model for Department
class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# Model for Tender (linked to Department)
class Tender(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    tender_number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.tender_number} - {self.name}"

# Model for Vendor (linked to Tender)
class Vendor(models.Model):
    name = models.CharField(max_length=200)
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, related_name="vendors")

    def __str__(self):
        return self.name

# VendorDocument Model (Each vendor can upload multiple documents)
class VendorDocument(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="documents")
    file = models.FileField(upload_to="vendor_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.vendor.name}"

# ShortfallDocument Model (For additional document submissions)
class ShortfallDocument(models.Model):
    SHORTFALL_CHOICES = [
        (1, 'Shortfall 1'),
        (2, 'Shortfall 2'),
        (3, 'Shortfall 3'),
    ]
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE, related_name="shortfall_documents")
    file = models.FileField(upload_to="shortfall_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, help_text="Reason for document shortfall",null=True)
    shortfall_stage = models.IntegerField(choices=SHORTFALL_CHOICES, default=1)

    def __str__(self):
        return f"Shortfall {self.get_shortfall_stage_display()} for {self.vendor.name}"
