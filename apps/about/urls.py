
from django.urls import path, include
from .views import *
from rest_framework import routers
from .serializers import AchievementViewSet
from rest_framework import generics

router = routers.DefaultRouter()
router.register(r'achievement', AchievementViewSet)

urlpatterns = [
    path('team/', TeamApi.as_view(), name='text'),
    path('alumini/', Alumini.as_view(), name='text'),
    path('verify/', VerifyEmail.as_view(), name='text'),
    path('', include(router.urls), name='about_api'),
    path('moveTeams/', MoveTeams.as_view(), name='move'),
    path('updateTeam/<int:id>/', generics.UpdateAPIView.as_view(queryset=Team.objects.all(),
                                                                serializer_class=TeamSerializer, lookup_field='id'), name='team-update')
]
