from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('person', views.PersonModelViewSet, basename="person")

urlpatterns = router.urls
