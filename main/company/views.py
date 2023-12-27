import json

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes

from django.utils.html import strip_tags
from django.template.loader import render_to_string

from .models import Company
from .serializers import (
    UserSerializer,
    CompanySerializer,
    CompanyUpdateSerializer,
)

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    body = json.loads(request.body)
    username = body["username"]
    email = body["email"]
    password = body["password"]

    account = None

    try:
        if email:
            account = User.objects.get(email=email)
        elif username:
            account = User.objects.get(username=username)
    except BaseException as e:
        raise ValidationError({"400": f"{str(e)}"})

    token = Token.objects.get_or_create(user=account)[0].key

    if account and not check_password(password, account.password):
        raise ValidationError({"message": "Incorrect Login credentials"})

    if account:
        if account.is_active:
            data = {"message": "user logged in", "email_address": account.email}

            return Response({"data": data, "token": token})
        else:
            raise ValidationError({"400": "Account not active"})
    else:
        raise ValidationError({"400": "Account doesnt exist"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def User_logout(request):
    request.user.auth_token.delete()

    logout(request)

    return Response("User Logged out successfully")


class CompanyListView(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ordering = self.request.query_params.get("ordering", "company_name")

        valid_ordering_fields = ["company_name", "number_of_employees"]
        if ordering not in valid_ordering_fields:
            ordering = "name"

        queryset = Company.objects.all().order_by(ordering)
        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="ordering",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Field to use for ordering the results.",
                enum=["company_name", "number_of_employees"],
            ),
        ]
    )
    def get(self, request):
        queryset = self.get_queryset()

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = self.request.user
        if user.owned_companies.count() == 5:
            return Response({"error": "You can create up to 5 companies."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            company = serializer.save(owner=user)
            mail_sent = self.send_email(user, company)
            if mail_sent is True:
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(f"Failed to send email: {mail_sent}", status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_email(self, user, company):
        subject = "New Company Created"
        html_message = render_to_string(
            settings.EMAIL_PATH_COMPANY_CREATION,
            {"username": user.username, "company_name": company.company_name},
        )
        plain_message = strip_tags(html_message)
        try:
            send_mail(subject, plain_message, settings.EMAIL_FROM, [user.email], html_message=html_message)
            return True
        except Exception as e:
            return str(e)


class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "PATCH" or self.request.method == "PUT":
            return CompanyUpdateSerializer
        return CompanySerializer

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {"error": "You do not have permission to delete a company."}, status=status.HTTP_403_FORBIDDEN
            )

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserCompanyListView(generics.ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.owned_companies.all()


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
