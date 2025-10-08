from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Problem, TestCase, Submission

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Qo‘shimcha ma’lumotlar", {"fields": ("bio", "avatar", "score", "country")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Qo‘shimcha ma’lumotlar", {"fields": ("bio", "avatar", "score", "country")}),
    )
    list_display = ("username", "email", "score", "country", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "country")
    search_fields = ("username", "email", "country")
    ordering = ("-score", "username")


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "difficulty", "created_at", "tags", "slug")
    list_filter = ("difficulty", "created_at", "tags")
    search_fields = ("title", "description", "tags")
    ordering = ("-created_at",)
    inlines = [TestCaseInline]
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