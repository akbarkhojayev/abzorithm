from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Problem, TestCase, Submission, Example, Exam, ExamQuestion, ExamAssignment, ExamSubmission, ExamStatistic


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Qo’shimcha ma’lumotlar", {"fields": ("bio", "avatar", "score")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Qo’shimcha ma’lumotlar", {"fields": ("bio", "avatar", "score")}),
    )
    list_display = ("username", "email", "score", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("-score", "username")


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1

class ExampleInline(admin.TabularInline):
    model = Example
    extra = 1
    fields = ('ex_input', 'ex_output')
    show_change_link = True

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "difficulty", "created_at", "tags", "slug")
    list_filter = ("difficulty", "created_at", "tags")
    search_fields = ("title", "description", "tags")
    ordering = ("-created_at",)
    inlines = [TestCaseInline, ExampleInline]
    readonly_fields = ("slug",)


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ("id", "problem", "order", "is_hidden")
    list_filter = ("is_hidden", "problem")
    search_fields = ("input_data", "expected_output")
    ordering = ("problem", "order")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "problem", "status", "language", "execution_time", "memory_used", "submitted_at")
    list_filter = ("status", "language", "submitted_at")
    search_fields = ("user__username", "problem__title", "code")
    ordering = ("-submitted_at",)
    readonly_fields = ("submitted_at",)


class ExamQuestionInline(admin.TabularInline):
    model = ExamQuestion
    extra = 1
    fields = ('problem', 'order')


class ExamAssignmentInline(admin.TabularInline):
    model = ExamAssignment
    extra = 10
    fields = ('user', 'assigned_at')
    readonly_fields = ('assigned_at',)
    raw_id_fields = ('user',)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "language", "duration_minutes", "start_time", "end_time", "is_active", "created_by", "created_at", "user_count")
    list_filter = ("is_active", "language", "start_time", "created_at")
    search_fields = ("title", "description", "created_by__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "created_by")
    fieldsets = (
        ("Asosiy ma'lumotlar", {
            "fields": ("title", "description", "language", "duration_minutes")
        }),
        ("Vaqt", {
            "fields": ("start_time", "end_time")
        }),
        ("Boshqa", {
            "fields": ("is_active", "created_by", "created_at")
        }),
    )
    inlines = [ExamQuestionInline, ExamAssignmentInline]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def user_count(self, obj):
        return obj.assignments.count()
    user_count.short_description = "Tayinlangan Userlar"


@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "exam", "problem", "order")
    list_filter = ("exam",)
    search_fields = ("exam__title", "problem__title")
    ordering = ("exam", "order")


@admin.register(ExamAssignment)
class ExamAssignmentAdmin(admin.ModelAdmin):
    list_display = ("id", "exam", "user", "assigned_at")
    list_filter = ("exam", "assigned_at")
    search_fields = ("exam__title", "user__username")
    ordering = ("-assigned_at",)


@admin.register(ExamSubmission)
class ExamSubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "exam", "user", "problem", "status", "submitted_at", "is_exam_completed")
    list_filter = ("exam", "status", "submitted_at", "is_exam_completed")
    search_fields = ("exam__title", "user__username", "problem__title")
    ordering = ("-submitted_at",)
    readonly_fields = ("submitted_at",)


@admin.register(ExamStatistic)
class ExamStatisticAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "exam", "status_display", "solved_problems", "total_problems", "success_rate_display", "completed_at")
    list_filter = ("status", "is_completed", "completed_at")
    search_fields = ("user__username", "exam__title")
    ordering = ("-completed_at", "-started_at")
    readonly_fields = ("started_at", "completed_at", "success_rate", "progress_percentage", "status")
    fieldsets = (
        ("User & Exam", {
            "fields": ("user", "exam", "status")
        }),
        ("Problems & Solutions", {
            "fields": ("total_problems", "solved_problems", "attempted_problems", "correct_submissions", "total_submissions")
        }),
        ("Performance", {
            "fields": ("score", "success_rate", "progress_percentage")
        }),
        ("Time & Completion", {
            "fields": ("time_spent_minutes", "is_completed", "started_at", "completed_at")
        }),
    )

    def status_display(self, obj):
        status_colors = {
            'not_started': '⚪',
            'in_progress': '🟡',
            'completed': '🟢',
        }
        return f"{status_colors.get(obj.status, '❓')} {obj.get_status_display()}"
    status_display.short_description = "Status"

    def success_rate_display(self, obj):
        return f"{obj.success_rate:.1f}%"
    success_rate_display.short_description = "Success Rate"

    def has_add_permission(self, request):
        return False