from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_v3.views import ArticleViewSet

app_name = "api_v3"

router = DefaultRouter()
router.register("articles", ArticleViewSet)

urlpatterns = [
    path("", include(router.urls))
]
