from rest_framework import serializers
from .models import Patient, Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ('id', 'name', 'age', 'date_of_birth', 'address', 'groups', 'children', 'parent', 'health_record', 'insurance_id')

    def create(self, validated_data):
        groups_data = validated_data.pop('groups')
        children_data = validated_data.pop('children', [])
        patient = Patient.objects.create(**validated_data)
        for group_data in groups_data:
            group, created = Group.objects.get_or_create(name=group_data['name'])
            patient.groups.add(group)
        for child_data in children_data:
            child_serializer = self.__class__(data=child_data)
            child_serializer.is_valid(raise_exception=True)
            child_serializer.save(parent=patient)
        return patient

    def get_children(self, obj):
        children = obj.children.all()
        serializer = self.__class__(children, many=True)
        return serializer.data


class PatientNestedSerializer(PatientSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'name', 'age', 'address', 'groups', 'created_at')
