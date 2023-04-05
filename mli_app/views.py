from django.db.models import Q
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .helpers import send_otp_via_email
from .serializers import PatientSerializer, PatientGroupSerializer, VerifyPatientSerializer
from .models import Patient, PatientGroup


class PatientGroupViewSet(viewsets.ModelViewSet):
    queryset = PatientGroup.objects.all()
    serializer_class = PatientGroupSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def create(self, request, *args, **kwargs):
        # Override create to handle patient's parent relationship
        parent_id = request.data.get('parent')
        if parent_id:
            parent = Patient.objects.get(id=parent_id)
            if not parent.parent:
                parent.parent = None
                parent.save()
            request.data['parent'] = parent
        return super(PatientViewSet, self).create(request, *args, **kwargs)


class PatientSearchView(generics.ListAPIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        search_param = self.request.query_params.get('q', None)

        if search_param:
            queryset = Patient.objects.filter(
                Q(name__icontains=search_param) |
                Q(insurance_id__icontains=search_param)
            )
        else:
            queryset = Patient.objects.all()

        return queryset


class AddChildView(generics.UpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def update(self, request, *args, **kwargs):
        # Get the id of the parent and the child
        parent_patient_id = kwargs.get('pk', None)
        child_patient_id = request.data.get('child_patient_id', None)

        if parent_patient_id is None:
            return Response({'detail': 'Parent patient ID is missing.'}, status=status.HTTP_400_BAD_REQUEST)

        if child_patient_id is None:
            return Response({'detail': 'Child patient ID is missing.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if both patients exists
        try:
            parent_patient = self.queryset.get(id=parent_patient_id)
        except Patient.DoesNotExist:
            return Response({'detail': 'Parent patient not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            child_patient = self.queryset.get(id=child_patient_id)
        except Patient.DoesNotExist:
            return Response({'detail': 'Child patient not found.'}, status=status.HTTP_404_NOT_FOUND)

        child_patient.parent = parent_patient
        child_patient.save()

        response_data = {
            'detail': 'Child patient added to parent patient successfully.',
            'parent_patient': PatientSerializer(parent_patient).data,
            'child_patient': PatientSerializer(child_patient).data
        }
        return Response(response_data, status=status.HTTP_200_OK)


class SignUpAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = PatientSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data['email'])
                return Response({
                    'status': 200,
                    'message': 'Sign up successfully, please check your email for OTP',
                    'data': serializer.data,
                })

            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            return Response({
                'status': 400,
                'message': f'{e}'
            })


class VerifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyPatientSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                patient = Patient.objects.get(email=email)
                if not patient.exist():
                    return Response({
                        'status': 400,
                        'message': 'something went wrong',
                        'data': 'invalid email'
                    })
                if patient.otp != otp:
                    return Response({
                        'status': 400,
                        'message': 'something went wrong',
                        'data': 'wrong otp',
                    })
                patient.is_verified = True
                patient.save()
                return Response({
                    'status': 200,
                    'message': 'account verified successfully',
                    'data': {},
                })
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            return Response({
                'status': 400,
                'message': f'something went wrong {e}',
            })
