from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Problem, TestCase, Submission


# ====================
# Custom User Admin
# ====================
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


# ====================
# Problem Admin
# ====================
class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1  # yangi qo‘shishda bitta bo‘sh forma chiqadi


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "difficulty", "created_at", "tags")
    list_filter = ("difficulty", "created_at", "tags")
    search_fields = ("title", "description", "tags")
    ordering = ("-created_at",)
    inlines = [TestCaseInline]  # Problemni ochganda test case’larni ham qo‘shib bo‘ladi


# ====================
# TestCase Admin
# ====================
@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ("id", "problem", "order", "is_hidden")
    list_filter = ("is_hidden", "problem")
    search_fields = ("input_data", "expected_output")
    ordering = ("problem", "order")


# ====================
# Submission Admin
# ====================
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "problem", "status", "language", "execution_time", "memory_used", "submitted_at")
    list_filter = ("status", "language", "submitted_at")
    search_fields = ("user__username", "problem__title", "code")
    ordering = ("-submitted_at",)
    readonly_fields = ("submitted_at",)
