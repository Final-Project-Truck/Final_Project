from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from analytics.views import generate_report

schema_view = get_schema_view(
    openapi.Info(
        title="The_Truck_Project",
        default_version='v1',
        description="Make a Survey",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="theman198888@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),

    #    path('', home, name="home"),
    path('api/v1/', include([
        router.urls,
        'baseuser.urls',
        'company.urls',
        'survey.urls',
        'chat.urls',
    ])),
    path('admin/', admin.site.urls),
    path('api/v1/report/', generate_report, name='report'),

]
