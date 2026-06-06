from rest_framework import serializers
from main.models import *
from .utils import generate_code_template, generate_javascript_template, generate_dart_template

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "bio", "avatar", "country")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "bio", "avatar", "score", "country")

class UserUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = User
        fields = ("id", "username", "email", "bio", "avatar", "country")
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
