from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import AdminProfile

# Register your models here.
from rest_framework_simplejwt import token_blacklist

class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)

User = get_user_model()

admin.site.register(User)
admin.site.unregister(Group)
admin.site.register(AdminProfile)