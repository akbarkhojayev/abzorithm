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
from django.db.models import Case, When, IntegerField, Sum
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

    def get_queryset(self):
        queryset = Problem.objects.all()

        # Hide exam problems from authenticated users while exam is active
        if self.request.user and self.request.user.is_authenticated:
            from django.utils import timezone

            # Get active exams assigned to this user
            active_exams = Exam.objects.filter(
                assignments__user=self.request.user,
                is_active=True,
                start_time__lte=timezone.now(),
                end_time__gte=timezone.now()
            )

            # Exclude problems that are part of active exams
            exam_problems = ExamQuestion.objects.filter(
                exam__in=active_exams
            ).values_list('problem_id', flat=True)

            queryset = queryset.exclude(id__in=exam_problems)

        return queryset

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

class ExamListView(generics.ListAPIView):
    serializer_class = ExamSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Exam.objects.filter(
            assignments__user=user,
            is_active=True
        ).distinct()


class ExamDetailView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        exam = super().get_object()
        user = self.request.user

        if not ExamAssignment.objects.filter(exam=exam, user=user).exists():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Siz bu imtixonga kirishga vastalik oqaysiz")

        return exam


class ExamSubmitView(generics.CreateAPIView):
    serializer_class = ExamSubmissionSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        exam_id = request.data.get('exam')
        problem_id = request.data.get('problem')
        code = request.data.get('code')

        exam = Exam.objects.get(id=exam_id)
        problem = Problem.objects.get(id=problem_id)

        if not ExamAssignment.objects.filter(exam=exam, user=request.user).exists():
            return Response({'error': 'Vastalik yoq'}, status=status.HTTP_403_FORBIDDEN)

        # Get existing exam statistic
        exam_stat = ExamStatistic.objects.filter(user=request.user, exam=exam).first()

        # Check if exam is already completed - prevent retakes
        if exam_stat and exam_stat.is_completed:
            return Response({
                'error': 'Bu imtixon allaqachon yakunlangan. Yana topshira olmaysiz!',
                'exam_completed': True
            }, status=status.HTTP_403_FORBIDDEN)

        # Use exam's language
        language = exam.language

        submission = ExamSubmission.objects.create(
            exam=exam,
            user=request.user,
            problem=problem,
            code=code,
            language=language
        )

        # Get or create exam statistic
        if not exam_stat:
            exam_stat = ExamStatistic.objects.create(
                user=request.user,
                exam=exam,
                total_problems=exam.questions.count(),
                status='in_progress'
            )

        # Update submission count
        exam_stat.total_submissions += 1

        testcases = problem.testcases.all()
        for index, tc in enumerate(testcases, start=1):
            ok, status_str, output, exec_time = run_python_function(
                code, problem.function_name, tc.input_data, tc.expected_output,
                language=language
            )

            if not ok:
                submission.status = status_str
                submission.execution_time = exec_time
                submission.save()

                # Update attempted problems count
                exam_stat.attempted_problems = ExamSubmission.objects.filter(
                    exam=exam, user=request.user
                ).values('problem').distinct().count()

                exam_stat.save()

                return Response({
                    "id": submission.id,
                    "problem": problem.id,
                    "status": submission.status,
                    "failed_test": index,
                    "message": f"Test {index} failed: {status_str}",
                }, status=status.HTTP_201_CREATED)

        submission.status = "Accepted"
        submission.save()

        # Update statistics on acceptance
        exam_stat.correct_submissions += 1
        exam_stat.solved_problems = ExamSubmission.objects.filter(
            exam=exam, user=request.user, status='Accepted'
        ).values('problem').distinct().count()
        exam_stat.attempted_problems = ExamSubmission.objects.filter(
            exam=exam, user=request.user
        ).values('problem').distinct().count()

        # Check if all problems are solved - mark exam as completed
        if exam_stat.solved_problems >= exam_stat.total_problems and exam_stat.total_problems > 0:
            exam_stat.is_completed = True
            exam_stat.status = 'completed'
            exam_stat.completion_reason = 'manual'
            # Calculate final score
            if exam_stat.total_problems > 0:
                exam_stat.score = int((exam_stat.solved_problems / exam_stat.total_problems) * 500)
            from django.utils import timezone
            exam_stat.completed_at = timezone.now()

            # Add score to user
            request.user.score += exam_stat.score
            request.user.save()

        exam_stat.save()

        return Response({
            "id": submission.id,
            "problem": problem.id,
            "status": "Accepted",
            "message": "✓ Hamasi testlarni o'tdi!",
            "exam_completed": exam_stat.is_completed,
            "solved": f"{exam_stat.solved_problems}/{exam_stat.total_problems}",
        }, status=status.HTTP_201_CREATED)


class ExamResultsView(generics.ListAPIView):
    serializer_class = ExamSubmissionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        exam_id = self.kwargs.get('exam_id')
        return ExamSubmission.objects.filter(
            exam_id=exam_id,
            user=self.request.user
        ).order_by('-submitted_at')


class AISolutionView(generics.RetrieveAPIView):
    queryset = Problem.objects.all()
    permission_classes = (AllowAny,)
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        from groq import Groq
        import os

        problem = self.get_object()

        api_key = "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"
        client = Groq(api_key=api_key)

        prompt = f"""
Siz Python dasturchisi bo'lib, beginner (yangi o'rganayotgan) o'quvchilarga masalalarni yechishga yordam berasiz.

**MASALA:** {problem.title}

**TAVSIF:** {problem.description}

**KIRISH MISOLI:**
{problem.input_example}

**KUTILGAN CHIQISH:**
{problem.output_example}

**KODNI YOZISH QOIDALARI - JUDA MUHIM!:**

KOD ICHIDA:
- ❌ HECH QACHON # comment, # izoh, # tushuntirish yo'q!
- ❌ HECH QACHON Uzbek tilida nomi: satri, harfi, qadamma, massiv
- ✅ FAQAT ENGLISH variable va function nomlari: text, character, count, array
- ✅ Aniq nomlar: data emas, user_data; x emas, result
- ✅ Sodda, tushunarli, qisqa kod

EXAMPLE - NOTO'G'RI:
```python
def is_palindrom(satri):  # WRONG - Uzbekcha
    satri = satri.lower()  # WRONG - comment
    return satri == satri[::-1]
```

EXAMPLE - TO'G'RI:
```python
def is_palindrome(text):
    text = text.lower()
    return text == text[::-1]
```

**JAVOB FORMATI:**

## YECHIM 1: ENG SODDA USUL

KOD:
```python
[KODINGIZ - FAQAT ENGLISH VARIABLE NOMLARI!]
```

QADAMMA-QADAMGA TUSHUNTIRISH:
1. [Birinchi qadamni tushuntiring]
2. [Ikkinchi qadamni tushuntiring]
3. [Uchinchi qadamni tushuntiring]
...

MISOL BILAN TUSHUNTIRISH:
[Konkret misolda qanday ishlayotganini ko'rsating]

---

## YECHIM 2: OPTIMAL USUL

KOD:
```python
[OPTIMALROQ KOD - FAQAT ENGLISH VARIABLE NOMLARI!]
```

NIMA FARQI BORA?
[Birinchi va ikkinchi yechimning farqini sodda tilda tushuntiring]

NEGA BU TEZROQ?
[Vaqt murakkabligini beginner uchun tushunarli qilib tushuntiring]

MISOL BILAN TUSHUNTIRISH:
[Konkret misol bilan ko'rsating]

---

**MUHIM AYTGANLAR:**
- ❌ HECH QACHON Uzbekcha variable nomi yozmang: satri, harfi, massiv, qadamma
- ✅ FAQAT English: text, character, array, step, result, is_valid, etc.
- Tushuntirishlar VERY SIMPLE bo'lishi kerak (5-6 sinf darajasi)
- Har bir yangi atamani tushuntiring (masalan: "loop" = "takrorlash")
- Beginner darajada o'rganayotganlar uchun yozing
"""

        try:
            message = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                max_tokens=3000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
        except:
            try:
                message = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    max_tokens=3000,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
            except:
                message = client.chat.completions.create(
                    model="gemma-7b-it",
                    max_tokens=3000,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

        response_text = message.choices[0].message.content

        solutions = {
            "problem_id": problem.id,
            "problem_title": problem.title,
            "full_response": response_text,
            "language": "python"
        }

        return Response(solutions)


class UserExamStatisticsView(generics.ListAPIView):
    serializer_class = ExamStatisticSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return ExamStatistic.objects.filter(user=self.request.user).order_by('-completed_at', '-started_at')


class AllExamStatisticsView(generics.ListAPIView):
    serializer_class = ExamStatisticSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['exam', 'is_completed', 'user']
    search_fields = ['user__username', 'exam__title']
    ordering_fields = ['solved_problems', 'score', 'completed_at']
    ordering = ['-completed_at']

    def get_queryset(self):
        # Only staff can see all statistics, regular users see only their own
        if self.request.user.is_staff:
            return ExamStatistic.objects.all()
        return ExamStatistic.objects.filter(user=self.request.user)


class ExamStatisticDetailView(generics.RetrieveUpdateAPIView):
    queryset = ExamStatistic.objects.all()
    serializer_class = ExamStatisticSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        exam_id = self.kwargs.get('exam_id')
        return ExamStatistic.objects.get(exam_id=exam_id, user=self.request.user)


class ExamCompleteView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        exam_id = kwargs.get('exam_id')
        reason = request.data.get('reason', 'manual')  # manual, timeout, violation

        print(f"[ExamCompleteView] User: {request.user}, Exam ID: {exam_id}, Reason: {reason}")

        try:
            exam = Exam.objects.get(id=exam_id)
            print(f"[ExamCompleteView] Exam found: {exam.title}")
        except Exam.DoesNotExist:
            print(f"[ExamCompleteView] Exam not found: {exam_id}")
            return Response({'error': 'Imtixon topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        assignment = ExamAssignment.objects.filter(exam=exam, user=request.user).exists()
        print(f"[ExamCompleteView] Assignment exists: {assignment}")

        if not assignment:
            return Response({'error': 'Sizga bu imtixon tayinlanmadi'}, status=status.HTTP_403_FORBIDDEN)

        # Get or create exam statistic
        exam_stat, created = ExamStatistic.objects.get_or_create(
            user=request.user,
            exam=exam,
            defaults={'total_problems': exam.questions.count()}
        )
        print(f"[ExamCompleteView] Exam stat: created={created}, solved={exam_stat.solved_problems}, total={exam_stat.total_problems}")

        # Calculate final statistics
        exam_stat.solved_problems = ExamSubmission.objects.filter(
            exam=exam, user=request.user, status='Accepted'
        ).values('problem').distinct().count()
        exam_stat.attempted_problems = ExamSubmission.objects.filter(
            exam=exam, user=request.user
        ).values('problem').distinct().count()
        exam_stat.total_submissions = ExamSubmission.objects.filter(
            exam=exam, user=request.user
        ).count()
        exam_stat.correct_submissions = ExamSubmission.objects.filter(
            exam=exam, user=request.user, status='Accepted'
        ).count()

        # Calculate score: (solved/total) * 500, or 0 if security violation
        if reason == 'violation':
            exam_stat.score = 0
        else:
            if exam_stat.total_problems > 0:
                exam_stat.score = int((exam_stat.solved_problems / exam_stat.total_problems) * 500)
            else:
                exam_stat.score = 0

        # Mark as completed
        exam_stat.is_completed = True
        exam_stat.status = 'completed'
        from django.utils import timezone
        exam_stat.completed_at = timezone.now()
        exam_stat.save()

        # Add score to user account
        request.user.score += exam_stat.score
        request.user.save()

        # Mark all submissions as exam_completed
        ExamSubmission.objects.filter(
            exam=exam, user=request.user
        ).update(is_exam_completed=True, completed_at=timezone.now())

        serializer = ExamStatisticSerializer(exam_stat)
        response_data = {
            'message': 'Imtixon yechilgan sifatida belgilandi',
            'reason': reason,
            'statistics': serializer.data
        }
        print(f"[ExamCompleteView] Sending response: score={exam_stat.score}, solved={exam_stat.solved_problems}/{exam_stat.total_problems}")
        return Response(response_data, status=status.HTTP_200_OK)


class UserProfileStatsView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        stats = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'score': user.score,
            'total_exams_assigned': user.exam_assignments.count(),
            'total_exams_completed': ExamStatistic.objects.filter(
                user=user, is_completed=True
            ).count(),
            'total_problems_solved': ExamStatistic.objects.filter(
                user=user
            ).aggregate(total=Sum('solved_problems'))['total'] or 0,
            'total_problems_attempted': ExamStatistic.objects.filter(
                user=user
            ).aggregate(total=Sum('attempted_problems'))['total'] or 0,
            'overall_success_rate': self._calculate_success_rate(user),
            'exam_statistics': ExamStatisticSerializer(
                ExamStatistic.objects.filter(user=user).order_by('-completed_at'),
                many=True
            ).data
        }
        return Response(stats)

    @staticmethod
    def _calculate_success_rate(user):
        stats = ExamStatistic.objects.filter(user=user).aggregate(
            correct=Sum('correct_submissions'),
            total=Sum('total_submissions')
        )
        if stats['total'] and stats['total'] > 0:
            return round((stats['correct'] / stats['total']) * 100, 1)
        return 0
