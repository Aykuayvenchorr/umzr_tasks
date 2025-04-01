from django.urls import path
import app_struct.views


urlpatterns = [
    path('companies/', app_struct.views.companies, name='companies'),
    path('company/<int:id>/', app_struct.views.company, name='company'),
    path('company/<int:id>/save/', app_struct.views.company_save, name='company_save'),
    path('company/<int:id>/subcompanies/', app_struct.views.subcompanies, name='subcompanies'),

    path('company/<int:id>/divisions/', app_struct.views.divisions, name='divisions'),
    path('company/<int:id>/division/<int:id_div>/', app_struct.views.division, name='division'),
    path('company/<int:id>/subdivisions/<int:id_div>/', app_struct.views.subdivisions, name='subdivisions'),
    path('company/<int:id>/division/<int:id_div>/projects/', app_struct.views.division_projects, name='division_projects'),
    path('company/<int:id>/division/<int:id_div>/save/', app_struct.views.save_div, name='save_div'),

    path('company/<int:id>/licenses/', app_struct.views.licenses, name='licenses'),
    path('license/<int:id>/', app_struct.views.license, name='license'),
    path('company/<int:id>/license/<int:id_lic>/save/', app_struct.views.license_save, name='license_save'),
    path('company/<int:id>/license/<int:id_lic>/facilities/', app_struct.views.license_facilities, name='license_facilities'),
    path('company/<int:id>/license/<int:id_lic>/projects/', app_struct.views.license_projects, name='license_projects'),
    path('company/<int:id>/license/<int:id_lic>/facility/<int:id_fc>/save/', app_struct.views.save_facility, name='save_facility'),

    path('company/<int:id>/license/<int:id_lic>/facility/<int:id_fc>/', app_struct.views.facility, name='facility'),
    path('company/<int:id>/license/<int:id_lic>/subfacilities/<int:id_fc>/', app_struct.views.subfacilities, name='subfacilities'),
]
