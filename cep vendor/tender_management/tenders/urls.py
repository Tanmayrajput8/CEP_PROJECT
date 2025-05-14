from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import shortfall_details

from .views import (
    login_view, logout_view, select_department, department_tenders, 
    tender_details
)

urlpatterns = [
    path("", login_view, name="login"),  # Login Page
    path("logout/", logout_view, name="logout"),  # Logout
    path("select-department/", select_department, name="select_department"),  # Select Department
    path("department/<int:department_id>/tenders/", department_tenders, name="department_tenders"),  # Show Tenders in Dept
    path("tender/<int:tender_id>/", tender_details, name="tender_details"),  # Tender Details
    path("shortfall_details/<int:vendor_id>/<int:stage>/", shortfall_details, name="shortfall_details"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
