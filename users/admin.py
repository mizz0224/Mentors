from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "계정 정보",
            {
                "fields" : (
                    "name",
                    "birthdate",
                    "gender",
                )
            },
        ),
    )
    
    list_display = (
        "name",
        "birthdate",
        "gender",
        "login_method"
    )
    
    list_filter = (
        "birthdate",
        "gender",
    )
    
@admin.register(models.Mentor)
class MentorAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "계정 정보",
            {
                "fields" : (
                    "is_authorized",
                    "is_supermento",
                    "user",
                )
            },
        ),
        (
            "멘토 정보",
            {
                "fields" : (
                    "main_branch",
                    "sub_branch",
                    "company",
                    "department",
                    "career",
                )
            },
        ),
    )
    
    list_display = (
        "__str__",
        "main_branch",
        "sub_branch",
        "company",
        "department",
        "career",
        "is_authorized",
        "is_supermento",
    )
    
    list_filter = (
        "is_authorized",
        "is_supermento",
    )
    
@admin.register(models.MainBranch)
class MainBranchAdmin(admin.ModelAdmin):
    pass
    
@admin.register(models.SubBranch)
class SubBranchAdmin(admin.ModelAdmin):
    pass