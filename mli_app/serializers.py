from rest_framework import serializers
from .models import Patient, PatientGroup


class PatientGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientGroup
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    group = PatientGroupSerializer(read_only=True)
    parent = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Patient
        fields = ['name', 'age', 'email', 'insurance_id', 'phone_number', 'date_of_birth', 'health_record', 'group',
                  'parent']


class VerifyPatientSerializer(serializers.Serializer):
    email = serializers.EmailField()
