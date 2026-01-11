from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [

    path("admin/", admin.site.urls),
    path("estimations/", include("apps.estimations.urls")), 
    path("submits/", include("apps.submits.urls")),
    path("", include("apps.users.urls")), 
]
