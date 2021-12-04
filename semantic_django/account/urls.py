from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('person', views.PersonModelViewSet, basename="person")
router.register('organization', views.OrganizationModelViewSet,
                basename="organization")
router.register('project', views.ProjectModelViewSet, basename="project")
router.register('skill', views.SkillViewSet, basename="skill")
router.register('category', views.CategoryViewSet, basename="category")
router.register('website', views.WebsiteViewSet, basename="website")

urlpatterns = router.urls
