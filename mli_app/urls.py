from django.urls import path
from .views import *

urlpatterns = [
    path('list-patient/', PatientListCreateView.as_view(), name='user-list'),
    path('add-to-group/', AddPatientToGroupView.as_view(), name='patient-list'),
    path('patients/<int:pk>/add_child/', AddChildToPatientAPIView.as_view(), name='add_child_to_patient'),
]
