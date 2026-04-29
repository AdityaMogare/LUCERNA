from django.urls import include, path
from rest_framework.routers import DefaultRouter

from contracts.views import ContractViewSet, DashboardView, DeadlineViewSet, HealthView

router = DefaultRouter()
router.register(r"contracts", ContractViewSet, basename="contract")
router.register(r"deadlines", DeadlineViewSet, basename="deadline")

urlpatterns = [
    path("health/", HealthView.as_view()),
    path("dashboard/", DashboardView.as_view()),
    path("", include(router.urls)),
]
