from rest_framework import serializers
from main.models import *
from .utils import generate_code_template, generate_javascript_template, generate_dart_template

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "bio", "avatar")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "bio", "avatar", "score")

class UserUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "bio", "avatar")
        read_only_fields = ("id", "username", "email")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = ['ex_input', 'ex_output']

class ProblemSerializer(serializers.ModelSerializer):
    is_solved = serializers.SerializerMethodField()
    examples = ExampleSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    languages = serializers.SerializerMethodField()
    testcase_count = serializers.SerializerMethodField()
    example_count = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = [
            'id', 'title', 'slug', 'description', 'difficulty',
            'input_example', 'output_example', 'function_name',
            'tags', 'created_at', 'is_solved', 'examples',
            'categories', 'languages', 'testcase_count', 'example_count'
        ]

    def get_is_solved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.submissions.filter(
                user=request.user,
                status='Accepted'
            ).exists()
        return False

    def get_languages(self, obj):
        return ['python', 'javascript', 'dart']

    def get_testcase_count(self, obj):
        return obj.testcases.count()

    def get_example_count(self, obj):
        return obj.examples.count()


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

class SubmissionCreateSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=False, allow_blank=True)
    template_code = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Submission
        fields = (
            'id', 'user', 'problem', 'code', 'language',
            'status', 'execution_time', 'memory_used', 'submitted_at', 'template_code'
        )
        read_only_fields = ('id', 'status', 'execution_time', 'memory_used', 'submitted_at')

    def get_template_code(self, obj):
        try:
            problem = obj.problem
            input_example = getattr(problem, "input_example", "")
            output_example = getattr(problem, "output_example", "")
            language = obj.language
            
            if language == 'javascript':
                return generate_javascript_template(problem.function_name, input_example, output_example)
            elif language == 'dart':
                return generate_dart_template(problem.function_name, input_example, output_example)
            else:
                return generate_code_template(problem.function_name, input_example, output_example)
        except Exception:
            return generate_code_template('solve', '', '')

class SubmissionListSerializer(serializers.ModelSerializer):
    problem_title = serializers.CharField(source='problem.title', read_only=True)
    difficulty = serializers.CharField(source='problem.difficulty', read_only=True)
    problem_slug = serializers.CharField(source='problem.slug', read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id', 'user', 'problem', 'problem_title', 'problem_slug',
            'code', 'language', 'status', 'submitted_at', 'execution_time',
            'memory_used', 'failed_test', 'error_input', 'error_expected',
            'error_output', 'difficulty'
        ]


class ExamQuestionSerializer(serializers.ModelSerializer):
    problem_detail = ProblemSerializer(source='problem', read_only=True)
    template_code = serializers.SerializerMethodField()

    class Meta:
        model = ExamQuestion
        fields = ['id', 'problem', 'problem_detail', 'order', 'template_code']

    def get_template_code(self, obj):
        try:
            problem = obj.problem
            input_example = getattr(problem, "input_example", "")
            output_example = getattr(problem, "output_example", "")

            from .utils import generate_code_template, generate_javascript_template, generate_dart_template

            # Get language from exam
            language = getattr(obj.exam, 'language', 'python')

            # Return template for exam's language only
            if language == 'javascript':
                return generate_javascript_template(problem.function_name, input_example, output_example)
            elif language == 'dart':
                return generate_dart_template(problem.function_name, input_example, output_example)
            else:
                return generate_code_template(problem.function_name, input_example, output_example)
        except Exception:
            return ''


class ExamSerializer(serializers.ModelSerializer):
    questions = ExamQuestionSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = [
            'id', 'title', 'description', 'duration_minutes', 'start_time',
            'end_time', 'is_active', 'language', 'created_by', 'created_by_name', 'created_at',
            'questions', 'question_count'
        ]

    def get_question_count(self, obj):
        return obj.questions.count()


class ExamAssignmentSerializer(serializers.ModelSerializer):
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ExamAssignment
        fields = ['id', 'exam', 'exam_title', 'user', 'user_name', 'assigned_at']


class ExamSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSubmission
        fields = '__all__'


class ExamStatisticSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    success_rate = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = ExamStatistic
        fields = [
            'id', 'user', 'user_name', 'exam', 'exam_title', 'status', 'total_problems',
            'solved_problems', 'attempted_problems', 'total_submissions',
            'correct_submissions', 'time_spent_minutes', 'started_at',
            'completed_at', 'is_completed', 'score', 'success_rate',
            'progress_percentage'
        ]
        read_only_fields = ('success_rate', 'progress_percentage')

    def get_success_rate(self, obj):
        if obj.total_submissions == 0:
            return 0
        return round((obj.correct_submissions / obj.total_submissions) * 100, 1)

    def get_progress_percentage(self, obj):
        if obj.total_problems == 0:
            return 0
        return round((obj.solved_problems / obj.total_problems) * 100, 1)
