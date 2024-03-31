import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe



class CustomUserManager(UserManager):
    #search_fields = ['email']
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not specified a valid e-mail address")
    
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        print("password set: ", user.password)
        user.save(using=self.db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='uploads/avatars')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now, editable=True)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    
    EMAIL_FIELD = 'email'

    search_fields = ["email"]
    def avatar_image(self):
        if self.avatar:
            url = f'{settings.WEBSITE_URL}{self.avatar.url}'
            #return f'<img src={url} className="rounded-full" />'
            return mark_safe('<img src="%s" class="rounded-circle" width="50" height="50" />' % (url))
        else:
            return ''