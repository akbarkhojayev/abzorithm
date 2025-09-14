from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import token_obtain_pair , token_refresh
from main.views import *

schema_view = get_schema_view(
  openapi.Info(
     title="Snippets API",
     default_version='v1',
     description="Test description",
     terms_of_service="https://www.google.com/policies/terms/",
     contact=openapi.Contact(email="contact@snippets.local"),
     license=openapi.License(name="BSD License"),
  ),
  public=True,
  permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('token/', token_obtain_pair ),
    path('token/refresh/', token_refresh ),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
urlpatterns += [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path("users/register/", UserCreateView.as_view(), name="user-register"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("users/me/update/", UserUpdateView.as_view(), name="user-update"),
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
    path("problems/", ProblemList.as_view(), name="problem-list"),
    path("problems/<int:pk>/", ProblemDetail.as_view(), name="problem-detail"),
    path("testcases/", TestCaseList.as_view(), name="testcase-list"),
    path("submissions/", SubmissionListView.as_view(), name="submission-list"),
    path("submissions/create/", SubmissionCreateView.as_view(), name="submission-create"),
    path("submissions/template/<int:pk>/", SubmissionTemplateView.as_view(), name="submission-template"),
    path("submissions/<int:pk>/", SubmissionDetailView.as_view(), name="submission-detail"),
]