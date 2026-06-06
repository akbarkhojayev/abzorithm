from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg import openapi
from main.models import *
from main.serializers import *
from main.utils import run_python_function, generate_javascript_template, generate_dart_template
from rest_framework.parsers import FormParser,MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from main.filters import *
from django.db.models import Case, When, IntegerField
from rest_framework.filters import SearchFilter, OrderingFilter


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser,FormParser]
    def get_object(self):
        return self.request.user

class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

class ProblemList(generics.ListAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['difficulty', 'tags']
    ordering = ['difficulty']
    search_fields = ['title', 'description']
    pagination_class = None

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='difficulty',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Difficulty of the problem',
            ),
            openapi.Parameter(
                name='limit',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Number of results to return per page (default: 10)',
            ),
            openapi.Parameter(
                name='offset',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='The initial index from which to return the results (default: 0)',
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        queryset = Problem.objects.annotate(
            difficulty_order=Case(
                When(difficulty='Easy', then=1),
                When(difficulty='Medium', then=2),
                When(difficulty='Hard', then=3),
                default=4,
                output_field=IntegerField(),
            )
        )
        return queryset

    def list(self, request, *args, **kwargs):
        limit = int(request.query_params.get('limit', 10))
        offset = int(request.query_params.get('offset', 0))

        limit = min(limit, 100)
        limit = max(limit, 1)

        queryset = self.filter_queryset(self.get_queryset())
        total = queryset.count()

        paginated_queryset = queryset[offset:offset + limit]
        serializer = self.get_serializer(paginated_queryset, many=True)

        return Response({
            'count': total,
            'limit': limit,
            'offset': offset,
            'results': serializer.data
        })

class ProblemDetail(generics.RetrieveAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class TestCaseList(generics.ListAPIView):
    queryset = TestCase.objects.all().order_by('order')
    serializer_class = TestCaseSerializer
    permission_classes = (AllowAny,)

# class SubmissionListCreateView(generics.ListCreateAPIView):
#     queryset = Submission.objects.all().order_by('-submitted_at')
#     serializer_class = SubmissionSerializer
#
#     def perform_create(self, serializer):
#         submission = serializer.save()
#         problem = submission.problem
#         testcases = problem.testcases.all()
#
#         all_passed = True
#         total_exec_time = 0
#
#         for tc in testcases:
#             ok, status, msg, exec_time = run_python_function(
#                 submission.code,
#                 problem.function_name,
#                 tc.input_data,
#                 tc.expected_output
#             )
#             total_exec_time += exec_time
#             if not ok:
#                 all_passed = False
#                 submission.status = status
#                 submission.execution_time = total_exec_time
#                 submission.save()
#                 return
#
#         already_accepted = Submission.objects.filter(
#             user=submission.user,
#             problem=problem,
#             status="Accepted"
#         ).exists()
#         submission.status = "Accepted"
#         submission.execution_time = total_exec_time
#         submission.save()
#         if not already_accepted:
#             user = submission.user
#
#             if problem.difficulty == "Easy":
#                 points = 5
#             elif problem.difficulty == "Medium":
#                 points = 7
#             elif problem.difficulty == "Hard":
#                 points = 10
#             else:
#                 points = 0
#             user.score = (user.score or 0) + points
#             user.save()

class SubmissionDetailView(generics.RetrieveAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = (IsAuthenticated,)

class SubmissionListView(generics.ListAPIView):
    serializer_class = SubmissionListSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='limit',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Number of results to return per page (default: 20)',
            ),
            openapi.Parameter(
                name='offset',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='The initial index from which to return the results (default: 0)',
            ),
        ]
    )
    def get_queryset(self):
        user_id = self.request.query_params.get('user', None)
        if user_id is not None:
            queryset = Submission.objects.filter(user_id=user_id).order_by('-submitted_at')
        else:
            queryset = Submission.objects.filter(user=self.request.user).order_by('-submitted_at')
        return queryset

    def list(self, request, *args, **kwargs):
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))

        limit = min(limit, 100)
        limit = max(limit, 1)

        queryset = self.filter_queryset(self.get_queryset())
        total = queryset.count()

        paginated_queryset = queryset[offset:offset + limit]
        serializer = self.get_serializer(paginated_queryset, many=True)

        return Response({
            'count': total,
            'limit': limit,
            'offset': offset,
            'results': serializer.data
        })

class SubmissionCreateView(generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionCreateSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save()
        problem = submission.problem
        user = submission.user
        testcases = problem.testcases.all()

        if not submission.code or not str(submission.code).strip():
            input_example = getattr(problem, "input_example", "")
            output_example = getattr(problem, "output_example", "")
            if submission.language == 'javascript':
                submission.code = generate_javascript_template(problem.function_name, input_example, output_example)
            elif submission.language == 'dart':
                submission.code = generate_dart_template(problem.function_name, input_example, output_example)
            else:
                submission.code = generate_code_template(problem.function_name, input_example, output_example)
            submission.save()

        total_exec_time = 0
        failed_test = None

        for index, tc in enumerate(testcases, start=1):
            ok, status_str, output, exec_time = run_python_function(
                submission.code,
                problem.function_name,
                tc.input_data,
                tc.expected_output,
                language=submission.language
            )
            total_exec_time += exec_time

            if not ok:
                submission.status = status_str
                submission.execution_time = total_exec_time
                submission.failed_test = index
                submission.error_input = tc.input_data
                submission.error_expected = tc.expected_output
                submission.error_output = output
                submission.save()

                return Response({
                    "id": submission.id,
                    "status": submission.status,
                    "execution_time": submission.execution_time,
                    "failed_test": submission.failed_test,
                    "error_input": submission.error_input,
                    "error_expected": submission.error_expected,
                    "error_output": submission.error_output,
                    "user_score": user.score,
                }, status=status.HTTP_201_CREATED)

        submission.status = "Accepted"
        submission.execution_time = total_exec_time
        submission.failed_test = None
        submission.error_input = None
        submission.error_expected = None
        submission.error_output = None
        submission.save()

        already_accepted = Submission.objects.filter(
            user=user,
            problem=problem,
            status="Accepted"
        ).exclude(id=submission.id).exists()

        if not already_accepted:
            if problem.difficulty == "Easy":
                points = 5
            elif problem.difficulty == "Medium":
                points = 7
            elif problem.difficulty == "Hard":
                points = 10
            else:
                points = 0
            user.score = (user.score or 0) + points
            user.save()

        return Response({
            "id": submission.id,
            "status": submission.status,
            "execution_time": submission.execution_time,
            "failed_test": submission.failed_test,
            "error_input": submission.error_input,
            "error_expected": submission.error_expected,
            "error_output": submission.error_output,
            "user_score": user.score,
        }, status=status.HTTP_201_CREATED)


class SubmissionTemplateView(generics.RetrieveAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        problem = self.get_object()

        language = kwargs.get('language') or request.query_params.get('language', 'python')

        if language == 'javascript':
            template = generate_javascript_template(problem.function_name, problem.input_example,
                                                    problem.output_example)
        elif language == 'dart':
            template = generate_dart_template(problem.function_name, problem.input_example, problem.output_example)
        else:
            template = generate_code_template(problem.function_name, problem.input_example, problem.output_example,
                                              problem.description)

        return Response({
            "problem": problem.id,
            "language": language,
            "template_code": template
        })

class LeaderboardView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-score', 'username')
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
