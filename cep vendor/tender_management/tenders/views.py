from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Department, Tender, Vendor
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Vendor, VendorDocument, ShortfallDocument
from django.urls import reverse
from .forms import VendorForm, VendorDocumentForm, ShortfallDocumentForm
from django.forms import modelformset_factory
from .models import Profile

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        selected_role = request.POST.get("role")  # e.g., 'clerk' or 'hod'

        user = authenticate(request, username=username, password=password)
        if user:
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                return render(request, "tenders/login.html", {"error": "User profile not found."})

            if profile.role != selected_role:
                return render(request, "tenders/login.html", {"error": f"You are not authorized as {selected_role}."})

            login(request, user)
            request.session['role'] = selected_role

            # Redirect based on role
            if selected_role == "clerk":
                return redirect("/admin/")
            elif selected_role == "hod":
                return redirect("select_department")

        else:
            return render(request, "tenders/login.html", {"error": "Invalid username or password."})

    return render(request, "tenders/login.html")


# Logout View
def logout_view(request):
    logout(request)
    return redirect("login")

# Step 1: Select Department
@login_required
def select_department(request):
    departments = Department.objects.all()
    return render(request, "tenders/select_department.html", {"departments": departments})

# Step 2: Show Tenders for Selected Department
@login_required
def department_tenders(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    tenders = Tender.objects.filter(department=department)
    return render(request, "tenders/department_tenders.html", {"department": department, "tenders": tenders})

# Step 3: Show Tender Details
@login_required
def tender_details(request, tender_id):
    tender = get_object_or_404(Tender, id=tender_id)
    vendors = Vendor.objects.filter(tender=tender).prefetch_related('documents','shortfall_documents')
    context = {
        "tender": tender,
        "vendors": vendors,
        "shortfall_stages": [1, 2, 3],  # ✅ Pass this list to the template
    }
    
    return render(request, "tenders/tender_details.html",context)

@login_required
def shortfall_details(request, vendor_id, stage):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    shortfall_documents = vendor.shortfall_documents.filter(shortfall_stage=stage)
    
    return render(request, "tenders/shortfall_details.html", {
        "vendor": vendor,
        "shortfall_documents": shortfall_documents,
        "stage": stage,
    })
    
    
    
    
def add_vendor_to_tender(request, tender_id):
    tender = get_object_or_404(Tender, id=tender_id)

    VendorDocumentFormSet = modelformset_factory(VendorDocument, form=VendorDocumentForm, extra=1)
    ShortfallDocumentFormSet = modelformset_factory(ShortfallDocument, form=ShortfallDocumentForm, extra=1)

    if request.method == 'POST':
        vendor_form = VendorForm(request.POST)
        doc_formset = VendorDocumentFormSet(request.POST, request.FILES, queryset=VendorDocument.objects.none())
        shortfall_formset = ShortfallDocumentFormSet(request.POST, request.FILES, queryset=ShortfallDocument.objects.none())

        if vendor_form.is_valid() and doc_formset.is_valid() and shortfall_formset.is_valid():
            vendor = vendor_form.save(commit=False)
            vendor.tender = tender
            vendor.save()

            for form in doc_formset:
                if form.cleaned_data:
                    doc = form.save(commit=False)
                    doc.vendor = vendor
                    doc.save()

            for form in shortfall_formset:
                if form.cleaned_data:
                    shortfall = form.save(commit=False)
                    shortfall.vendor = vendor
                    shortfall.save()

            return redirect('clerk_tenders')  # or redirect to tender detail

    else:
        vendor_form = VendorForm()
        doc_formset = VendorDocumentFormSet(queryset=VendorDocument.objects.none())
        shortfall_formset = ShortfallDocumentFormSet(queryset=ShortfallDocument.objects.none())

    return render(request, 'add_vendor.html', {
        'tender': tender,
        'vendor_form': vendor_form,
        'doc_formset': doc_formset,
        'shortfall_formset': shortfall_formset
    })
    