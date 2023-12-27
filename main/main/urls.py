from django.urls import path, re_path, include

from django.contrib import admin

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions
from django.contrib.auth.decorators import permission_required


schema_view = get_schema_view(
    openapi.Info(
        title="SAT API",
        default_version="v1",
        description="SAT description",
        terms_of_service="",
        contact=openapi.Contact(email="iv.stoickov@gmail.com"),
        license=openapi.License(name="Apache License 2.0"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    re_path(r"^(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("", include("company.urls")),
    path(r"auth/", include("rest_framework.urls", namespace="rest_framework")),
]
