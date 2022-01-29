from django.urls import path, include
from rest_framework import routers
# from .views import FormResponsesViewset, QuestionsViewset, FormResponsesAPIView
from .views import FormResponses, FormResponsesApi, RetrieveResponseApi
router = routers.DefaultRouter()

app_name = 'recruitment'

urlpatterns = [
    path('', include(router.urls)),
    # path('questions/', QuestionsView.as_view()),
    path('response/', FormResponsesApi.as_view()),
    path('retrieve/', RetrieveResponseApi.as_view())
]
