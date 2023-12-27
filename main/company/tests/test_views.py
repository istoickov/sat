import json

from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from django.urls import reverse

from company.models import Company


class CompanyListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="test@example.com")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.company_list_url = reverse("company-list")

    def test_company_list_view_authenticated(self):
        response = self.client.get(self.company_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_company_list_view_unauthenticated(self):
        client = APIClient()
        response = client.get(self.company_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CompanyDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="test@example.com")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.company = Company.objects.create(owner=self.user, company_name="Test Company", number_of_employees=10)
        self.company_detail_url = reverse("company-detail", args=[self.company.id])

    def test_company_detail_view_authenticated(self):
        response = self.client.get(self.company_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_company_detail_view_unauthenticated(self):
        client = APIClient()
        response = client.get(self.company_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
