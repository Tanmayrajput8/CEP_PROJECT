import nested_admin  # ✅ Import nested admin
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Department, Tender, Vendor, VendorDocument, ShortfallDocument
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Role'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# ✅ Vendor Documents Inline (Nested under Vendor)
class VendorDocumentInline(nested_admin.NestedTabularInline):  # ✅ Use Nested Inline
    model = VendorDocument
    extra = 1
    fields = ('file',)


# ✅ Shortfall Documents Inline (Nested under Vendor)
class ShortfallDocumentInline(nested_admin.NestedTabularInline):  # ✅ Use Nested Inline
    model = ShortfallDocument
    extra = 1
    fields = ('shortfall_stage', 'file', 'reason')
    ordering = ['shortfall_stage']

# ✅ Vendor Inline (Now includes Documents and Shortfall)
class VendorInline(nested_admin.NestedTabularInline):  # ✅ Use Nested Inline
    model = Vendor
    extra = 1
    fields = ('name',)
    inlines = [VendorDocumentInline, ShortfallDocumentInline]  # ✅ Nest Documents under Vendors

# ✅ Tender Admin (To Show Vendors Inside Tender)
class TenderAdmin(nested_admin.NestedModelAdmin):  # ✅ Use NestedModelAdmin
    list_display = ('name', 'tender_number', 'department', 'published_date')
    list_filter = ('department',)
    search_fields = ('name', 'tender_number')
    inlines = [VendorInline]  # ✅ Now Vendors and their Documents appear inside Tenders

# ✅ Register Models
admin.site.register(Department)
admin.site.register(Tender, TenderAdmin)  # ✅ Now Vendors & Docs are inside Tender
