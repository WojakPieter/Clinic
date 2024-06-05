from rest_framework import serializers

from .models import *

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name')

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('login', 'role')
    def get_role(self, obj):
        return RoleSerializer(obj.role).data

class NoteSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()
    class Meta:
        model = Note
        fields = ('content', 'patient', 'doctor', 'creation_date')
    def get_patient(self, obj):
        return UserSerializer(obj.patient).data
    def get_doctor(self, obj):
        return UserSerializer(obj.doctor).data
