from rest_framework import serializers
from main.models import *
from .utils import generate_code_template

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

class ProblemSerializer(serializers.ModelSerializer):
    is_solved = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = '__all__'

    def get_is_solved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.submissions.filter(
                user=request.user,
                status='Accepted'
            ).exists()
        return False


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
            return generate_code_template(problem.function_name, input_example)
        except Exception:
            return generate_code_template('solve', '')

class SubmissionListSerializer(serializers.ModelSerializer):
    problem_title = serializers.CharField(source='problem.title', read_only=True)
    
    class Meta:
        model = Submission
        fields = '__all__'