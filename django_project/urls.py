from django.conf import settings
from django.contrib import admin
from django.urls import (
    include,
    path,
)
from rest_framework import routers

from accounts import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("accounts.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include("pages.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
