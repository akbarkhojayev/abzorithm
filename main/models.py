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
        ('Runtime Error', 'Runtime Error'),
        ('Time Limit Exceeded', 'Time Limit Exceeded'),
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


class Exam(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('dart', 'Dart'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_minutes = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='python')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_exams")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        unique_together = ('exam', 'problem')
        ordering = ['order']

    def __str__(self):
        return f"{self.exam.title} - {self.problem.title}"


class ExamAssignment(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="assignments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exam_assignments")
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('exam', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.exam.title}"


class ExamSubmission(models.Model):
    STATUS_CHOICES = [
        ('Accepted', 'Accepted'),
        ('Wrong Answer', 'Wrong Answer'),
        ('Runtime Error', 'Runtime Error'),
        ('Time Limit Exceeded', 'Time Limit Exceeded'),
    ]

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="submissions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exam_submissions")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=10, default='python')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Wrong Answer')
    submitted_at = models.DateTimeField(auto_now_add=True)
    execution_time = models.FloatField(null=True, blank=True)
    is_exam_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.user.username} - {self.exam.title} - {self.problem.title}"


class ExamStatistic(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Boshlash'),
        ('in_progress', 'Davom etyapti'),
        ('completed', 'Yechilgan'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exam_statistics")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="statistics")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    total_problems = models.IntegerField(default=0)
    solved_problems = models.IntegerField(default=0)
    attempted_problems = models.IntegerField(default=0)
    total_submissions = models.IntegerField(default=0)
    correct_submissions = models.IntegerField(default=0)
    time_spent_minutes = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'exam')
        verbose_name_plural = "Exam Statistics"
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['exam', 'is_completed']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.exam.title}: {self.solved_problems}/{self.total_problems} ({self.get_status_display()})"

    def update_status(self):
        """Automatically update status based on completion"""
        if self.is_completed:
            self.status = 'completed'
        elif self.total_submissions > 0:
            self.status = 'in_progress'
        else:
            self.status = 'not_started'

    @property
    def success_rate(self):
        if self.total_submissions == 0:
            return 0
        return (self.correct_submissions / self.total_submissions) * 100

    @property
    def progress_percentage(self):
        if self.total_problems == 0:
            return 0
        return (self.solved_problems / self.total_problems) * 100

    def save(self, *args, **kwargs):
        self.update_status()
        super().save(*args, **kwargs)
