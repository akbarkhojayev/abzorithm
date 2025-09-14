from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from main.models import *
from main.serializers import *
from main.utils_docker import run_python_function_docker as run_python_function

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

    def get_object(self):
        return self.request.user

class ProblemList(generics.ListAPIView):
    queryset = Problem.objects.all().order_by('-created_at')
    serializer_class = ProblemSerializer
    permission_classes = (AllowAny,)

class ProblemDetail(generics.RetrieveAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = (IsAuthenticated,)

class TestCaseList(generics.ListAPIView):
    queryset = TestCase.objects.all().order_by('order')
    serializer_class = TestCaseSerializer
    permission_classes = (AllowAny,)

class SubmissionListCreateView(generics.ListCreateAPIView):
    queryset = Submission.objects.all().order_by('-submitted_at')
    serializer_class = SubmissionSerializer

    def perform_create(self, serializer):
        submission = serializer.save()
        problem = submission.problem
        testcases = problem.testcases.all()

        all_passed = True
        total_exec_time = 0

        for tc in testcases:
            ok, status, msg, exec_time = run_python_function(
                submission.code,
                problem.function_name,
                tc.input_data,
                tc.expected_output
            )
            total_exec_time += exec_time
            if not ok:
                all_passed = False
                submission.status = status
                submission.execution_time = total_exec_time
                submission.save()
                return

        already_accepted = Submission.objects.filter(
            user=submission.user,
            problem=problem,
            status="Accepted"
        ).exists()
        submission.status = "Accepted"
        submission.execution_time = total_exec_time
        submission.save()
        if not already_accepted:
            user = submission.user
            user.score = (user.score or 0) + 1
            user.save()

class SubmissionDetailView(generics.RetrieveAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = (IsAuthenticated,)

class SubmissionListView(generics.ListAPIView):
    queryset = Submission.objects.all().order_by('-submitted_at')
    serializer_class = SubmissionListSerializer
    permission_classes = (IsAuthenticated,)

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

        # Agar kod bo‘sh bo‘lsa -> template generate qilamiz
        if not submission.code or not str(submission.code).strip():
            input_example = getattr(problem, "input_example", "")
            submission.code = generate_code_template(problem.function_name, input_example)
            submission.save()

        total_exec_time = 0
        failed_test = None

        # Har bir testni ishlatamiz
        for index, tc in enumerate(testcases, start=1):
            ok, status_str, output, exec_time = run_python_function(
                submission.code,
                problem.function_name,
                tc.input_data,
                tc.expected_output
            )
            total_exec_time += exec_time

            if not ok:
                # ❌ Xato chiqqan joyda to‘xtaymiz
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

        # ✅ Agar shu joyga yetgan bo‘lsa — hammasi o‘tdi
        submission.status = "Accepted"
        submission.execution_time = total_exec_time
        submission.failed_test = None
        submission.error_input = None
        submission.error_expected = None
        submission.error_output = None
        submission.save()

        # ✅ Faqat birinchi Accepted bo‘lsa score +1
        already_accepted = Submission.objects.filter(
            user=user,
            problem=problem,
            status="Accepted"
        ).exclude(id=submission.id).exists()

        if not already_accepted:
            user.score = (user.score or 0) + 1
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
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        problem = self.get_object()
        template = generate_code_template(problem.function_name, problem.input_example, problem.output_example, problem.description)
        return Response({
            "problem": problem.id,
            "template_code": template
        })

class LeaderboardView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-score', 'username')
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
