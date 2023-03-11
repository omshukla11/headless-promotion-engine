from django.db import models

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self,username,email,password=None,**extra_fields):

        if username is None:
            raise ValueError('Users should have a username')
        if email is None:
            raise ValueError('Users should have an Email')
        user = self.model(username = username, email = self.normalize_email(email))
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self,username,email,password,**extra_fields):
        if password is None:
            raise TypeError('Password should not be none')
        
        user = self.create_user(username,self.normalize_email(email),password)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.is_verified = True
        user.save(using = self._db)
        return user

    def create_staffuser(self,username,email,password,**extra_fields):
        user = self.create_superuser(username,self.normalize_email(email),password)
        user.is_admin = False
        user.save(using=self._db)
        return user


AUTH_PROVIDERS = {'facebook':'facebook', 'google':'google', 'twitter':'twitter', 'email':'email'}

class User(AbstractBaseUser, PermissionsMixin):
    username          = models.CharField(max_length = 200, unique = True, blank = False, db_index= True)
    email             = models.EmailField(max_length = 200, unique = True, db_index= True)
    first_name        = models.CharField(max_length = 200, blank = True)
    last_name         = models.CharField(max_length = 200, blank = True)
    is_admin          = models.BooleanField(default = False)
    is_active         = models.BooleanField(default =True)
    is_verified       = models.BooleanField(default =False)
    is_staff          = models.BooleanField(default = False)
    is_superuser      = models.BooleanField(default = False)
    created_at        = models.DateTimeField(blank = False,auto_now_add=True)
    update_at         = models.DateTimeField(blank = False,auto_now=True)
    auth_provider     = models.CharField(max_length = 255, blank = False, null = False, default=AUTH_PROVIDERS.get('email'))


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

class AdminProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    companyname = models.CharField(max_length=255,blank=True, null=True)
    coupon_count = models.IntegerField(default=0,blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    img = models.ImageField(blank=True, null=True)

class UserData(models.Model):
    admin = models.ForeignKey(AdminProfile, on_delete=models.SET_NULL, null=True)
    