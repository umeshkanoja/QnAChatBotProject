from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('files', views.FileViewSet, basename='file')

urlpatterns = [
    path('query/', views.create_query, name='query'),
    path('', include(router.urls)),
]
