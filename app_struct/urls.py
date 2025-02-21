from django.urls import path
import app_struct.views


urlpatterns = [
    path('companies/', app_struct.views.companies, name='companies'),
    path('company/<int:id>/', app_struct.views.company, name='company'),
    path('company/<int:id>/subcompanies/', app_struct.views.subcompanies, name='subcompanies'),
    path('company/<int:id>/divisions/', app_struct.views.divisions, name='divisions'),
    path('company/<int:id>/division/<int:id_div>/', app_struct.views.division, name='division'),
    path('company/<int:id>/subdivisions/<int:id_div>/', app_struct.views.subdivisions, name='subdivisions'),
    # path('company/<int:id_comp>/division/<int:id_div>/', app_struct.views.divisions, name='division'),
    path('company/<int:id>/licenses/', app_struct.views.licenses, name='licenses'),
    path('company/<int:id>/license/<int:id_lic>/', app_struct.views.license, name='license'),
    path('company/<int:id>/license/<int:id_lic>/facilities/', app_struct.views.facilities, name='facilities'),
    path('company/<int:id>/license/<int:id_lic>/facility/<int:id_fc>/', app_struct.views.facility, name='facility'),
    path('company/<int:id>/license/<int:id_lic>/subfacilities/<int:id_fc>/', app_struct.views.subfacilities, name='subfacilities'),
    path('company/<int:id>/license/<int:id_lic>/projects/', app_struct.views.projects, name='projects'),
    path('company/<int:id>/license/<int:id_lic>/project/<int:id_pr>/', app_struct.views.project, name='project'),
]