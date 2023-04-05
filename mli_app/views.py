from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import PatientSerializer, GroupSerializer, PatientNestedSerializer
from .models import Patient, Group


class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class AddPatientToGroupView(generics.UpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientNestedSerializer

    def update(self, request, *args, **kwargs):
        group_name = request.data.get('group_name')
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            return Response({'detail': 'Patient group not found'}, status=status.HTTP_404_NOT_FOUND)
        patient = self.get_object()
        patient.groups.add(group)
        serializer = self.get_serializer(patient)
        return Response(serializer.data)


class SearchPatientView(generics.ListAPIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q')
        queryset = Patient.objects.filter(Q(name__icontains=query) | Q(parent__name__icontains=query))
        return queryset


class AddChildToPatientAPIView(generics.UpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def update(self, request, *args, **kwargs):
        parent_id = kwargs.get('pk')
        child_id = request.data.get('child_id')

        try:
            parent = Patient.objects.get(id=parent_id)
        except Patient.DoesNotExist:
            return Response({'detail': 'Parent patient not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            child = Patient.objects.get(id=child_id)
        except Patient.DoesNotExist:
            return Response({'detail': 'Child patient not found'}, status=status.HTTP_404_NOT_FOUND)

        if child in parent.children.all():
            return Response({'detail': 'Child patient already added to parent'}, status=status.HTTP_400_BAD_REQUEST)

        parent.children.add(child)
        parent.save()

        serializer = self.get_serializer(parent)
        return Response(serializer.data)