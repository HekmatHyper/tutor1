from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('tutor', 'Tutor'),
        ('viewer', 'Viewer'),
    ]

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone', 'role']

    def __str__(self):
        return self.email
    

class TutorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'tutor'})
    experience = models.TextField()
    skills = models.TextField()
    interests = models.TextField()
    location = models.CharField(max_length=100)
    timezone = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"TutorProfile: {self.user.full_name}"


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    academic_needs = models.TextField()
    program_details = models.CharField(max_length=255)
    preferred_format = models.CharField(max_length=50)
    required_hours = models.PositiveIntegerField()

    def __str__(self):
        return f"StudentProfile: {self.user.full_name}"



class TutorAssignment(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE)
    tutor = models.ForeignKey('TutorProfile', on_delete=models.CASCADE)
    assigned_by = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'admin'})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tutor.user.full_name} -> {self.student.user.full_name}"


class TutorPayment(models.Model):
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'admin'})

    def __str__(self):
        return f"{self.tutor.user.full_name} - ${self.amount_paid} for {self.hours_worked} hrs"
