from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    score = models.IntegerField(default=0)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username

class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    input_example = models.TextField()
    output_example = models.TextField()
    tags = models.CharField(max_length=255, blank=True)
    function_name = models.CharField(max_length=50, default="Solution().solve")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='testcases')
    input_data = models.TextField()
    expected_output = models.TextField()
    order = models.IntegerField(default=0)
    is_hidden = models.BooleanField(default=True)

    def __str__(self):
        return f"TestCase for {self.problem.title} (#{self.order})"


class Submission(models.Model):
    STATUS_CHOICES = [
        ('Accepted', 'Accepted'),
        ('Wrong Answer', 'Wrong Answer'),
        ('RuntimeError', 'RuntimeError'),
        ('TimeLimit', 'TimeLimit'),
    ]

    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('cpp', 'C++'),
        ('java', 'Java'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="submissions")
    code = models.TextField()
    language = models.CharField(max_length=10, default='python', choices=LANGUAGE_CHOICES)
    status = models.CharField(max_length=20, default='Wrong Answer', choices=STATUS_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)
    execution_time = models.FloatField(null=True, blank=True)
    memory_used = models.FloatField(null=True, blank=True)

    # ❗ LeetCode uslubidagi qo‘shimchalar
    failed_test = models.IntegerField(null=True, blank=True)   # Qaysi testda yiqildi
    error_input = models.TextField(null=True, blank=True)      # Test input
    error_expected = models.TextField(null=True, blank=True)   # Expected natija
    error_output = models.TextField(null=True, blank=True)     # Sizning chiqaringan natijangiz

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} ({self.status})"

