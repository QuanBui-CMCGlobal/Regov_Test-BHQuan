from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'groups', PatientGroupViewSet)
router.register(r'patients', PatientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('patient-search/', PatientSearchView.as_view(), name='patient-search'),
    path('patient/<int:pk>/add-child/', AddChildView.as_view(), name='patient-search'),
    path('sign-up/', SignUpAPI.as_view(), name='sign-up'),
    path('verify/', VerifyOTP.as_view(), name='verify'),
]
