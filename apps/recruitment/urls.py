from django.urls import path, include
from rest_framework import routers
# from .views import FormResponsesViewset, QuestionsViewset, FormResponsesAPIView
from .views import FormResponses
router = routers.DefaultRouter()

app_name = 'recruitment'

urlpatterns = [
    path('',include(router.urls)),
    # path('questions/', QuestionsView.as_view()), 
    path('response/', FormResponses.as_view())
]