from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class Group(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name


class Patient(models.Model):
    name = models.CharField(max_length=255)
    groups = models.ManyToManyField(Group)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    age = models.IntegerField()
    date_of_birth = models.DateField(null=True)
    health_record = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.IntegerField(blank=True)
    address = models.TextField()
    insurance_id = models.CharField(max_length=30, default=None, blank=True, null=True)

    def __str__(self):
        return self.email


class LoginCredential(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
