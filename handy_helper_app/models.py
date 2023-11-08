from django.db import models
import re


class UserManager(models.Manager):
    @staticmethod
    def register_validator(post_data):
        errors = {}
        password1 = post_data["password"]
        password2 = post_data["confirm"]
        if len(post_data["first_name"]) < 2:
            errors["first_name"] = "First name should not be less than 2 characters"
        if len(post_data["last_name"]) < 2:
            errors["last_name"] = "Last name should not be less than 2 characters"
        email_regex = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        if not email_regex.match(post_data["email"]):
            errors["email"] = "Invalid email address"
        if len(post_data["password"]) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if password1 != password2:
            errors["confirm"] = "Passwords did not match"
        user_email_check = User.objects.filter(email=post_data["email"])
        if len(user_email_check) >= 1:
            errors["duplicate"] = "Email address already being used"
        return errors


class JobManager(models.Manager):
    @staticmethod
    def job_validator(post_data):
        errors = {}
        if len(post_data["title"]) < 3:
            errors["title"] = "Title must be more than 3 characters"
        if len(post_data["desc"]) < 3:
            errors["desc"] = "Description must be more than 3 characters"
        if len(post_data["location"]) < 3:
            errors["location"] = "Location must be more than 3 characters"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Job(models.Model):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(
        User, related_name="jobs_added", on_delete=models.CASCADE
    )
    taken_by = models.ForeignKey(
        User, related_name="jobs_taken", null=True, on_delete=models.CASCADE
    )
    objects = JobManager()
