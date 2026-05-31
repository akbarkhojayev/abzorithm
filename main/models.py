from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

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
    categories = models.ManyToManyField(Category, related_name="problems")
    tags = models.CharField(max_length=255, blank=True)
    function_name = models.CharField(max_length=50, default="Solution().solve")
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            while Problem.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Example(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="examples")
    ex_input = models.TextField()
    ex_output = models.TextField()


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
        ('javascript', 'JavaScript'),
        ('dart', 'Dart'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="submissions")
    code = models.TextField()
    language = models.CharField(max_length=10, default='python', choices=LANGUAGE_CHOICES)
    status = models.CharField(max_length=20, default='Wrong Answer', choices=STATUS_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)
    execution_time = models.FloatField(null=True, blank=True)
    memory_used = models.FloatField(null=True, blank=True)

    failed_test = models.IntegerField(null=True, blank=True)
    error_input = models.TextField(null=True, blank=True)
    error_expected = models.TextField(null=True, blank=True)
    error_output = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} ({self.status})"
