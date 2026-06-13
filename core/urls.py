from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
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

# API Routes (under /api/ prefix)
api_patterns = [
    path("users/register/", UserCreateView.as_view(), name="user-register"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("users/me/", CurrentUserView.as_view(), name="current-user"),
    path("users/me/update/", UserUpdateView.as_view(), name="user-update"),
    path("users/me/stats/", UserProfileStatsView.as_view(), name="user-profile-stats"),
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
    path("problems/", ProblemList.as_view(), name="problem-list"),
    path("problems/<slug:slug>/", ProblemDetail.as_view(), name="problem-detail"),
    path("problems/<int:pk>/ai-solution/", AISolutionView.as_view(), name="ai-solution"),
    path("testcases/", TestCaseList.as_view(), name="testcase-list"),
    path("submissions/", SubmissionListView.as_view(), name="submission-list"),
    path("submissions/create/", SubmissionCreateView.as_view(), name="submission-create"),
    path("submissions/template/<int:pk>/<str:language>/", SubmissionTemplateView.as_view(), name="submission-template-lang"),
    path("submissions/<int:pk>/", SubmissionDetailView.as_view(), name="submission-detail"),
    path("exams/", ExamListView.as_view(), name="exam-list"),
    path("exams/<int:pk>/", ExamDetailView.as_view(), name="exam-detail"),
    path("exams/<int:exam_id>/results/", ExamResultsView.as_view(), name="exam-results"),
    path("exams/submit/", ExamSubmitView.as_view(), name="exam-submit"),
    path("exams/<int:exam_id>/complete/", ExamCompleteView.as_view(), name="exam-complete"),
    path("exam-statistics/", AllExamStatisticsView.as_view(), name="exam-statistics"),
    path("exam-statistics/user/", UserExamStatisticsView.as_view(), name="user-exam-statistics"),
    path("exam-statistics/<int:exam_id>/", ExamStatisticDetailView.as_view(), name="exam-statistic-detail"),
]

# Main URL patterns
urlpatterns = [
    path('api/token/', token_obtain_pair),
    path('api/token/refresh/', token_refresh),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
]

# Media files serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
