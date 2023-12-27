from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["company_name", "description", "number_of_employees"]


class CompanyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["number_of_employees"]


class UserSerializer(serializers.ModelSerializer):
    owned_companies = CompanySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "owned_companies"]
